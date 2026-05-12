#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path


def load_configured_services(config_path: Path) -> list[str]:
    with config_path.open(encoding="utf-8") as file:
        return json.load(file)


def load_listed_services(readme_path: Path) -> list[str]:
    content = readme_path.read_text(encoding="utf-8")
    services_section = re.search(
        r"^## Services\s*$([\s\S]*?)(?:^## |\Z)",
        content,
        flags=re.MULTILINE,
    )
    if not services_section:
        return []

    return [
        match.group(1).strip()
        for match in re.finditer(r"^\s*-\s+(.+?)\s*$", services_section.group(1), flags=re.MULTILINE)
    ]


def main() -> int:
    repository_root = Path(__file__).resolve().parent.parent
    configured_services = load_configured_services(repository_root / "services.json")
    listed_services = load_listed_services(repository_root / "README.md")

    if configured_services != listed_services:
        print("README.md service list does not match services.json")
        print(f"Configured: {configured_services}")
        print(f"Listed:     {listed_services}")
        return 1

    print("README.md service list matches services.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
