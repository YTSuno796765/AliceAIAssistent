# Public Personal Agent Sandbox

This repository is a sanitized public workspace for generic personal-agent
experiments and documentation.

It intentionally does not contain:

- real API keys, tokens, OAuth credentials, cookies, or sessions;
- server hostnames, SSH users, SSH ports, SSH key paths, or deployment logs;
- runtime snapshots, memory exports, databases, caches, or personal data;
- production runbooks tied to a private server.

## Safety

Before committing, run:

```powershell
./scripts/verify-no-secrets.ps1
```

or on macOS/Linux:

```bash
bash scripts/verify-no-secrets.sh
```

Use placeholder values in examples and keep private operational notes outside
this public repository.
