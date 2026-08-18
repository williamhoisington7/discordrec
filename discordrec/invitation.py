from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from io import BytesIO
from typing import BinaryIO

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

DEFAULT_MARKETING_URL = "https://wouldkillforpie.com"
DEFAULT_COMMUNITY_NAME = "Would Kill For PiE"
DEFAULT_SIGNER = "The Would Kill For PiE Community"

# Theme aligned with dark-fantasy / PoE-inspired WKFP graphics.
THEME_BG = HexColor("#140c0a")
THEME_PANEL = HexColor("#1c1210")
THEME_INK = HexColor("#f3e6cf")
THEME_MUTED = HexColor("#b9a48a")
THEME_GOLD = HexColor("#d4a84b")
THEME_GOLD_SOFT = HexColor("#a67c2d")
THEME_CRIMSON = HexColor("#8b1e2d")
THEME_RULE = HexColor("#5c4030")


@dataclass(frozen=True)
class InvitationDetails:
    """Structured fields for a single personalized invitation letter."""

    recipient_name: str
    marketing_url: str = DEFAULT_MARKETING_URL
    community_name: str = DEFAULT_COMMUNITY_NAME
    signer_name: str = DEFAULT_SIGNER
    personal_note: str = ""
    letter_date: date | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "recipient_name", _clean_required_name(self.recipient_name))
        object.__setattr__(self, "marketing_url", _clean_url(self.marketing_url) or DEFAULT_MARKETING_URL)
        object.__setattr__(self, "community_name", (self.community_name or DEFAULT_COMMUNITY_NAME).strip())
        object.__setattr__(self, "signer_name", (self.signer_name or DEFAULT_SIGNER).strip())
        object.__setattr__(self, "personal_note", (self.personal_note or "").strip())
        object.__setattr__(self, "letter_date", self.letter_date or date.today())


