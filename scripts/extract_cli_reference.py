"""Extract stable, JSON-serializable snapshots from the shipped CLI parsers."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Iterable


_REPEATABLE_ACTIONS = (argparse._AppendAction,) + (
    (argparse._ExtendAction,) if hasattr(argparse, "_ExtendAction") else ()
)


def _value(value: Any) -> Any:
    if value is argparse.SUPPRESS:
        return "inapplicable"
    if value is None:
        return "none"
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [_value(item) for item in value]
    return str(value)


def _type_name(value: Any) -> str:
    if value is None:
        return "inapplicable"
    return getattr(value, "__name__", str(value))


def _argument(action: argparse.Action) -> dict[str, Any]:
    flags = list(action.option_strings)
    return {
        "flags": ", ".join(flags) if flags else action.dest,
        "spellings": flags,
        "dest": action.dest,
        "required": bool(getattr(action, "required", False)),
        "choices": [_value(choice) for choice in action.choices]
        if action.choices is not None
        else [],
        "default": _value(action.default),
        "repeatable": isinstance(action, _REPEATABLE_ACTIONS),
        "nargs": _value(action.nargs),
        "type": _type_name(action.type),
        "help": action.help or "",
        "action": action.__class__.__name__,
    }


def _subparsers(parser: argparse.ArgumentParser) -> Iterable[tuple[str, argparse.ArgumentParser]]:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            yield from sorted(action.choices.items())


def _records(
    parser: argparse.ArgumentParser, path: tuple[str, ...] = ()
) -> list[dict[str, Any]]:
    records = [
        {
            "path": " ".join(path) or "(root)",
            "usage": " ".join(parser.format_usage().removeprefix("usage:").split()),
            "help": parser.description or "",
            "arguments": [
                _argument(action)
                for action in parser._actions
                if not isinstance(action, argparse._SubParsersAction)
            ],
        }
    ]
    for name, child in _subparsers(parser):
        records.extend(_records(child, path + (name,)))
    return records


def extract(tool: str, code_root: Path) -> list[dict[str, Any]]:
    sys.path.insert(0, str(code_root.resolve() / "src"))
    if tool == "GenomicElementTools":
        from GenomicElementTools.cli import GenomicElementTools  # type: ignore[import-not-found]

        builder = GenomicElementTools
    elif tool == "ExogeneousSequenceTools":
        from ExogeneousSequenceTools.cli import ExogeneousSequenceTools  # type: ignore[import-not-found]

        builder = ExogeneousSequenceTools
    elif tool == "MotifTools":
        from MotifTools.cli import MotifTools  # type: ignore[import-not-found]

        builder = MotifTools
    else:
        raise ValueError(f"Unsupported CLI: {tool}")
    parser = argparse.ArgumentParser(prog=tool)
    builder.set_parser(parser)
    return _records(parser)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code-root", type=Path, required=True)
    parser.add_argument("--tool", choices=("GenomicElementTools", "ExogeneousSequenceTools", "MotifTools"), required=True)
    args = parser.parse_args()
    print(json.dumps(extract(args.tool, args.code_root), sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
