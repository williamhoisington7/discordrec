"""discordrec package: invite helpers and personalized invitation letters."""

from discordrec.invitation import (
    DEFAULT_MARKETING_URL,
    InvitationDetails,
    build_invitation_body,
    build_invitation_pdf,
    sanitize_filename_part,
)
from discordrec.poe2_inviter import (
    DEFAULT_POE2_ROLE_ALIASES,
    build_invite_message,
    is_poe2_player,
    normalize_names,
)

__all__ = [
    "DEFAULT_MARKETING_URL",
    "DEFAULT_POE2_ROLE_ALIASES",
    "InvitationDetails",
    "build_invitation_body",
    "build_invitation_pdf",
    "build_invite_message",
    "is_poe2_player",
    "normalize_names",
    "sanitize_filename_part",
]
