# Env Aware Relational Memory (Demo)

A tiny, reproducible demo showing how a **relational interpretive layer** can maintain
a lightweight, decaying memory of the **machine environment** (e.g., Windows, PowerShell,
Pandoc installed) and **change behavior accordingly**.

This is a self-contained subset of the ANGEL interpretive layer intended for engineers
who want a concrete, testable example.

## What it shows
- Token-weighted **environment state** with exponential decay
- A simple **policy** that decides the next action:
  - If Windows + PowerShell + Pandoc are believed present → provide direct Pandoc command
  - If PowerShell but Pandoc uncertain → suggest install command
  - Otherwise → ask a single clarifying question

## Files
- `env_state_controller.py` — environment tracker + policy
- `demo_env_awareness.py` — runs a short simulation and writes a CSV of learned weights
- `.gitignore`, `LICENSE`, `requirements.txt` — housekeeping

## Quick start (Windows / PowerShell)
```powershell
# 1) (Optional) Create and activate a venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) (No external deps needed, but keep this for consistency)
pip install -r requirements.txt

# 3) Run the demo
python .\demo_env_awareness.py
```
## Quick start (Linux)

## Quick Start (MacOS)

You should see output similar to:
```json
{
  "env_state": {
    "Windows": 0.7,
    "PowerShell": 1.23,
    "PandocInstalled": 0.8,
    "PDFExportSuccess": 0.8
  },
  "policy_decision": {
    "assumption": "Windows + PowerShell + Pandoc present",
    "action": "Provide direct conversion command",
    "command": "pandoc \"C:\\Users\\<you>\\ANGEL_ML\\ANGEL.AI_Business\\ANGEL_System_Brief.md\" -o \"...\" --pdf-engine=xelatex"
  }
}
```

A CSV artifact like `env_awareness_log_YYYYMMDD_HHMMSS.csv` will be written in the repo
root with the learned token weights.

## Why this matters
This demonstrates **persistent, decaying relational state** driving **context-aware behavior**
without retraining any model — exactly the interpretive layer’s job in a small, verifiable unit.

## License
MIT © 2025 Robin Macomber
