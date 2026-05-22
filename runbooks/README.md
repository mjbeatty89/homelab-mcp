# runbooks/

Operational procedures the model (or you) can follow when something
needs to happen on the homelab. One file per procedure.

Suggested first runbooks:

- `upgrade-proxmox-node.md`        — drain, snapshot, apt upgrade, reboot, verify
- `rotate-truenas-snapshots.md`    — review retention, purge, verify replication
- `unraid-parity-check.md`         — schedule, monitor, interpret
- `docker-compose-deploy.md`       — pull, plan, apply with rollback
- `tunnel-rotation.md`             — rotate cloudflared credentials + Vault AppRole

Each runbook should have, at minimum:

1. **Preconditions** — what must be true before starting.
2. **Plan** — exact tool calls a model should make, in order, marked
   `read` vs `mutate`.
3. **Verification** — how to confirm success (specific tool calls
   whose output you can grep).
4. **Rollback** — what to do if step N fails.

Empty for now; will populate as servers come online.
