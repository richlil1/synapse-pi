import tkinter as tk
from tkinter import ttk
import threading
import requests
import time
import os
import json
import background_processes as bg
import datetime
from utils import generate_key, load_key, save_key, encrypt, decrypt, save_config, load_config, load_secrets, save_secrets

# -------------------- CONFG --------------------

LLAMA_MODEL = "meta-llama/llama-3-8b-instruct"
OPENAI_MODEL = "gpt-4o"
api_keys = {}
key = load_key() or generate_key()
if not os.path.exists("key.key"):
    save_key(key)

LEADERBOARD_FILE = ".local_scores.json"
CHAT_HISTORY_FILE = ".chat_data"
WIN_SCORE = 17
MAX_ENEMIES = 4
chat_history_enabled = False

# -------------------- API functions --------------------

def send_request(api_key, url, model, prompt):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    response = requests.post(url, headers=headers, json=data, timeout=10)
    return response.json()["choices"][0]["message"]["content"] if response.status_code == 200 else f"Error: {response.status_code}"

def send_to_llama(prompt):
    return send_request(api_keys["llama"], "https://openrouter.ai/api/v1/chat/completions", LLAMA_MODEL, prompt)

def send_to_openai(prompt):
    return send_request(api_keys["openai"], "https://api.openai.com/v1/chat/completions", OPENAI_MODEL, prompt)

# -------------------- Leaderboard --------------------

def load_leaderboard():
    return json.load(open(LEADERBOARD_FILE)) if os.path.exists(LEADERBOARD_FILE) else []

def save_leaderboard(score):
    leaderboard = sorted(load_leaderboard() + [score], reverse=True)[:5]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)

# -------------------- Chat History --------------------

def save_chat_history(history):
    if chat_history_enabled:
        encrypted = encrypt(json.dumps(history), key)
        with open(CHAT_HISTORY_FILE, "wb") as f:
            f.write(encrypted)

def load_chat_history():
    if not os.path.exists(CHAT_HISTORY_FILE):
        return []
    try:
        with open(CHAT_HISTORY_FILE, "rb") as f:
            decrypted = decrypt(f.read(), key)
            return json.loads(decrypted)
    except:
        return []

# -------------------- Minigame (Game 1 Shooter) --------------------

def launch_minigame(parent, secrets_data):
    game = tk.Toplevel(parent)
    game.overrideredirect(True)
    game.geometry("400x400+400+200")
    game.configure(bg="black")

    canvas = tk.Canvas(game, bg="black", width=400, height=400)
    canvas.pack()

    player = canvas.create_rectangle(180, 370, 220, 380, fill="lime")
    bullets, enemies = [], []
    running, score = True, 0

    def move_left(event): canvas.move(player, -20, 0)
    def move_right(event): canvas.move(player, 20, 0)

    def shoot(event):
        x1, y1, x2, y2 = canvas.coords(player)
        bullets.append(canvas.create_rectangle(x1+15, y1-10, x2-15, y1, fill="white"))

    def show_game_over(victory):
        canvas.delete("all")
        msg = "SECRET FOUND" if victory else "GAME OVER"
        submsg = f"You shot {WIN_SCORE} enemies!" if victory else "You got hit!"
        canvas.create_text(200, 150, text=msg, fill="white", font=("Courier", 24))
        canvas.create_text(200, 200, text=submsg, fill="red", font=("Courier", 18))
        canvas.update()
        time.sleep(3)
        canvas.delete("all")
        secrets_data["found"] += 1
        save_secrets(secrets_data)
        save_leaderboard(score)

        leaderboard = load_leaderboard()
        canvas.create_text(200, 40, text="HIGH SCORES", fill="red", font=("Courier", 20))
        for idx, s in enumerate(leaderboard):
            color = "lime" if idx == 0 else "white"
            canvas.create_text(200, 80 + idx * 30, text=f"{idx+1}: {s}", fill=color, font=("Courier", 16))

        tk.Button(game, text="Return to Chat", bg="lime", fg="black", command=game.destroy).pack(pady=20)

    def game_loop():
        nonlocal score, running
        while running:
            for bullet in bullets[:]:
                canvas.move(bullet, 0, -10)
                if canvas.coords(bullet)[1] < 0:
                    canvas.delete(bullet)
                    bullets.remove(bullet)

            if running and len(enemies) < MAX_ENEMIES and time.time() % 1 < 0.05:
                x = 50 + int(time.time() * 100 % 300)
                enemies.append(canvas.create_rectangle(x, 0, x+30, 20, fill="red"))

            for enemy in enemies[:]:
                canvas.move(enemy, 0, 5)
                enemy_coords = canvas.coords(enemy)
                player_coords = canvas.coords(player)

                if enemy_coords[3] >= player_coords[1] and enemy_coords[2] >= player_coords[0] and enemy_coords[0] <= player_coords[2]:
                    running = False
                    show_game_over(False)
                    return

                if enemy_coords[3] > 400:
                    canvas.delete(enemy)
                    enemies.remove(enemy)

            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if canvas.bbox(bullet) and canvas.bbox(enemy):
                        b, e = canvas.bbox(bullet), canvas.bbox(enemy)
                        if b[2] > e[0] and b[0] < e[2] and b[3] > e[1] and b[1] < e[3]:
                            canvas.delete(bullet), canvas.delete(enemy)
                            bullets.remove(bullet), enemies.remove(enemy)
                            score += 1
                            if score >= WIN_SCORE:
                                running = False
                                show_game_over(True)
                                return
                            break

            canvas.update()
            time.sleep(0.05)

    canvas.bind("<Left>", move_left)
    canvas.bind("<Right>", move_right)
    canvas.bind("<space>", shoot)
    canvas.focus_set()
    threading.Thread(target=game_loop).start()

