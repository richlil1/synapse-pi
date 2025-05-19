import json
import os
import random
import time
import tkinter as tk
import threading
from PIL import Image, ImageTk  # For rotating Synapse image and resizing

STATE_FILE = ".user_metrics.json"

# Load or initialize state
if os.path.exists(STATE_FILE):
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
else:
    state = {"eggs_found": [], "synapse_mentions": 0, "python_mentions": 0, "unlocked_final": False}

def save_state():
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# -------------------- Game 2 --------------------

def trigger_synapse_cave():
    game = tk.Toplevel()
    game.geometry("400x400+400+200")
    game.configure(bg="#d8c6c6")
    canvas = tk.Canvas(game, bg="#d8c6c6", width=400, height=400)
    canvas.pack()

    canvas.create_text(200, 50, text="You found the Synapse Cave!", fill="black", font=("Courier", 16))

    tunnels = ["Left Tunnel", "Center Tunnel", "Right Tunnel"]
    correct_tunnel = random.choice(tunnels)

    def start_battle():
        game.destroy()
        synapse_battle()

    def choose(tunnel):
        canvas.delete("all")
        if tunnel == correct_tunnel:
            canvas.create_text(200, 200, text="A Wild MALWARE Appeared!", fill="black", font=("Courier", 14))
            state["eggs_found"].append("synapse_cave_found")
            state["eggs_found"].append("synapse_battle_won")
            save_state()
            canvas.update()
            time.sleep(2)
            start_battle()
        else:
            state["eggs_found"].append("synapse_cave_gameover")
            save_state()
            canvas.create_text(200, 200, text="GAME OVER", fill="red", font=("Courier", 18))
            canvas.update()
            time.sleep(3)
            game.destroy()

    for i, tunnel in enumerate(tunnels):
        btn = tk.Button(game, text=tunnel, command=lambda t=tunnel: choose(t), bg="gray", fg="black")
        canvas.create_window(200, 150 + (i * 50), window=btn)

    game.mainloop()

# -------------------- Synapse Battle --------------------

def synapse_battle():
    battle = tk.Toplevel()
    battle.geometry("800x600+400+200")
    battle.configure(bg="#e8dcdc")

    canvas = tk.Canvas(battle, bg="#e8dcdc", width=800, height=600)
    canvas.pack(fill=tk.BOTH, expand=True)

    assets_path = "assets/"
    bg_img = tk.PhotoImage(file=os.path.join(assets_path, "synapseokemonBG.PNG"))
    malware_img_path = os.path.join(assets_path, "malwareBG.png")
    player_img = tk.PhotoImage(file=os.path.join(assets_path, "anon.png"))

    # Resize malware image to match anon size
    def load_and_resize(path, size=(500, 250)):
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    malware_img = load_and_resize(malware_img_path, (500, 250))

    canvas.create_image(0, 0, image=bg_img, anchor="nw")

    synapse = canvas.create_image(700, 100, image=malware_img, anchor="nw")
    player = canvas.create_image(-200, 400, image=player_img, anchor="nw")

    for x in range(-200, 100, 10):
        canvas.coords(player, x, 400)
        canvas.update()
        time.sleep(0.05)

    canvas.create_text(400, 40, text="Malware appeared!", fill="black", font=("Courier", 20))

    synapse_hp = 20
    synapse_bar = canvas.create_rectangle(700, 70, 700 + synapse_hp * 5, 90, fill="green")
    battle_text = canvas.create_text(400, 550, text="You attack!", fill="black", font=("Courier", 16))

    def rotate_image(image_path, size=(500, 250)):
        img = Image.open(image_path).resize(size, Image.Resampling.LANCZOS)
        rotated = img.rotate(90, expand=True)
        return ImageTk.PhotoImage(rotated)

    def attack():
        nonlocal synapse_hp
        while synapse_hp > 0:
            synapse_hp -= 1
            canvas.coords(synapse_bar, 700, 70, 700 + synapse_hp * 5, 90)
            canvas.update()
            time.sleep(0.2)

        canvas.itemconfig(battle_text, text="Malware defeated!")
        canvas.update()
        time.sleep(1)

        for i in range(10):
            canvas.move(synapse, 3, 6)
            canvas.update()
            time.sleep(0.05)

        rotated_img = rotate_image(malware_img_path, (250, 500))
        canvas.itemconfig(synapse, image=rotated_img)
        canvas.update()
        time.sleep(2)

        canvas.itemconfig(synapse, state="hidden")
        canvas.create_text(400, 300, text="", fill="black", font=("Courier", 16))

        state["eggs_found"].append("synapse_battle_win")
        save_state()
        time.sleep(3)
        battle.destroy()

        # ---------> NEW: Show how many eggs they have found
        show_egg_progress()

    threading.Thread(target=attack, daemon=True).start()
    battle.mainloop()

# -------------------- Easter Egg Progress --------------------

