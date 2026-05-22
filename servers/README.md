# servers/

One subdirectory per platform-specific MCP server. Each server owns its
own dependencies, transport, and capability set; the gateway aggregates
them.

Planned servers (see `inventory/services.yaml` for the canonical list):

- `proxmox-mcp/` — wraps the Proxmox VE API (proxmoxer)
- `docker-mcp/`  — Docker SDK over SSH on app-hosts
- `unraid-mcp/`  — Unraid GraphQL API
- `truenas-mcp/` — TrueNAS websocket API

Each server should:

1. Export a single MCP entrypoint (stdio for local dev, HTTP/SSE for
   gateway-fronted deployment).
2. Tag every tool with one of `read`, `mutate`, `destructive` in its
   description; the gateway uses this for auth tiering.
3. Provide a `describe_*` (read) tool for every `*` (mutate) tool —
   models that can read before they write make far fewer mistakes.
4. For destructive operations, expose a two-step API:
   `plan_<op>` returns an opaque token; `confirm_<op>(token)` performs
   the change. Tokens expire in 60s.
5. Accept an `idempotency_key` on every mutating call.

None of these are scaffolded yet — they'll land in follow-up PRs as we
build them out one platform at a time.
