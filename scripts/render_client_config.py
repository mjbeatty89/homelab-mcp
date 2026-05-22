#!/usr/bin/env python3
"""Render a clients/*.json template by substituting ${VAR} placeholders
from the current environment.

Most MCP hosts (Claude Desktop, Cursor) do NOT expand ${VAR} inside
their config files — values are passed to spawned subprocesses literally.
Run this script to produce a ready-to-use config from a template.

Usage:
    python3 scripts/render_client_config.py clients/claude-desktop.config.json > out.json
    python3 scripts/render_client_config.py clients/cursor.mcp.json --output ~/.cursor/mcp.json

Unset placeholders are reported on stderr and the corresponding server
block is removed so the harness ignores it cleanly instead of crashing.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")


def render(value, missing: set[str]):
    if isinstance(value, str):
        def replace(match: re.Match) -> str:
            name = match.group(1)
            if name in os.environ:
                return os.environ[name]
            missing.add(name)
            return match.group(0)
        return PLACEHOLDER.sub(replace, value)
    if isinstance(value, list):
        return [render(item, missing) for item in value]
    if isinstance(value, dict):
        return {key: render(val, missing) for key, val in value.items()}
    return value


def server_has_unresolved(block, missing: set[str]) -> bool:
    rendered = json.dumps(block)
    return any(f"${{{name}}}" in rendered for name in missing)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path, help="Path to a clients/*.json template")
    parser.add_argument("--output", "-o", type=Path, help="Write rendered config here (default: stdout)")
    parser.add_argument(
        "--keep-unresolved",
        action="store_true",
        help="Keep server blocks that still contain ${VAR}; default removes them",
    )
    args = parser.parse_args()

    with args.template.open(encoding="utf-8") as file:
        template = json.load(file)

    missing: set[str] = set()
    rendered = render(template, missing)

    if missing:
        print(f"warning: {len(missing)} unset env var(s): {sorted(missing)}", file=sys.stderr)

    if not args.keep_unresolved and isinstance(rendered, dict) and "mcpServers" in rendered:
        kept = {}
        dropped = []
        for name, block in rendered["mcpServers"].items():
            if server_has_unresolved(block, missing):
                dropped.append(name)
            else:
                kept[name] = block
        rendered["mcpServers"] = kept
        if dropped:
            print(f"info: dropped server(s) with unresolved vars: {dropped}", file=sys.stderr)

    output_json = json.dumps(rendered, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output_json, encoding="utf-8")
        print(f"Wrote {args.output}", file=sys.stderr)
    else:
        sys.stdout.write(output_json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