# -------------------- UI --------------------

def create_tab(frame, send_func):
    secrets_data = load_secrets()
    chat_history = load_chat_history()

    def ask(event=None):
        prompt = input_entry.get().strip()

        # Game triggers
        if prompt == "-game2":
            bg.trigger_synapse_cave()
            return
        if prompt == "-game3":
            bg.trigger_skull_kid()
            return
        if prompt == "-congrats":
            bg.show_final_puzzle()
            return

        if "synapse" in prompt.lower():
            bg.register_synapse()

        if "python" in prompt.lower() and datetime.datetime.now().hour >= 0:
            bg.register_python(after_midnight=True)

        bg.check_completion()

        if any(word in prompt.lower() for word in ["ppi", "piiii", "synapsee"]):
            launch_minigame(root, secrets_data)

        if prompt:
            input_entry.delete(0, tk.END)
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, f"You: {prompt}\n", "user")
            output_text.config(state=tk.DISABLED)

            def run():
                for _ in range(5):
                    output_text.config(state=tk.NORMAL)
                    output_text.insert(tk.END, ".", "thinking")
                    output_text.config(state=tk.DISABLED)
                    frame.update()
                    time.sleep(0.5)

                result = send_func(prompt)
                output_text.config(state=tk.NORMAL)
                output_text.insert(tk.END, f"\nSynapse: {result}\n", "ai")
                output_text.config(state=tk.DISABLED)

                chat_history.append({"user": prompt, "ai": result})
                save_chat_history(chat_history)

            threading.Thread(target=run).start()

    output_text = tk.Text(frame, height=20, bg="#000", fg="lime", insertbackground="lime", state=tk.DISABLED, wrap=tk.WORD)
    output_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
    output_text.tag_config("user", foreground="white")
    output_text.tag_config("thinking", foreground="lime")
    output_text.tag_config("ai", foreground="lime")

    for msg in chat_history:
        output_text.config(state=tk.NORMAL)
        output_text.insert(tk.END, f"You: {msg['user']}\nSynapse: {msg['ai']}\n", "ai")
        output_text.config(state=tk.DISABLED)

    input_entry = tk.Entry(frame, bg="#2a2a2a", fg="white", insertbackground="white", font=("Arial", 12))
    input_entry.pack(padx=20, pady=10, fill=tk.X)
    input_entry.bind("<Return>", ask)

    tk.Button(frame, text="Send", command=ask, bg="lime", fg="black", font=("Arial", 12)).pack(pady=10)

# -------------------- API Key Input --------------------

def get_api_keys():
    def save_keys():
        global chat_history_enabled
        api_keys["openai"] = openai_entry.get().strip()
        api_keys["llama"] = llama_entry.get().strip()
        chat_history_enabled = save_var.get() == 1
        if chat_history_enabled:
            save_config(api_keys, key)
        popup.destroy()

    saved = load_config(key)
    popup = tk.Tk()
    popup.title("Enter API Keys")
    popup.geometry("400x300")
    tk.Label(popup, text="OpenAI API Key").pack(pady=5)
    openai_entry = tk.Entry(popup, width=40)
    openai_entry.pack(pady=5)
    openai_entry.insert(0, saved.get("openai", ""))
    tk.Label(popup, text="Llama API Key").pack(pady=5)
    llama_entry = tk.Entry(popup, width=40)
    llama_entry.pack(pady=5)
    llama_entry.insert(0, saved.get("llama", ""))
    save_var = tk.IntVar()
    tk.Checkbutton(popup, text="Encrypt keys + chat history", variable=save_var).pack(pady=10)
    tk.Button(popup, text="Save", command=save_keys).pack(pady=20)
    popup.mainloop()

get_api_keys()

# -------------------- MAIN --------------------

root = tk.Tk()
root.title("Synapse Pi")
root.geometry("600x700")
root.configure(bg="black")

tabControl = ttk.Notebook(root)
llama_tab = ttk.Frame(tabControl)
openai_tab = ttk.Frame(tabControl)
tabControl.add(llama_tab, text="Meta Llama")
tabControl.add(openai_tab, text="OpenAI")
tabControl.pack(expand=1, fill="both")

create_tab(llama_tab, send_to_llama)
create_tab(openai_tab, send_to_openai)

root.mainloop()
