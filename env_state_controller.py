
"""
Environment-aware extension for ANGEL Relational Layer.

Drop this file into: relational_layer/env_state_controller.py

It augments the RelationalMemorySystem with a simple "environment channel"
that tracks machine/tooling tokens (e.g., Windows, PowerShell, Pandoc) and
demonstrates policy decisions (e.g., generate a Pandoc command vs. suggest install).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
import math
import json

# Local import in your repo context would be:
# from .relational_token_memory import RelationalMemorySystem, TokenMemory

# For stand-alone testing without package imports, we include a minimal shim.
class _TokenMemoryShim:
    def __init__(self, name, decay=0.95):
        self.name = name
        self.decay = decay
        self.token_weights: Dict[str, float] = {}

    def update_weights(self, tokens: List[str], intensity: float):
        for t in tokens:
            prev = self.token_weights.get(t, 0.0)
            self.token_weights[t] = prev * self.decay + intensity

    def decay_weights(self):
        for t in list(self.token_weights.keys()):
            self.token_weights[t] *= self.decay
            if self.token_weights[t] < 1e-6:
                del self.token_weights[t]

    def get_weights(self) -> Dict[str, float]:
        return dict(self.token_weights)


class EnvironmentStateTracker:
    """
    Tracks environment/tooling cues as a token-weighted state with decay.
    Examples: 'Windows', 'PowerShell', 'PandocInstalled', 'LaTeX', 'GitCLI'.
    """

    def __init__(self, decay: float = 0.95, threshold: float = 0.6):
        self.mem = _TokenMemoryShim("Env", decay=decay)
        self.threshold = threshold

    def observe(self, tokens: List[str], intensity: float = 1.0):
        """
        Add observations that imply environment state.
        Example: ["Windows", "PowerShell", "PandocInstalled"]
        """
        self.mem.update_weights(tokens, intensity)

    def hypothesis(self, key: str) -> bool:
        """
        True if weighted belief about `key` exceeds threshold.
        """
        return self.mem.get_weights().get(key, 0.0) >= self.threshold

    def to_json(self) -> str:
        return json.dumps(self.mem.get_weights(), indent=2)


@dataclass
class RelationalController:
    """
    Simple policy that uses (a) user/ai drift and (b) environment hypotheses
    to choose the next action template.
    """
    env: EnvironmentStateTracker = field(default_factory=lambda: EnvironmentStateTracker(decay=0.95, threshold=0.6))

    def policy_for_pdf_request(self, brief_path_md: str, engine: str = "xelatex") -> Dict[str, str]:
        """
        Decide how to respond to: "Convert this MD to PDF" given environment state.
        Returns a dict with keys: 'assumption', 'action', 'command'
        """
        has_windows = self.env.hypothesis("Windows")
        has_pwsh   = self.env.hypothesis("PowerShell")
        has_pandoc = self.env.hypothesis("PandocInstalled")

        # Build a context-aware command if we *believe* the user has the tools.
        if has_windows and has_pwsh and has_pandoc:
            cmd = f'pandoc "{brief_path_md}" -o "{brief_path_md[:-3]}.pdf" --pdf-engine={engine}'
            return {
                "assumption": "Windows + PowerShell + Pandoc present",
                "action": "Provide direct conversion command",
                "command": cmd
            }
        elif has_windows and has_pwsh and not has_pandoc:
            return {
                "assumption": "Windows + PowerShell; Pandoc uncertain",
                "action": "Offer install path then conversion command",
                "command": 'winget install Pandoc.Pandoc'
            }
        else:
            return {
                "assumption": "Environment uncertain",
                "action": "Ask one clarifying question to establish environment",
                "command": "Do you have Pandoc installed and can you run PowerShell on Windows?"
            }


# Demo runner
def demo_environment_awareness():
    env = EnvironmentStateTracker(decay=0.9, threshold=0.6)
    ctrl = RelationalController(env=env)

    # Simulate a few interactions that imply environment state
    # Turn 1: mention Windows and PowerShell
    env.observe(["Windows", "PowerShell"], intensity=0.7)
    # Turn 2: successful PDF conversion in the past (implies Pandoc present)
    env.observe(["PandocInstalled", "PDFExportSuccess"], intensity=0.8)
    # Turn 3: repeated use of PowerShell
    env.observe(["PowerShell"], intensity=0.6)

    decision = ctrl.policy_for_pdf_request(r"C:\Users\Robin_B_Macomber\ANGEL_ML\ANGEL.AI_Business\ANGEL_System_Brief.md")
    return {
        "env_state": json.loads(env.to_json()),
        "policy_decision": decision
    }


if __name__ == "__main__":
    out = demo_environment_awareness()
    print(json.dumps(out, indent=2))
