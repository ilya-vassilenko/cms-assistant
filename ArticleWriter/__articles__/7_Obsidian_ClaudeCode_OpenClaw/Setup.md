# Obsidian Second Brain -- Setup Guide

An Obsidian-based personal knowledge management system powered by OpenClaw (Telegram capture + RAG queries), Docker (web UI), and Claude Code MCP (IDE integration).

## Architecture

```
┌─────────────┐     ┌────────────────────────────────────────────────┐
│  Telegram    │◄───►│  Intel Home Server (always-on)                │
│  (capture +  │     │                                               │
│   query)     │     │  ┌──────────┐  ┌─────────────────────┐       │
└─────────────┘     │  │ OpenClaw │──│ Obsidian Vault      │       │
                    │  │ Agent    │  │ ~/obsidian-vault/    │       │
                    │  └──────────┘  │ (Git repo)           │       │
┌─────────────┐     │       │        └──────────┬──────────┘       │
│  OpenAI API  │◄───│───────┘                   │                   │
│  (summary,   │     │                ┌─────────┴──────────┐       │
│   whisper,   │     │                │                    │       │
│   RAG)       │     │  ┌─────────────┴──┐  ┌─────────────┴──┐   │
└─────────────┘     │  │ Obsidian Remote│  │ Obsidian API   │   │
                    │  │ :8080 (Docker) │  │ :5000 (Docker) │   │
                    │  └────────────────┘  └────────────────┘   │
                    └───────────────────────────────────────────┘
                              │                    │
                    ┌─────────┴────────┐           │
                    │  Browser (any    │    ┌──────┴──────┐
                    │  device on LAN)  │    │ Claude Code │
                    └──────────────────┘    │ MCP (SSHFS) │
                                           └─────────────┘
```

## Prerequisites

| Component | Requirement |
|-----------|-------------|
| Intel Server | Linux, Node.js 22.14+, Docker, Git, Python 3, curl |
| OpenClaw | `npm install -g openclaw@latest` (already installed) |
| OpenAI API Key | From your $20 ChatGPT license (api.openai.com/account/api-keys) |
| MacBook | macFUSE + sshfs, Node.js/npx, Claude Code CLI |

---

## Phase 1: Initialize the Vault (Intel Server)

### 1.1 Copy the vault scaffold

```bash
# On the Intel server
mkdir -p ~/obsidian-vault
cp -r vault-scaffold/* ~/obsidian-vault/
cp vault-scaffold/.gitignore ~/obsidian-vault/
```

### 1.2 Initialize Git

```bash
cd ~/obsidian-vault
git init
git add -A
git commit -m "init: vault scaffold with folder structure and templates"
```

### 1.3 Verify structure

```bash
tree -L 2 ~/obsidian-vault
# Expected:
# ├── 00-Inbox/
# ├── 10-Customers/
# ├── 20-Resources/
# ├── 30-Ideas/
# ├── 40-Quotes/
# ├── 50-Files/
# ├── 90-Archive/
# └── Templates/
#     ├── customer.md
#     ├── idea.md
#     ├── link.md
#     ├── quote.md
#     └── voice.md
```

### 1.4 Set up auto-backup cron

```bash
# Copy backup script
cp scripts/vault-backup.sh ~/obsidian-vault/scripts/
chmod +x ~/obsidian-vault/scripts/vault-backup.sh

# Edit the VAULT_DIR variable if your path differs
# Then add to crontab:
crontab -e
# Add this line:
*/30 * * * * /home/YOUR_USER/obsidian-vault/scripts/vault-backup.sh >> /tmp/vault-backup.log 2>&1
```

**Optional -- remote backup:**

```bash
cd ~/obsidian-vault
git remote add origin git@github.com:YOUR_USER/obsidian-vault-backup.git
git push -u origin main
```

The backup script will auto-push to the remote if one is configured.

---

## Phase 2: Configure OpenClaw + Telegram

### 2.1 Create the Telegram bot

1. Open Telegram, search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g., "My Vault") and username (e.g., `my_vault_brain_bot`)
4. Copy the bot token (looks like `123456:ABCdefGHIjklMNO`)

### 2.2 Set environment variables

```bash
# Add to ~/.bashrc or ~/.zshrc on the Intel server
export TELEGRAM_BOT_TOKEN="123456:ABCdefGHIjklMNO"
export OPENAI_API_KEY="sk-..."
```

Reload: `source ~/.bashrc`

### 2.3 Install the obsidian-direct skill

