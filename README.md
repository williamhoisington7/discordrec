# discordrec

Offline **Would Kill For PiE** invitation studio and optional Discord helpers.

## Invitation Studio (standalone Windows 11 app)

Create one formal PDF invitation at a time:

1. Enter a recipient name.
2. Preview or download a dark-fantasy styled letter.
3. The letter asks them to visit **wouldkillforpie.com** first.
4. When they are ready, they join Discord using the link on that site.

No internet connection and no Discord bot are required to generate letters.

### Run from source

```bash
pip install -r requirements.txt
python desktop_app.py
```

Browser-only mode:

```bash
python app.py
```

Then open `http://127.0.0.1:5000`.

### Build the Windows 11 executable

On Windows 11:

```bat
build_windows.bat
```

Output:

```text
dist\WouldKillForPiE-InvitationStudio.exe
```

Double-click the `.exe` to open the offline invitation studio.

GitHub Actions also builds the Windows executable on push (`Build Windows Invitation Studio` workflow), uploads `WouldKillForPiE-InvitationStudio.exe` as an artifact, and publishes it on the [latest release](https://github.com/williamhoisington7/discordrec/releases/latest).

Direct download (after the latest main build finishes):

https://github.com/williamhoisington7/discordrec/releases/latest/download/WouldKillForPiE-InvitationStudio.exe

### Tests

```bash
python -m unittest discover -s tests -v
```

## Optional PoE2 DM bot

```bash
pip install -r requirements.txt
python bot.py
```

Environment variables:

- `DISCORD_TOKEN` (required)
- `TARGET_GUILD_ID` (required)
- `INVITE_URL` (required)
- `EXTRA_LINK` (optional)
- `POE2_ROLE_NAMES` (optional)
- `DRY_RUN` (optional)
