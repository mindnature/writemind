#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.core import build_skill, discover_writers, init_writer
from runtime.policy import transfer_action
from runtime.taskfit import evaluate_task_fit
from runtime.validation import validate_writer


def main() -> int:
    parser = argparse.ArgumentParser(prog="writemind")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init-writer")
    p_init.add_argument("name")
    p_init.add_argument("--slug")

    p_validate = sub.add_parser("validate")
    p_validate.add_argument("--writer", required=True)

    p_fit = sub.add_parser("task-fit")
    p_fit.add_argument("--input", required=True)

    p_transfer = sub.add_parser("transfer-action")
    p_transfer.add_argument("confidence", choices=["high", "medium", "low", "reject"])

    p_build = sub.add_parser("build-skill")
    p_build.add_argument("--writer", required=True)
    p_build.add_argument("--output")

    sub.add_parser("list-writers")
    args = parser.parse_args()

    try:
        if args.cmd == "init-writer":
            print(init_writer(args.name, args.slug).resolve())
        elif args.cmd == "validate":
            errors = validate_writer(args.writer)
            if errors:
                for e in errors:
                    print(f"ERROR: {e}")
                return 1
            print("Validation OK")
        elif args.cmd == "task-fit":
            payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
            print(json.dumps(evaluate_task_fit(payload), ensure_ascii=False, indent=2))
        elif args.cmd == "transfer-action":
            print(transfer_action(args.confidence))
        elif args.cmd == "build-skill":
            output = Path(args.output) if args.output else None
            print(build_skill(args.writer, output=output).resolve())
        elif args.cmd == "list-writers":
            print("\n".join(discover_writers()))
        return 0
    except (ValueError, FileNotFoundError, FileExistsError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
