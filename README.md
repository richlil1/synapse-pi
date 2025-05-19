# Synapse-Pi — Your Lightweight AI Terminal on Raspberry Pi

**Synapse-Pi** is a lightweight, Python-based AI assistant designed specifically for Raspberry Pi devices. It runs directly from your terminal, bootstraps on startup, and leverages powerful LLMs (like OpenAI or Meta’s LLaMA) for local assistant-style interactions — without the need for a browser or UI.

Whether you're using it as a personal command-line assistant, an automation engine, or an educational project, Synapse-Pi is a modular, expandable foundation for AI on the edge.

---

## Features

* Fully terminal-based, no GUI required
* Lightweight and resource-conscious
* Integrates OpenAI or LLaMA via API for responses
* Includes encrypted memory, local logs, and task tools
* Modular file structure (UI, utils, background processes, secrets, config)

---

## Use Cases

* Terminal-based AI assistant for Raspberry Pi
* Educational AI + Python project
* Smart home controller or interface
* Local server command execution via AI

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/richlil1/synapse-pi.git
cd synapse-pi
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create Your `.env` File

Create a `.env` file in the root directory:

```bash
touch .env
```

Paste this inside:

```
OPENAI_API_KEY=your-openai-api-key
```

---

### 4. Run the App

```bash
python synapse.py
```

---

## Directory Structure

```
synapse-pi/
│
├── assets/                  # Images and visual assets
├── background_processes.py  # Optional modules (e.g. metrics, uptime)
├── config.json              # Runtime config
├── key.key                  # Encryption key (generated automatically)
├── leaderboard.json         # Usage tracking / gamified metrics
├── synapse.py               # Main entry script
├── ui.py                    # Terminal interface logic
├── utils.py                 # Helper functions and logic
├── .env                     # Your API keys
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Future Plans

* Voice command integration
* Local model fallback (offline AI)
* GUI interface with touch/mouse support

---

## License

This project is open source under the MIT License.
See the [LICENSE](./LICENSE) file for full terms.

---

## Contributing

Pull requests and forks are welcome. If you'd like to suggest features or contribute, open an issue or create a branch.

To contribute formally, please read the [CONTRIBUTING.md](./CONTRIBUTING.md) file (if available).
