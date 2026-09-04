from __future__ import annotations
from pathlib import Path
from .policy import ROOT, load_policy

DIMS = ("genre_fit", "decision_structure_fit", "evidence_fit", "added_value_fit")


def evaluate_task_fit(assessment: dict, root: Path = ROOT) -> dict:
    policy = load_policy(root)["writer_task_fit"]
    scores = assessment.get("scores", assessment)
    normalized = {}
    for key in DIMS:
        if key not in scores:
            raise ValueError(f"missing task-fit score: {key}")
        value = float(scores[key])
        if not 0 <= value <= 100:
            raise ValueError(f"{key} must be 0..100")
        normalized[key] = value
    total = sum(normalized[k] * policy["weights"][k] for k in DIMS)
    thresholds = policy["thresholds"]
    activation = "active" if total >= thresholds["active"] else "experimental" if total >= thresholds["experimental"] else "abstain"
    cross = policy.get("cross_genre_rule", {})
    if normalized["genre_fit"] < cross.get("genre_fit_below", -1) and normalized["decision_structure_fit"] < cross.get("unless_decision_structure_fit_at_least", 101):
        if activation == "active":
            activation = cross.get("maximum_activation", "experimental")
    return {"scores": normalized, "weighted_score": round(total, 2), "activation": activation}
