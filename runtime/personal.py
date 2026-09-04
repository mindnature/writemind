from __future__ import annotations
from datetime import datetime, timezone
import hashlib
from pathlib import Path
from .core import dump_json, load_json, personal_dir
from .policy import ROOT, load_policy


def init_personal_profile(name: str, slug: str, root: Path = ROOT) -> Path:
    base = personal_dir(slug, root)
    if base.exists():
        raise FileExistsError(f"personal profile already exists: {slug}")
    (base / "revision_episodes").mkdir(parents=True)
    (base / "generated").mkdir(parents=True)
    dump_json(base / "style_profile.json", {
        "profile_id": slug,
        "name": name,
        "version": "0.2",
        "platform_profiles": {},
        "voice_dna": {"preferred": [], "avoid": [], "confidence": "bootstrap"},
        "structural_dna": {"preferred": [], "avoid": [], "confidence": "bootstrap"},
        "revision_dna": {"frequent_deletions": [], "frequent_additions": [], "frequent_reorders": [], "confidence": "bootstrap"},
        "taste_dna": {"quality_signals": [], "rejection_signals": [], "confidence": "bootstrap"},
        "personal_heuristics": [],
        "evidence": {"accepted_articles": 0, "revision_episodes": 0, "explicit_feedback_events": 0}
    })
    return base


def _rule_key(rule: str) -> str:
    normalized = " ".join(rule.lower().split())
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:10]


def _promote_personal_rules(profile: dict, episode: dict, root: Path) -> None:
    policy = load_policy(root).get("personal_learning", {})
    thresholds = {
        "candidate": int(policy.get("candidate_after", 1)),
        "provisional": int(policy.get("provisional_after", 2)),
        "validated": int(policy.get("validated_after", 3)),
    }
    heuristics = profile.setdefault("personal_heuristics", [])
    by_key = {h.get("key"): h for h in heuristics}
    for rule in episode.get("candidate_personal_rules", []):
        rule = str(rule).strip()
        if not rule:
            continue
        key = _rule_key(rule)
        h = by_key.get(key)
        if h is None:
            h = {
                "id": f"PERS-{key.upper()}",
                "key": key,
                "name": rule[:60],
                "rule": rule,
                "confidence": "candidate",
                "evidence_count": 0,
                "supporting_revision_episodes": []
            }
            heuristics.append(h)
            by_key[key] = h
        if episode["episode_id"] not in h["supporting_revision_episodes"]:
            h["supporting_revision_episodes"].append(episode["episode_id"])
            h["evidence_count"] += 1
        count = h["evidence_count"]
        if count >= thresholds["validated"]:
            h["confidence"] = "validated"
        elif count >= thresholds["provisional"]:
            h["confidence"] = "provisional"
        else:
            h["confidence"] = "candidate"


def record_revision(slug: str, payload: dict, root: Path = ROOT) -> Path:
    base = personal_dir(slug, root)
    profile_path = base / "style_profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"personal profile not found: {slug}")
    required = ["context", "original_text", "final_text", "user_feedback"]
    missing = [key for key in required if not payload.get(key)]
    if missing:
        raise ValueError("revision episode missing: " + ", ".join(missing))
    policy = load_policy(root).get("personal_learning", {})
    if policy.get("require_explicit_feedback", True) and not str(payload.get("user_feedback", "")).strip():
        raise ValueError("explicit user_feedback is required for personal learning")
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%S%fZ")
    episode_id = payload.get("episode_id") or f"REV-{stamp}"
    episode = {
        "episode_id": episode_id,
        "recorded_at": now.isoformat(),
        "context": payload["context"],
        "platform": payload.get("platform", "unknown"),
        "task": payload.get("task", "revision"),
        "original_text": payload["original_text"],
        "advisor_suggestion": payload.get("advisor_suggestion", ""),
        "user_final_text": payload["final_text"],
        "accepted_changes": payload.get("accepted_changes", []),
        "rejected_changes": payload.get("rejected_changes", []),
        "user_feedback": payload["user_feedback"],
        "candidate_personal_rules": payload.get("candidate_personal_rules", []),
        "writer_lenses_used": payload.get("writer_lenses_used", []),
        "confidence": payload.get("confidence", "candidate")
    }
    path = base / "revision_episodes" / f"{episode_id}.json"
    if path.exists():
        raise FileExistsError(f"revision episode already exists: {episode_id}")
    dump_json(path, episode)
    profile = load_json(profile_path)
    profile.setdefault("evidence", {})["revision_episodes"] = len(list((base / "revision_episodes").glob("*.json")))
    profile["evidence"]["explicit_feedback_events"] = profile["evidence"].get("explicit_feedback_events", 0) + 1
    _promote_personal_rules(profile, episode, root)
    dump_json(profile_path, profile)
    return path


