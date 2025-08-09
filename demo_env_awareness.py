
"""
Run a minimal environment-awareness demo.

Usage (after placing env_state_controller.py into your repo's relational_layer/):
> python demo_env_awareness.py
"""

import json
import csv
from datetime import datetime

# Local import if placed under relational_layer:
# from relational_layer.env_state_controller import demo_environment_awareness
# For stand-alone run from this folder, we import the local file:
from env_state_controller import demo_environment_awareness  # type: ignore

def main():
    result = demo_environment_awareness()
    print(json.dumps(result, indent=2))

    # Also write a simple CSV log the engineer can inspect
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"env_awareness_log_{timestamp}.csv"
    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "weight"])
        for k, v in result["env_state"].items():
            w.writerow([k, v])
    print(f"Wrote {csv_path}")

if __name__ == "__main__":
    main()
