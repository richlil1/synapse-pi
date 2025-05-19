import tkinter as tk
import threading
import time
import random
import utils

SECRET_WORDS = ["ppi", "piiii", "synapsee"]

def check_for_secret(prompt):
    for word in SECRET_WORDS:
        if word in prompt.lower():
            return True
    return False

def show_secret_found(window):
    count = utils.secrets_found_count()
    popup = tk.Toplevel(window)
    popup.geometry("300x100")
    popup.configure(bg="black")
    tk.Label(popup, text=f"You found secret #{count + 1}!", 
             fg="lime", 
             bg="black", 
             font=("Arial", 16)).pack(expand=True)
    popup.after(3000, popup.destroy)

def launch_minigame(window):
    utils.mark_secret_found("minigame")
    show_secret_found(window)

    game = tk.Toplevel(window)
    game.title("Secret Game")
    game.geometry("400x400")
    game.configure(bg="black")

    player = tk.Label(game, text="▲", fg="lime", bg="black", font=("Arial", 24))
    player.place(x=200, y=350)

    enemies = []

    def spawn_enemy():
        while True:
            x = random.randint(10, 380)
            enemy = tk.Label(game, text="●", fg="red", bg="black", font=("Arial", 14))
            enemy.place(x=x, y=0)
            enemies.append(enemy)
            time.sleep(2)

    def move_enemies():
        while True:
            for e in enemies:
                e.place_configure(y=e.winfo_y() + 5)
                if e.winfo_y() > 400:
                    enemies.remove(e)
                    e.destroy()
            game.update()
            time.sleep(0.05)

    threading.Thread(target=spawn_enemy, daemon=True).start()
    threading.Thread(target=move_enemies, daemon=True).start()

    game.bind("<Left>", lambda e: player.place_configure(x=player.winfo_x() - 10))
    game.bind("<Right>", lambda e: player.place_configure(x=player.winfo_x() + 10))
    game.focus_set()

def handle_prompt(prompt, window):
    if check_for_secret(prompt):
        launch_minigame(window)
        return True
    return False