def validate_personal_profile(slug: str, root: Path = ROOT) -> list[str]:
    base = personal_dir(slug, root)
    profile_path = base / "style_profile.json"
    if not profile_path.exists():
        return ["missing style_profile.json"]
    profile = load_json(profile_path)
    errors = []
    for key in ("voice_dna", "structural_dna", "revision_dna", "taste_dna", "personal_heuristics", "evidence"):
        if key not in profile:
            errors.append(f"style_profile.json: missing {key}")
    episode_ids = {p.stem for p in (base / "revision_episodes").glob("*.json")}
    for h in profile.get("personal_heuristics", []):
        for eid in h.get("supporting_revision_episodes", []):
            if eid not in episode_ids:
                errors.append(f"{h.get('id', 'personal heuristic')}: broken revision episode ref {eid}")
    return errors


def build_personal_skill(slug: str, root: Path = ROOT, output: Path | None = None) -> Path:
    base = personal_dir(slug, root)
    profile = load_json(base / "style_profile.json")
    output = output or (base / "generated" / "SKILL.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        f"name: writemind-personal-{slug}",
        f'description: "Personal writing profile and revision coach for {profile["name"]}. Use explicit writing samples and revision history; do not invent preferences."',
        "---",
        "",
        f"# {profile['name']} · Personal Writing Profile",
        "",
        "Current explicit user instruction overrides every stored preference. When new feedback conflicts with an older inferred preference, record the conflict as a new Revision Episode instead of silently forcing the old style.",
        "",
    ]
    for key, title in [("voice_dna", "Voice DNA"), ("structural_dna", "Structural DNA"), ("revision_dna", "Revision DNA"), ("taste_dna", "Taste DNA")]:
        data = profile.get(key, {})
        lines += [f"## {title}", ""]
        for subkey, value in data.items():
            if subkey == "confidence":
                continue
            lines += [f"### {subkey}", ""]
            if isinstance(value, list):
                if value:
                    lines.extend(f"- {x}" for x in value)
                else:
                    lines.append("- No validated preference yet.")
            else:
                lines.append(str(value))
            lines.append("")
    lines += ["## Personal heuristics", ""]
    heuristics = profile.get("personal_heuristics", [])
    if heuristics:
        for h in heuristics:
            lines += [
                f"### {h.get('id', 'PERSONAL')} · {h.get('name', '')}",
                "",
                h.get("rule", ""),
                "",
                f"Confidence: `{h.get('confidence', 'candidate')}` · Evidence: {h.get('evidence_count', 0)} Revision Episodes",
                "",
                "Supporting episodes: " + ", ".join(f"`{x}`" for x in h.get("supporting_revision_episodes", [])),
                "",
            ]
    else:
        lines += ["No validated personal heuristic yet. Continue collecting Revision Episodes.", ""]
    lines += [
        "## Coach rule",
        "",
        "Do not merely rewrite. Explain one highest-leverage issue, show one limited example, compare the user's revision when available, and record accepted/rejected changes as evidence. Never infer acceptance from silence.",
        "",
    ]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