def _clean_required_name(value: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        raise ValueError("Recipient name is required.")
    if len(cleaned) > 120:
        raise ValueError("Recipient name must be 120 characters or fewer.")
    return cleaned


def _clean_url(value: str | None) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        return ""
    if not re.match(r"^https?://", cleaned, flags=re.IGNORECASE):
        cleaned = f"https://{cleaned}"
    return cleaned


def sanitize_filename_part(value: str) -> str:
    """Turn a display name into a safe PDF filename fragment."""
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", (value or "").strip())
    cleaned = cleaned.strip("-._")
    return cleaned or "guest"


def build_invitation_body(details: InvitationDetails) -> str:
    """Return the plain-text body of the formal invitation letter.

    Invitees are directed to the recruitment site first so they can understand
    the community. Discord is joined only through the link on that site.
    """
    site = details.marketing_url
    paragraphs = [
        (
            f"It is with sincere pleasure that {details.community_name} extends this "
            f"personal invitation to you, {details.recipient_name}."
        ),
        (
            "Before joining our Discord server fully, we ask every invited guest to "
            f"visit our recruitment page at {site}. That page is the home of our "
            "community preview: who we are, what we value, and what life among fellow "
            "exiles feels like."
        ),
        (
            f"Please begin at {site}. Take your time reviewing the site. When you "
            "decide you are ready to join the Discord server, click the Discord link "
            "presented on wouldkillforpie.com. That is the official path into the "
            "server; no separate invite is required from this letter."
        ),
    ]

    if details.personal_note:
        paragraphs.append(details.personal_note)

    paragraphs.append(
        "We would be honored to welcome you after you have explored "
        f"{site}. Thank you for considering this invitation."
    )
    return "\n\n".join(paragraphs)


def build_invitation_preview(details: InvitationDetails) -> dict[str, str]:
    """Return structured preview fields for the web UI."""
    return {
        "header": details.community_name,
        "tagline": "A Personal Invitation",
        "date": details.letter_date.strftime("%B %d, %Y"),
        "salutation": f"Dear {details.recipient_name},",
        "body": build_invitation_body(details),
        "closing": "With warm regards,",
        "signer": details.signer_name,
        "footer": details.marketing_url.replace("https://", "").replace("http://", ""),
        "marketing_url": details.marketing_url,
    }


def build_invitation_pdf(details: InvitationDetails, output: BinaryIO | None = None) -> bytes:
    """Render a formal single-page invitation PDF and return its bytes."""
    buffer: BinaryIO = output if output is not None else BytesIO()
    preview = build_invitation_preview(details)

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=0.95 * inch,
        rightMargin=0.95 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title=f"Invitation for {details.recipient_name}",
        author=details.community_name,
    )

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(
        "InviteHeader",
        parent=styles["Heading1"],
        fontName="Times-Bold",
        fontSize=26,
        leading=30,
        textColor=THEME_GOLD,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    tagline_style = ParagraphStyle(
        "InviteTagline",
        parent=styles["Normal"],
        fontName="Times-Italic",
        fontSize=12,
        leading=16,
        textColor=THEME_MUTED,
        alignment=TA_CENTER,
        spaceAfter=18,
    )
    date_style = ParagraphStyle(
        "InviteDate",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=11,
        leading=14,
        textColor=THEME_MUTED,
        alignment=TA_RIGHT,
        spaceAfter=18,
    )
    body_style = ParagraphStyle(
        "InviteBody",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=12,
        leading=18,
        textColor=THEME_INK,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
    )
    salutation_style = ParagraphStyle(
        "InviteSalutation",
        parent=body_style,
        textColor=THEME_GOLD,
        spaceBefore=4,
        spaceAfter=14,
    )
    closing_style = ParagraphStyle(
        "InviteClosing",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=12,
        leading=16,
        textColor=THEME_INK,
        spaceBefore=10,
        spaceAfter=2,
    )
    signer_style = ParagraphStyle(
        "InviteSigner",
        parent=styles["Normal"],
        fontName="Times-Bold",
        fontSize=12,
        leading=16,
        textColor=THEME_GOLD,
        spaceAfter=18,
    )
    footer_style = ParagraphStyle(
        "InviteFooter",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10,
        leading=13,
        textColor=THEME_MUTED,
        alignment=TA_CENTER,
    )

    story = [
        Paragraph(_escape_xml(preview["header"]), header_style),
        Paragraph(_escape_xml(preview["tagline"]), tagline_style),
        HRFlowable(width="100%", thickness=1.5, color=THEME_CRIMSON, spaceBefore=0, spaceAfter=3),
        HRFlowable(width="100%", thickness=0.6, color=THEME_GOLD_SOFT, spaceBefore=0, spaceAfter=16),
        Paragraph(_escape_xml(preview["date"]), date_style),
        Paragraph(_escape_xml(preview["salutation"]), salutation_style),
    ]

    for paragraph in preview["body"].split("\n\n"):
        story.append(Paragraph(_escape_xml(paragraph), body_style))

    story.extend(
        [
            Spacer(1, 0.15 * inch),
            Paragraph(_escape_xml(preview["closing"]), closing_style),
            Paragraph(_escape_xml(preview["signer"]), signer_style),
            HRFlowable(width="100%", thickness=0.6, color=THEME_RULE, spaceBefore=8, spaceAfter=10),
            Paragraph(_escape_xml(preview["footer"]), footer_style),
        ]
    )

    def _draw_frame(canvas, _doc) -> None:
        canvas.saveState()
        width, height = letter
        canvas.setFillColor(THEME_BG)
        canvas.rect(0, 0, width, height, fill=1, stroke=0)

        canvas.setFillColor(THEME_PANEL)
        canvas.roundRect(0.38 * inch, 0.38 * inch, width - 0.76 * inch, height - 0.76 * inch, 8, fill=1, stroke=0)

        canvas.setStrokeColor(THEME_CRIMSON)
        canvas.setLineWidth(2)
        canvas.rect(0.48 * inch, 0.48 * inch, width - 0.96 * inch, height - 0.96 * inch)

        canvas.setStrokeColor(THEME_GOLD)
        canvas.setLineWidth(0.8)
        canvas.rect(0.58 * inch, 0.58 * inch, width - 1.16 * inch, height - 1.16 * inch)

        # Corner ornaments
        ornament = 0.28 * inch
        for x, y in (
            (0.58 * inch, height - 0.58 * inch - ornament),
            (width - 0.58 * inch - ornament, height - 0.58 * inch - ornament),
            (0.58 * inch, 0.58 * inch),
            (width - 0.58 * inch - ornament, 0.58 * inch),
        ):
            canvas.setFillColor(THEME_GOLD)
            canvas.circle(x + ornament / 2, y + ornament / 2, 2.2, fill=1, stroke=0)

        canvas.restoreState()

    doc.build(story, onFirstPage=_draw_frame, onLaterPages=_draw_frame)

    if hasattr(buffer, "getvalue"):
        return buffer.getvalue()
    if hasattr(buffer, "seek"):
        buffer.seek(0)
    return b""


def _escape_xml(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
