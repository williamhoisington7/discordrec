from __future__ import annotations

from typing import Iterable, Sequence

DEFAULT_POE2_ROLE_ALIASES = ("path of exile 2", "poe2")


def normalize_names(names: Iterable[str]) -> set[str]:
    return {name.strip().lower() for name in names if name and name.strip()}


def is_poe2_player(member_role_names: Sequence[str], target_role_names: Iterable[str] | None = None) -> bool:
    target = normalize_names(target_role_names or DEFAULT_POE2_ROLE_ALIASES)
    roles = normalize_names(member_role_names)
    return bool(target & roles)


def build_invite_message(invite_url: str, extra_link: str | None = None) -> str:
    message = (
        "Hey! You are receiving this because you have the Path of Exile 2 role.\n"
        f"Join us here: {invite_url}"
    )
    if extra_link:
        message += f"\nMore info: {extra_link}"
    return message
