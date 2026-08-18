# discordrec

Automatically send a Discord invite + link to members who have a Path of Exile 2 role.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables:
   - `DISCORD_TOKEN` (required)
   - `TARGET_GUILD_ID` (required)
   - `INVITE_URL` (required)
   - `EXTRA_LINK` (optional)
   - `POE2_ROLE_NAMES` (optional, comma-separated, default: `path of exile 2,poe2`)
   - `DRY_RUN` (optional, `true`/`false`)

## Run

```bash
python bot.py
```

When the bot starts, it DMs all non-bot users in `TARGET_GUILD_ID` whose roles match `POE2_ROLE_NAMES`.
Use `DRY_RUN=true` to preview recipients without sending messages.
