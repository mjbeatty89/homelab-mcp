# Inventory

Source of truth for everything the homelab MCP gateway can reach.

## Files

- `hosts.yaml` — physical/virtual machines the gateway operates on
  (Proxmox nodes, Unraid box, TrueNAS, Docker app-hosts, etc.).
- `services.yaml` — MCP servers that make up this suite. The committed
  top-level `services.json` is **generated** from this file by
  `scripts/generate_services.py`; CI fails if they drift.

## Conventions

- Host names are stable identifiers — never rename, only deprecate.
- `vault_path` values are Vault KV paths (`kv/homelab/<platform>/<host>`),
  never credentials themselves. See `secrets/README.md`.
- `capabilities` are namespaced verbs (`vm.lifecycle`, `dataset.snapshot`).
  The gateway uses them to route tool calls and to refuse calls a host
  hasn't opted into.
- Tag every capability that mutates state with a verb ending in
  `.lifecycle`, `.snapshot`, or `.write`. Read-only verbs end in `.read`
  or `.status`. The gateway enforces a stricter auth tier for mutating
  capabilities.