```bash
openclaw skill install obsidian-direct
```

### 2.4 Install the custom second-brain skill

```bash
# Copy the skill to OpenClaw's skill directory
cp -r openclaw/second-brain ~/.openclaw/workspace/skills/second-brain

# Verify it loaded
openclaw skills list
# Should show: second-brain, obsidian-direct
```

### 2.5 Configure OpenClaw

Copy the provided config (adjust paths if needed):

```bash
# Back up existing config
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak 2>/dev/null || true

# Copy new config
cp openclaw/openclaw.json5 ~/.openclaw/openclaw.json
```

**Important:** Edit `~/.openclaw/openclaw.json` and replace:
- `${TELEGRAM_BOT_TOKEN}` with your actual token (or leave it if you set the env var)
- Verify `workspace` points to `~/obsidian-vault`

### 2.6 Start the gateway

```bash
openclaw gateway
```

### 2.7 Pair your Telegram account

1. Open Telegram and send any message to your bot
2. On the server terminal, you'll see a pairing code
3. Approve it:

```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

### 2.8 Test basic commands

Send these via Telegram to verify:

| Message | Expected result |
|---------|-----------------|
| `/help` | Shows command list |
| `/idea Test my vault setup` | Creates note in `00-Inbox/` |
| `/link https://example.com` | Fetches, summarizes, saves |
| `/customer Acme First meeting` | Creates `10-Customers/Acme.md` |
| `/q What ideas have I saved?` | RAG query over vault |

---

## Phase 3: Docker Web UI (Intel Server)

### 3.1 Deploy the stack

```bash
cd /path/to/docker/   # where docker-compose.yml lives

# Create .env from template
cp .env.example .env

# Edit .env -- set VAULT_PATH, passwords
nano .env

# Start
docker compose up -d
```

### 3.2 Access Obsidian in browser

Open `http://<server-ip>:8080` from any device on your network.

On first launch:
1. Open the vault at `/vaults/second-brain`
2. Go to **Settings → Community Plugins → Browse**
3. Search and install **Smart Connections**
4. Enable it and let it index the vault (may take a few minutes on first run)

Smart Connections gives you:
- Semantic search across all notes (by meaning, not just keywords)
- Related notes sidebar (shows connected ideas while you read)
- In-vault RAG chat

### 3.3 REST API access

The API is at `http://<server-ip>:5000/docs` (Swagger UI).

Test with curl:

```bash
curl -u admin:YOUR_PASSWORD http://localhost:5000/api/notes
```

---

## Phase 4: Claude Code MCP (MacBook)

### 4.1 Install SSHFS

```bash
brew install macfuse
brew install sshfs
```

Note: macFUSE requires a reboot after install and may need a security exception in System Preferences → Privacy & Security.

### 4.2 Mount the vault

```bash
# Edit and run the setup script, or do it manually:
mkdir -p ~/obsidian-vault-remote

sshfs YOUR_USER@INTEL_SERVER_IP:/home/YOUR_USER/obsidian-vault \
    ~/obsidian-vault-remote \
    -o reconnect \
    -o ServerAliveInterval=15 \
    -o ServerAliveCountMax=3
```

Verify: `ls ~/obsidian-vault-remote` should show `00-Inbox/`, `10-Customers/`, etc.

### 4.3 Add MCP server to Claude Code

```bash
claude mcp add obsidian -- npx -y obsidian-mcp --vault ~/obsidian-vault-remote
```

### 4.4 Test from Claude Code

```bash
claude "Search my vault for all customer notes"
claude "What links have I saved about security?"
claude "Create a new idea note about container monitoring"
```

Available MCP tools: `search_notes`, `read_note`, `create_note`, `get_backlinks`, `vault_stats`, `list_notes`, and more.

---

## Telegram Command Reference

| Command | What it does |
|---------|-------------|
| `/link <url> [comment]` | Fetch URL, AI-summarize, auto-tag, save to Inbox |
| `/customer <name> <note>` | Add/update customer note in `10-Customers/` |
| `/idea <text>` | Save quick idea to Inbox |
| `/quote <text> -- <author>` | Save attributed quote to Inbox |
| `/q <question>` | RAG query: search vault, synthesize answer via ChatGPT |
| `/search <term>` | Keyword search, returns list of matching notes |
| `/help` | Show this command list |
| *(no command)* | AI auto-classifies: URL→link, question→query, else→idea |
| *(voice message)* | Transcribe via Whisper API, summarize, save |
| *(photo/file)* | Save to `50-Files/`, create reference note |

