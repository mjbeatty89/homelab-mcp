#!/usr/bin/env python3
"""Generate services.json from inventory/services.yaml.

services.json is the published list of MCP servers in this suite. We
generate it from inventory/services.yaml so editors only touch one file;
CI verifies the generated artifact matches what's committed.
"""
import json
import sys
from pathlib import Path

import yaml


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    inventory = root / "inventory" / "services.yaml"
    output = root / "services.json"

    with inventory.open(encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    services = data.get("services") or []
    if not isinstance(services, list):
        print(f"error: {inventory.relative_to(root)} 'services' must be a list", file=sys.stderr)
        return 1

    names: list[str] = []
    for index, service in enumerate(services):
        if not isinstance(service, dict) or "name" not in service:
            print(
                f"error: {inventory.relative_to(root)} services[{index}] is missing 'name'",
                file=sys.stderr,
            )
            return 1
        names.append(service["name"])

    output.write_text(json.dumps(names, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(root)} ({len(names)} services)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
