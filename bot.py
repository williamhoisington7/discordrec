from __future__ import annotations

import asyncio
import logging
import os

import discord

from poe2_inviter import DEFAULT_POE2_ROLE_ALIASES, build_invite_message, is_poe2_player

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("poe2-invite-bot")

TOKEN = os.getenv("DISCORD_TOKEN", "")
GUILD_ID = int(os.getenv("TARGET_GUILD_ID", "0"))
INVITE_URL = os.getenv("INVITE_URL", "")
EXTRA_LINK = os.getenv("EXTRA_LINK")
TARGET_ROLE_NAMES = tuple(
    role_name.strip()
    for role_name in os.getenv("POE2_ROLE_NAMES", ",".join(DEFAULT_POE2_ROLE_ALIASES)).split(",")
    if role_name.strip()
)
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"


class Poe2InviteBot(discord.Client):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(intents=intents)
        self._did_broadcast = False

    async def on_ready(self) -> None:
        if self._did_broadcast:
            return
        self._did_broadcast = True

        guild = self.get_guild(GUILD_ID)
        if guild is None:
            LOGGER.error("Could not find guild with id %s", GUILD_ID)
            await self.close()
            return

        message = build_invite_message(INVITE_URL, EXTRA_LINK)
        sent_count = 0

        for member in guild.members:
            if member.bot:
                continue
            role_names = [role.name for role in member.roles]
            if not is_poe2_player(role_names, TARGET_ROLE_NAMES):
                continue

            if DRY_RUN:
                LOGGER.info("[DRY_RUN] Would send invite to %s", member)
                sent_count += 1
                continue

            try:
                await member.send(message)
                sent_count += 1
                await asyncio.sleep(1)
            except discord.Forbidden:
                LOGGER.warning("Cannot DM %s (DMs closed)", member)
            except discord.HTTPException as error:
                LOGGER.warning("Failed to DM %s: %s", member, error)

        LOGGER.info("Path of Exile 2 invite broadcast complete. Sent to %s users.", sent_count)
        await self.close()


if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("DISCORD_TOKEN is required")
    if not GUILD_ID:
        raise SystemExit("TARGET_GUILD_ID is required")
    if not INVITE_URL:
        raise SystemExit("INVITE_URL is required")
    bot = Poe2InviteBot()
    bot.run(TOKEN)