def show_egg_progress():
    progress = tk.Toplevel()
    progress.geometry("400x300+500+300")
    progress.configure(bg="black")

    canvas = tk.Canvas(progress, bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    eggs_found = len(set(state["eggs_found"]))

    canvas.create_text(200, 100, text=f"You have found {eggs_found}/7 Easter Eggs!", fill="lime", font=("Courier", 18))
    canvas.create_text(200, 180, text="Keep going to find them all!", fill="white", font=("Courier", 12))

    def close():
        progress.destroy()

    canvas.create_text(200, 250, text="(Click to continue)", fill="gray", font=("Courier", 10))
    progress.bind("<Button-1>", lambda e: close())

    progress.mainloop()

# -------------------- Final Puzzle --------------------

def show_final_puzzle():
    game = tk.Toplevel()
    game.geometry("600x600+400+200")
    game.configure(bg="black")
    game.resizable(True, True)

    canvas = tk.Canvas(game, bg="black")
    canvas.pack(fill=tk.BOTH, expand=True)

    def blink():
        while True:
            canvas.itemconfig(congrats, fill="lime")
            canvas.update()
            time.sleep(0.5)
            canvas.itemconfig(congrats, fill="black")
            canvas.update()
            time.sleep(0.5)

    congrats = canvas.create_text(300, 50, text="CONGRATULATIONS !!!", fill="lime", font=("Courier", 24))
    threading.Thread(target=blink, daemon=True).start()

    puzzle = """
  7/7 EASTER EGGS FOUND!

==========================
XGBF AE XMR QSO VIHHUI
WLHNTMZG MX RLCI PGG

URQF ZNGR FGEVHZ
ZNT VPY HVR N JBEYQ VAF
==========================
    """

    canvas.create_text(300, 300, text=puzzle, fill="white", font=("Courier", 14), justify="center")
    game.mainloop()

# -------------------- Game 3 --------------------

def trigger_skull_kid():
    game = tk.Toplevel()
    game.geometry("900x600+400+200")
    game.configure(bg="black")

    canvas = tk.Canvas(game, bg="black", width=900, height=600, scrollregion=(0, 0, 1500, 600))
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(game, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.config(xscrollcommand=scrollbar.set)

    canvas.create_text(450, 30, text="ANONYMOUS SKULL KID", fill="lime", font=("Courier", 16))

    assets_path = "assets/"
    player_img = tk.PhotoImage(file=os.path.join(assets_path, "anon.png"))
    fire_img = tk.PhotoImage(file=os.path.join(assets_path, "fire.png"))
    fish_img = tk.PhotoImage(file=os.path.join(assets_path, "fisht.png"))

    player = canvas.create_image(50, 350, image=player_img, anchor="nw")

    blocks = [
        {"name": "FIREWALL", "x": 600, "health": 5, "broken": False, "img": fire_img, "id": None},
        {"name": "PHISH TANK", "x": 1100, "health": 5, "broken": False, "img": fish_img, "id": None},
    ]

    for block in blocks:
        block["id"] = canvas.create_image(block["x"], 350, image=block["img"], anchor="nw")

    player_speed = 10
    is_cutting = False

    def animate_cut(block):
        for _ in range(3):
            canvas.itemconfig(block["id"], image="")
            canvas.update()
            time.sleep(0.1)
            canvas.itemconfig(block["id"], image=block["img"])
            canvas.update()
            time.sleep(0.1)

    def move(event):
        if event.keysym in ["Right", "d", "D"]:
            canvas.move(player, player_speed, 0)

    def cut():
        while True:
            if is_cutting:
                px, py = canvas.coords(player)
                for block in blocks:
                    if not block["broken"]:
                        bx = block["x"]
                        if px + 100 >= bx and px <= bx + 100:
                            block["health"] -= 1
                            animate_cut(block)

                            if block["health"] <= 0:
                                block["broken"] = True
                                canvas.itemconfig(block["id"], state="hidden")
                                canvas.create_text(bx + 50, 330, text=f"{block['name']} DESTROYED!", fill="white", font=("Courier", 12))

                if all(b["broken"] for b in blocks):
                    state["eggs_found"].append("skull_trigger")
                    state["eggs_found"].append("skull_win")
                    save_state()
                    canvas.create_text(750, 250, text="ALL CLEARED → SECRET FOUND!", fill="lime", font=("Courier", 18))
                    canvas.update()
                    time.sleep(3)
                    game.destroy()
                    show_final_puzzle()
                    return

            canvas.update()
            time.sleep(0.3)

    def cut_start(event):
        nonlocal is_cutting
        is_cutting = True

    def cut_end(event):
        nonlocal is_cutting
        is_cutting = False

    game.bind("<Right>", move)
    game.bind("<d>", move)
    game.bind("<D>", move)
    game.bind("<space>", cut_start)
    game.bind("<KeyRelease-space>", cut_end)

    threading.Thread(target=cut, daemon=True).start()
    game.mainloop()

# -------------------- Triggers --------------------

def register_synapse():
    state["synapse_mentions"] += 1
    save_state()
    if state["synapse_mentions"] == 7:
        trigger_synapse_cave()

def register_python(after_midnight):
    state["python_mentions"] += 1
    save_state()
    if after_midnight and state["python_mentions"] == 6:
        trigger_skull_kid()

def check_completion():
    if len(set(state["eggs_found"])) >= 7 and not state["unlocked_final"]:
        state["unlocked_final"] = True
        save_state()
        show_final_puzzle()
