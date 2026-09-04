from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_policy(root: Path = ROOT) -> dict:
    return json.loads((root / "config" / "policy.json").read_text(encoding="utf-8"))


def transfer_action(confidence: str, root: Path = ROOT) -> str:
    policy = load_policy(root)
    try:
        return policy["transfer_policy"][confidence]
    except KeyError as exc:
        raise ValueError(f"unknown transfer confidence: {confidence}") from exc
