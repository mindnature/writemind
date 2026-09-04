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
    lines = ["---", f"name: writemind-{slug}", f'description: "Evidence-grounded Writer Advisor for {profile["name"]}. Not impersonation."', "---", "", f"# {profile['name']} · WriteMind Advisor", "", "Preserve the target register. Use only evidence-grounded lenses below. Never present inference as the writer's own words.", ""]
    if not heuristics:
        lines += ["## Lens status", "", "No active or experimental Writer Lens is currently validated. Use Generic Writing Baseline and abstain from writer-specific claims."]
    for h in heuristics:
        lines += [f"## {h['heuristic_id']} · {h['name']}", "", f"Lens family: `{h['lens_family']}`", "", h["rule"], "", f"Eligibility: `{h.get('routing', {}).get('lens_eligibility')}`", ""]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output
