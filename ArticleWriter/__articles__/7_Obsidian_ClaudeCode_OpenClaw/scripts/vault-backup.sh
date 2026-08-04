#!/usr/bin/env bash
# vault-backup.sh -- Auto-commit Obsidian vault changes to Git
#
# Install as cron job (every 30 min):
#   crontab -e
#   */30 * * * * /home/your-user/obsidian-vault/scripts/vault-backup.sh >> /tmp/vault-backup.log 2>&1
#
# Optional: add a git remote for off-site backup
#   cd ~/obsidian-vault && git remote add origin git@github.com:you/obsidian-vault-backup.git

set -euo pipefail

VAULT_DIR="${VAULT_DIR:-$HOME/obsidian-vault}"

cd "$VAULT_DIR"

git add -A

if ! git diff --cached --quiet; then
    git commit -m "auto: vault snapshot $(date +%Y-%m-%d_%H:%M)"

    if git remote get-url origin >/dev/null 2>&1; then
        git push origin main 2>/dev/null || true
    fi
fi
