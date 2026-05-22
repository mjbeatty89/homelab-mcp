# Secrets

## Chosen approach: HashiCorp Vault (homelab), bootstrapped from Cloudflare Workers Secrets.

### Why not the alternatives

- **Vaultwarden** is a password manager (Bitwarden-compatible). It has
  no leases, no dynamic secrets, no audit primitives, and the API is
  built for human-vault sync. Wrong tool for service-to-service auth.
  Keep it for personal passwords.
- **1Password Desktop** can't be used from a Cloudflare Worker — it
  requires the desktop app or CLI present in the runtime. That's why
  the Dev env binding has been painful: it disappears the moment you
  leave a local interactive shell.
- **1Password Connect** would work (small HTTP service exposed into
  your vault) and is the lighter alternative if Vault feels heavy. But
  you still end up wanting Vault's lease/revoke/audit for homelab
  automation, so we go straight there.

### Topology

```
Claude harness  ──┐
                  │  Authorization: Bearer <session token>
                  ▼
   Cloudflare Worker  ── verifies session token against KV/Workers Secrets
        │
        │  AppRole login (role_id + secret_id from Worker Secrets)
        ▼
   HashiCorp Vault (in homelab, exposed via cloudflared)
        │
        │  KV reads:  kv/homelab/proxmox/pve-01, kv/homelab/unraid/..., etc.
        ▼
   Per-platform credentials (short-lived where the API supports it)
```

### Bootstrap secrets (Cloudflare Workers Secrets / Secrets Store)

These are the only secrets stored *outside* Vault:

| Name                | Purpose                                                |
|---------------------|--------------------------------------------------------|
| `VAULT_ADDR`        | URL of Vault behind the cloudflared tunnel             |
| `VAULT_ROLE_ID`     | AppRole role_id for the Worker                         |
| `VAULT_SECRET_ID`   | AppRole secret_id (rotated; use response-wrapping)     |
| `MCP_BEARER_PUBKEY` | Public key used to verify incoming MCP session tokens  |

Set them with `wrangler secret put <NAME>`.

### Vault layout

```
kv/homelab/
  proxmox/pve-01           { api_token_id, api_token_secret, user }
  proxmox/pve-02           { ... }
  unraid/unraid-01         { api_key, host }
  truenas/truenas-01       { api_key, host }
  docker/docker-prod       { ssh_user, ssh_key_pem, host }
  github/automation        { pat }                  # for the GitHub MCP
```

Vault paths are referenced from `inventory/hosts.yaml` as `vault_path:`.

### Operational rules

- Worker code **never logs secret values**, including in error paths.
- Each per-platform read goes through a small helper that caches by
  lease ID and respects `lease_duration`.
- Use `vault token revoke -self` on Worker shutdown when feasible (the
  Cloudflare runtime won't always give you that hook; rely on short
  leases as the backstop).
- Use response-wrapping (`-wrap-ttl`) for the initial AppRole
  `secret_id` delivery so it can only be unwrapped once.

### What goes where, quick reference

| Secret kind                          | Where it lives                |
|--------------------------------------|-------------------------------|
| Vault bootstrap creds                | Cloudflare Workers Secrets    |
| Proxmox / Unraid / TrueNAS API keys  | Vault KV                      |
| SSH keys for Docker hosts            | Vault KV                      |
| Per-session MCP bearer tokens        | Issued by Worker, never stored|
| Personal passwords / TOTP            | Vaultwarden (unchanged)       |
