from __future__ import annotations
from pathlib import Path
from .core import load_json, writer_dir
from .policy import ROOT, load_policy


def validate_writer(slug: str, root: Path = ROOT) -> list[str]:
    base = writer_dir(slug, root)
    errors: list[str] = []
    for required in ("writer_profile.json", "source_registry.json"):
        if not (base / required).exists():
            errors.append(f"missing {required}")
    if errors:
        return errors
    registry = load_json(base / "source_registry.json")
    source_ids = {s.get("source_id") for s in registry.get("sources", [])}
    episodes = {}
    for path in (base / "episodes").glob("*.json"):
        ep = load_json(path)
        eid = ep.get("episode_id")
        if not eid:
            errors.append(f"{path.name}: missing episode_id")
            continue
        episodes[eid] = ep
        for ref in ep.get("source_refs", []):
            if ref not in source_ids:
                errors.append(f"{path.name}: broken source ref {ref}")
    policy = load_policy(root)
    minimum = policy["active_lens_provenance"]["minimum_supporting_episodes"]
    for path in (base / "heuristics").glob("*.json"):
        h = load_json(path)
        hid = h.get("heuristic_id", path.name)
        support = h.get("supporting_episodes", [])
        for eid in support:
            if eid not in episodes:
                errors.append(f"{path.name}: broken episode ref {eid}")
        eligibility = h.get("routing", {}).get("lens_eligibility")
        if eligibility == "active_lens":
            if len(support) < minimum:
                errors.append(f"{hid}: active_lens needs >= {minimum} supporting episodes")
            if not h.get("specificity", {}).get("writer_added_delta", "").strip():
                errors.append(f"{hid}: active_lens missing writer_added_delta")
            if h.get("composition_audit", {}).get("fabrication_risk") in {None, "high", "unknown"}:
                errors.append(f"{hid}: active_lens composition audit insufficient")
    return errors