---

## Vault Folder Structure

```
obsidian-vault/
├── 00-Inbox/          ← All Telegram captures land here
├── 10-Customers/      ← Per-customer subfolders
│   ├── Acme Corp.md
│   └── Beta GmbH.md
├── 20-Resources/      ← Articles, links, references
├── 30-Ideas/          ← Quick thoughts and brainstorms
├── 40-Quotes/         ← Saved quotes with attribution
├── 50-Files/          ← Binary attachments
│   ├── photos/
│   ├── docs/
│   ├── voice/
│   └── other/
├── 90-Archive/        ← Completed or outdated items
├── Templates/         ← Note templates
├── scripts/           ← Backup and utility scripts
└── .gitignore
```

**Workflow:** Everything arrives in `00-Inbox/`. Periodically triage items into the right folder -- or let them accumulate and rely on search/tags.

---

## File Inventory

This package contains all the files you need:

```
7_Obsidian_ClaudeCode_OpenClaw/
├── Setup.md                          ← This guide
├── vault-scaffold/                   ← Copy to ~/obsidian-vault on server
│   ├── 00-Inbox/.gitkeep
│   ├── 10-Customers/.gitkeep
│   ├── 20-Resources/.gitkeep
│   ├── 30-Ideas/.gitkeep
│   ├── 40-Quotes/.gitkeep
│   ├── 50-Files/.gitkeep
│   ├── 90-Archive/.gitkeep
│   ├── Templates/
│   │   ├── link.md
│   │   ├── customer.md
│   │   ├── idea.md
│   │   ├── quote.md
│   │   └── voice.md
│   └── .gitignore
├── openclaw/
│   ├── openclaw.json5                ← OpenClaw config → ~/.openclaw/openclaw.json
│   └── second-brain/                 ← Custom skill → ~/.openclaw/workspace/skills/
│       ├── SKILL.md
│       └── scripts/
│           ├── process_url.py
│           ├── process_voice.py
│           └── process_file.py
├── docker/
│   ├── docker-compose.yml            ← Obsidian Remote + REST API
│   └── .env.example
└── scripts/
    ├── vault-backup.sh               ← Cron auto-commit + push
    ├── setup-sshfs.sh                ← Mount vault on MacBook
    └── setup-mcp.sh                  ← Add MCP server to Claude Code
```

---

## Troubleshooting

### OpenClaw doesn't respond in Telegram
- Check gateway is running: `openclaw gateway status`
- Check pairing: `openclaw pairing list telegram`
- Check token: verify `TELEGRAM_BOT_TOKEN` env var is set

### URL processing fails
- Verify `OPENAI_API_KEY` is set and valid
- Test manually: `python3 ~/.openclaw/workspace/skills/second-brain/scripts/process_url.py "https://example.com"`
- Check curl can reach the URL: `curl -sI https://example.com`

### Voice transcription fails
- Whisper API requires a valid OpenAI API key with audio access
- Check audio file format (supports mp3, mp4, mpeg, mpga, m4a, wav, webm)
- Test manually: `python3 ~/.openclaw/workspace/skills/second-brain/scripts/process_voice.py /path/to/audio.ogg`

### SSHFS mount drops
- The `-o reconnect` flag should handle temporary disconnects
- For persistent mounts, create a macOS LaunchAgent or add to `/etc/fstab`
- Alternative: use `rsync` on a schedule instead of SSHFS

### Obsidian Remote shows blank page
- Check Docker logs: `docker logs obsidian-remote`
- Verify the vault path in `.env` is correct
- Ensure ports 8080/8443 are not blocked by firewall

### Smart Connections not finding notes
- Wait for initial indexing to complete (check plugin status)
- Try re-indexing: Smart Connections settings → Force Re-Index
- Verify notes have content (empty files won't be indexed)

---

## Next Steps (v2 Enhancements)

- **Vector embeddings**: Index all notes with OpenAI embeddings for better RAG retrieval. Store in SQLite, query by cosine similarity before passing to ChatGPT.
- **Daily digest**: Schedule OpenClaw to send a Telegram summary of yesterday's captures every morning.
- **Auto-triage**: Periodically move aged `00-Inbox/` items to their target folders based on tags.
- **Dataview plugin**: Install in Obsidian Remote for dynamic tables (e.g., "all customer notes from the last 30 days").
- **Tailscale**: For secure remote access to Obsidian Remote and the REST API from outside your home network.
