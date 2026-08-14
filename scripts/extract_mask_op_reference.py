from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def _subparser(parser: argparse.ArgumentParser, name: str) -> argparse.ArgumentParser:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return action.choices[name]
    raise RuntimeError(f"No subparser named {name!r} below {parser.prog!r}")


def _display_default(action: argparse.Action) -> str:
    if action.default is argparse.SUPPRESS:
        return "inapplicable"
    if action.default is None:
        return "none"
    return str(action.default)


def _action_record(action: argparse.Action) -> dict[str, Any]:
    choices = list(action.choices) if action.choices is not None else []
    value_type = getattr(action.type, "__name__", "inapplicable")
    return {
        "flags": ", ".join(action.option_strings),
        "required": action.required,
        "choices": choices,
        "default": _display_default(action),
        "type": value_type,
        "repeatable": isinstance(action, argparse._AppendAction),
        "help": action.help,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-root", type=Path, required=True)
    args = parser.parse_args()

    sys.path.insert(0, str(args.code_root.resolve() / "src"))
    from GenomicElementTools.cli import GenomicElementTools  # type: ignore[import-not-found]

    root = argparse.ArgumentParser(prog="GenomicElementTools")
    GenomicElementTools.set_parser(root)
    intersect = _subparser(_subparser(root, "mask_op"), "intersect")
    usage = " ".join(intersect.format_usage().removeprefix("usage:").split())
    print(
        json.dumps(
            {
                "usage": usage,
                "arguments": [_action_record(action) for action in intersect._actions],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
