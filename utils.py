import json
import os
from cryptography.fernet import Fernet

CONFIG_FILE = ".config_data.json"          # Hidden config file (encrypted API keys)
SECRETS_FILE = ".user_secrets.json"        # Hidden file (for secret/minigame progress)

# -------------------- Key Generation and Management --------------------

def generate_key():
    return Fernet.generate_key()

def load_key():
    if os.path.exists("key.key"):
        return open("key.key", "rb").read()
    return None

def save_key(key):
    with open("key.key", "wb") as f:
        f.write(key)

# -------------------- Encryption + Decryption --------------------

def encrypt(data, key):
    return Fernet(key).encrypt(data.encode())

def decrypt(data, key):
    return Fernet(key).decrypt(data).decode()

# -------------------- API Config Save + Load (Encrypted) --------------------

def save_config(api_keys, key):
    data = {
        "openai": encrypt(api_keys.get("openai", ""), key).decode(),
        "llama": encrypt(api_keys.get("llama", ""), key).decode()
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

def load_config(key):
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        return {
            "openai": decrypt(data.get("openai", ""), key),
            "llama": decrypt(data.get("llama", ""), key)
        }

# -------------------- Secrets / Minigame Progress Save + Load --------------------

def load_secrets():
    if not os.path.exists(SECRETS_FILE):
        return {"found": 0}
    with open(SECRETS_FILE, "r") as f:
        return json.load(f)

def save_secrets(data):
    with open(SECRETS_FILE, "w") as f:
        json.dump(data, f)
