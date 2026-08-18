# discordrec

Tools for Discord community recruitment around [wouldkillforpie.com](https://wouldkillforpie.com):

1. **Invitation letter UI** — create a formal, personalized PDF for one person at a time.
2. **Optional role-based DM bot** — message members who already have a Path of Exile 2 role.

## Invitation letter UI

The UI uses a dark-fantasy Would Kill For PiE theme (deep charcoal, crimson, and gold) inspired by the community’s Path of Exile aesthetic.

Each letter:

- is personalized with the recipient’s name
- asks them to visit **wouldkillforpie.com** first to understand the community
- tells them to join Discord only by clicking the link on that site

### Setup

```bash
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Open `http://127.0.0.1:5000`, enter a recipient name, preview the letter, and download the PDF.

Optional fields:

- Community name
- Recruitment site URL (defaults to `https://wouldkillforpie.com`)
- Signer name
- Personal note

### Tests

```bash
python -m unittest discover -s tests -v
```

## Optional PoE2 DM bot

1. Install dependencies with `pip install -r requirements.txt`.
2. Set environment variables:
   - `DISCORD_TOKEN` (required)
   - `TARGET_GUILD_ID` (required)
   - `INVITE_URL` (required)
   - `EXTRA_LINK` (optional)
   - `POE2_ROLE_NAMES` (optional, comma-separated, default: `path of exile 2,poe2`)
   - `DRY_RUN` (optional, `true`/`false`)

```bash
python bot.py
```

When the bot starts, it DMs non-bot users in `TARGET_GUILD_ID` whose roles match `POE2_ROLE_NAMES`.
Use `DRY_RUN=true` to preview recipients without sending messages.
