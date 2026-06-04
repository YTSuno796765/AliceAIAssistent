# Instructions for Codex / Claude

This repository has been sanitized for public visibility. Do not add personal
operational details, server coordinates, credentials, runtime snapshots, logs,
sessions, databases, cookies, or environment files.

## Safety

- Do not print, copy, commit, or infer secrets.
- Never commit API tokens, OAuth credentials, Telegram credentials, SSH keys,
  cookies, sessions, logs, caches, databases, lock files, pid files, or local
  environment files.
- Run `scripts/verify-no-secrets.ps1` on Windows or
  `scripts/verify-no-secrets.sh` on macOS/Linux before every commit.
- Keep deployment and server-specific runbooks outside this public repository.

## Working Pattern

1. Keep the repository public-safe by default.
2. Add examples only with placeholder values.
3. Document integrations at a design level only; do not include real accounts,
   hostnames, tokens, API keys, user IDs, or private infrastructure details.
4. Prefer generic templates over snapshots copied from a live runtime.
