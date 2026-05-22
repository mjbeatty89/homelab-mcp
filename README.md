# homelab-mcp

Aggregator gateway and per-platform MCP servers for managing a homelab
that mixes Proxmox VE, Docker, Unraid, and TrueNAS — plus a shared
harness-config bundle that ships the full personal MCP suite into Claude
Code, Claude Desktop, and Cursor.

## Services

- homelab-mcp
- proxmox-mcp
- docker-mcp
- unraid-mcp
- truenas-mcp

The list above is verified in CI against `services.json`, which is
generated from `inventory/services.yaml`.

## Layout

| Path           | Purpose                                                              |
|----------------|----------------------------------------------------------------------|
| `inventory/`   | Source of truth: hosts and services. See `inventory/README.md`.      |
| `clients/`     | Drop-in MCP configs for Claude Code / Desktop / Cursor + profiles.   |
| `servers/`     | Per-platform MCP server implementations (one dir per service).       |
| `gateway/`     | Cloudflare Worker that aggregates the platform servers.              |
| `secrets/`     | Conventions for Vault-backed secret distribution.                    |
| `runbooks/`    | Operational runbooks (upgrade Proxmox node, rotate snapshots, etc.). |
| `scripts/`     | Helpers — currently the services.json generator and sync verifier.   |

## Working on it

```bash
pip install -r requirements.txt
python3 scripts/generate_services.py   # after editing inventory/services.yaml
python3 scripts/verify_services_sync.py
```

CI runs both on every PR.
