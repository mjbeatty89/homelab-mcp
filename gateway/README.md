# gateway/

Cloudflare Worker that fronts the platform MCP servers.

Responsibilities:

- Terminate the MCP session (HTTP/SSE) and verify the bearer token.
- Look up requested tool → host in `inventory/`.
- Pull short-lived per-platform credentials from Vault (AppRole).
- Route to the appropriate platform server over the Cloudflare tunnel.
- Enforce auth tiers from tool capability tags (`read` / `mutate` /
  `destructive`).
- Write a JSON-line audit record per call:
  `{ts, session, tool, host, args_redacted, result_kind, lease_id}`.

Not implemented yet — see `secrets/README.md` for the topology and
bootstrap-secret list this Worker will need.
