# Harness configs

Drop-in MCP configurations for the different model harnesses, all
referencing the same set of personal MCP servers with env-var
placeholders.

## Files

| File                            | Use with                                                       |
|---------------------------------|----------------------------------------------------------------|
| `claude-code.mcp.json`          | Claude Code CLI — copy to `.mcp.json` at a project root        |
| `claude-desktop.config.json`    | Claude Desktop — merge into `claude_desktop_config.json`       |
| `cursor.mcp.json`               | Cursor — copy to `~/.cursor/mcp.json` or `<project>/.cursor/`  |
| `profiles/homelab.json`         | Slim profile: just homelab + filesystem + memory               |
| `profiles/dev.json`             | Coding profile: github, supabase, postgres, context7, memory   |
| `profiles/research.json`        | Read-heavy profile: fetch, search, hf, context7, memory        |

> **Claude Code on the web** does not read these files — MCPs there are
> configured per-environment in the web UI. Use these files for the
> CLI / desktop / Cursor flows.

## Why profiles

Shipping 200+ tools every session bloats the prompt and degrades model
behavior. Pick the smallest profile that covers the task. The full
suite is still available — just edit the active config to the profile
file you want (or symlink).

## Harness compatibility — important

These files use `${VAR}` placeholders. Harness support varies:

| Harness        | Expands `${VAR}` in config? | Recommended workflow                              |
|----------------|-----------------------------|---------------------------------------------------|
| Claude Code    | Partial (env vars in shell when CLI launches) | Use the template directly if you set env vars before `claude` |
| Claude Desktop | **No** — values pass through literally        | Render first (see below), then point Desktop at the output |
| Cursor         | **No**                                        | Render first, then write to `~/.cursor/mcp.json` |

For the harnesses that don't expand placeholders, use the render
script — it reads `${VAR}` from your shell env and emits a
ready-to-use config, dropping any server whose vars aren't set so the
harness ignores those entries instead of erroring:

```sh
# Render and write to the Desktop config location (macOS)
python3 scripts/render_client_config.py clients/claude-desktop.config.json \
    --output "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Render and write to Cursor's user config
python3 scripts/render_client_config.py clients/cursor.mcp.json \
    --output "$HOME/.cursor/mcp.json"

# Or print to stdout for inspection
python3 scripts/render_client_config.py clients/claude-code.mcp.json
```

## Env vars to set

Populate these in your shell init or your harness's secret store. The
homelab gateway entry expects a bearer token issued by your Cloudflare
Worker:

```sh
export HOMELAB_MCP_URL="https://homelab-mcp.<your-account>.workers.dev/sse"
export HOMELAB_MCP_TOKEN="..."  # short-lived; see secrets/README.md
export GITHUB_PAT="..."
export SUPABASE_ACCESS_TOKEN="..."
export POSTGRES_URL="..."
export BRAVE_API_KEY="..."
export HF_TOKEN="..."
export SLACK_BOT_TOKEN="..."
export LINEAR_API_KEY="..."
```

Anything not set will cause the harness to skip that server at startup
rather than crash.

## Hosted vs local servers

Many MCP servers in this bundle are **remote/hosted** by their vendor.
We connect to them via the `mcp-remote` bridge so a single config style
works in every harness. The homelab gateway itself is a hosted Worker
in your Cloudflare account.

Servers marked `local-only` in the configs run as subprocesses and need
the relevant package available via `npx` or `uvx`.
