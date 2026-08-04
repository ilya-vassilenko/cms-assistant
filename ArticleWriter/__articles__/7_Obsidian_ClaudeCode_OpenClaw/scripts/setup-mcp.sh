#!/usr/bin/env bash
# setup-mcp.sh -- Configure Claude Code MCP server for Obsidian vault access
#
# Run on your MacBook after mounting the vault via SSHFS.
#
# Prerequisites:
#   - Claude Code installed (claude CLI available)
#   - Node.js / npx available
#   - SSHFS mount active (see setup-sshfs.sh)

set -euo pipefail

VAULT_MOUNT="${1:-$HOME/obsidian-vault-remote}"

if [ ! -d "$VAULT_MOUNT" ]; then
    echo "ERROR: Vault mount not found at $VAULT_MOUNT"
    echo "Run setup-sshfs.sh first, or pass the mount path as argument."
    exit 1
fi

echo "Adding Obsidian MCP server to Claude Code..."
echo "  Vault path: $VAULT_MOUNT"

claude mcp add obsidian -- npx -y obsidian-mcp --vault "$VAULT_MOUNT"

echo ""
echo "Done. Available tools in Claude Code:"
echo "  search_notes, read_note, create_note, get_backlinks,"
echo "  vault_stats, list_notes, and more."
echo ""
echo "Test with: claude 'Search my vault for notes about customers'"
