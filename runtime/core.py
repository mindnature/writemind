from __future__ import annotations
import json
import re
from pathlib import Path
from .policy import ROOT


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def simple_slug(name: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    if not slug:
        raise ValueError("non-Latin names require --slug")
    return slug


def writer_dir(slug: str, root: Path = ROOT) -> Path:
    return root / "data" / slug


def personal_dir(slug: str, root: Path = ROOT) -> Path:
    return root / "personal" / slug


def init_writer(name: str, slug: str | None = None, root: Path = ROOT) -> Path:
    slug = slug or simple_slug(name)
    base = writer_dir(slug, root)
    if base.exists():
        raise FileExistsError(f"writer already exists: {slug}")
    (base / "episodes").mkdir(parents=True)
    (base / "heuristics").mkdir(parents=True)
    dump_json(base / "writer_profile.json", {
        "writer_id": slug,
        "name": name,
        "slug": slug,
        "aliases": [],
        "languages": [],
        "period": "",
        "genres": [],
        "source_ceiling": "D",
        "distillation_grade": "D_textual_reconstruction",
        "unsafe_to_claim": ["Do not impersonate the writer."]
    })
    dump_json(base / "source_registry.json", {"writer": name, "sources": []})
    return base


def discover_writers(root: Path = ROOT) -> list[str]:
    data = root / "data"
    if not data.exists():
        return []
    return sorted(p.name for p in data.iterdir() if p.is_dir() and (p / "writer_profile.json").exists())


def _render_list(lines: list[str], title: str, items: list[str]) -> None:
    if not items:
        return
    lines += [f"### {title}", ""]
    for item in items:
        lines.append(f"- {item}")
    lines.append("")


def _render_heuristic(lines: list[str], h: dict) -> None:
    lines += [f"## {h['heuristic_id']} · {h['name']}", "", f"Lens family: `{h.get('lens_family', 'unknown')}`", "", f"Eligibility: `{h.get('routing', {}).get('lens_eligibility', 'unknown')}`", ""]
    if h.get("decision_structure"):
        lines += ["### Decision structure", "", h["decision_structure"], ""]
    lines += ["### Rule", "", h.get("rule", ""), ""]
    _render_list(lines, "Operational actions", h.get("operational_actions", []))
    _render_list(lines, "Diagnostic questions", h.get("diagnostic_questions", []))
    _render_list(lines, "Boundary conditions", h.get("boundary_conditions", []))
    _render_list(lines, "Failure signals", h.get("failure_signals", []))
    specificity = h.get("specificity", {})
    if specificity:
        lines += ["### Writer-added delta", "", specificity.get("writer_added_delta", "Not specified."), ""]
    support = h.get("supporting_episodes", [])
    if support:
        lines += ["### Provenance", "", "Supporting Episodes: " + ", ".join(f"`{x}`" for x in support), ""]
    audit = h.get("composition_audit", {})
    if audit:
        lines += ["### Composition audit", "", f"Fabrication risk: `{audit.get('fabrication_risk', 'unknown')}`", ""]
        if audit.get("alternative_interpretation"):
            lines += [audit["alternative_interpretation"], ""]


def build_skill(slug: str, root: Path = ROOT, output: Path | None = None) -> Path:
    base = writer_dir(slug, root)
    profile = load_json(base / "writer_profile.json")
    heuristics = []
    for path in sorted((base / "heuristics").glob("*.json")):
        h = load_json(path)
        if h.get("routing", {}).get("lens_eligibility") in {"active_lens", "experimental_lens"}:
            heuristics.append(h)
    output = output or (base / "generated" / "SKILL.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        f"name: writemind-{slug}",
        f'description: "Evidence-grounded Writer Advisor for {profile["name"]}. Preserves target register and exposes provenance, boundaries and revision actions. Not impersonation."',
        "---",
        "",
        f"# {profile['name']} · WriteMind Advisor",
        "",
        "Preserve the target platform, era and register. Never present inference as the writer's own words.",
        "",
        "## Advisor protocol",
        "",
        "1. `WRITING_BASELINE`: diagnose the text without the writer.",
        "2. `WRITER_TASK_FIT`: active / experimental / abstain.",
        "3. `WRITER_LENS`: use only task-relevant heuristics below.",
        "4. `TRANSFER`: state similarities, broken assumptions and confidence.",
        "5. `ACTION`: diagnose / advise / revise / challenge / compare / coach.",
        "",
    ]
    if not heuristics:
        lines += ["## Lens status", "", "No active or experimental Writer Lens is currently validated. Use Generic Writing Baseline and abstain from writer-specific claims.", ""]
    for h in heuristics:
        _render_heuristic(lines, h)
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
