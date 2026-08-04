#!/usr/bin/env bash
# setup-sshfs.sh -- Mount the Obsidian vault from Intel server via SSHFS
#
# Prerequisites:
#   macOS: brew install macfuse sshfs
#   Linux: apt install sshfs
#
# Usage:
#   ./setup-sshfs.sh                              # uses defaults
#   ./setup-sshfs.sh user@server /remote/path     # custom

set -euo pipefail

SSH_TARGET="${1:-your-user@intel-server}"
REMOTE_PATH="${2:-/home/your-user/obsidian-vault}"
LOCAL_MOUNT="$HOME/obsidian-vault-remote"

if mount | grep -q "$LOCAL_MOUNT"; then
    echo "Already mounted at $LOCAL_MOUNT"
    exit 0
fi

mkdir -p "$LOCAL_MOUNT"

echo "Mounting $SSH_TARGET:$REMOTE_PATH → $LOCAL_MOUNT"
sshfs "$SSH_TARGET:$REMOTE_PATH" "$LOCAL_MOUNT" \
    -o reconnect \
    -o ServerAliveInterval=15 \
    -o ServerAliveCountMax=3 \
    -o follow_symlinks

echo "Mounted successfully."
echo ""
echo "To unmount: umount $LOCAL_MOUNT"
echo "To auto-mount on login, add to /etc/fstab or use a LaunchAgent."
