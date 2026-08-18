from __future__ import annotations

import os
from datetime import date
from io import BytesIO

from flask import Flask, render_template, request, send_file

from discordrec.invitation import (
    DEFAULT_COMMUNITY_NAME,
    DEFAULT_MARKETING_URL,
    DEFAULT_SIGNER,
    InvitationDetails,
    build_invitation_pdf,
    build_invitation_preview,
    sanitize_filename_part,
)

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "discordrec-invitation-dev-key")


def _form_defaults() -> dict[str, str]:
    return {
        "recipient_name": "",
        "marketing_url": DEFAULT_MARKETING_URL,
        "community_name": DEFAULT_COMMUNITY_NAME,
        "signer_name": DEFAULT_SIGNER,
        "personal_note": "",
    }


def _details_from_values(values: dict[str, str]) -> InvitationDetails:
    return InvitationDetails(
        recipient_name=values.get("recipient_name", ""),
        marketing_url=values.get("marketing_url", DEFAULT_MARKETING_URL),
        community_name=values.get("community_name", DEFAULT_COMMUNITY_NAME),
        signer_name=values.get("signer_name", DEFAULT_SIGNER),
        personal_note=values.get("personal_note", ""),
        letter_date=date.today(),
    )


@app.get("/")
def index():
    return render_template("index.html", values=_form_defaults(), preview=None, error=None)


@app.post("/")
def create_invitation():
    values = {
        "recipient_name": request.form.get("recipient_name", "").strip(),
        "marketing_url": request.form.get("marketing_url", DEFAULT_MARKETING_URL).strip()
        or DEFAULT_MARKETING_URL,
        "community_name": request.form.get("community_name", DEFAULT_COMMUNITY_NAME).strip()
        or DEFAULT_COMMUNITY_NAME,
        "signer_name": request.form.get("signer_name", DEFAULT_SIGNER).strip() or DEFAULT_SIGNER,
        "personal_note": request.form.get("personal_note", "").strip(),
    }
    action = request.form.get("action", "preview")

    try:
        details = _details_from_values(values)
    except ValueError as error:
        return render_template("index.html", values=values, preview=None, error=str(error)), 400

    if action == "download":
        pdf_bytes = build_invitation_pdf(details)
        filename = f"invitation-{sanitize_filename_part(details.recipient_name)}.pdf"
        return send_file(
            path_or_file=BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )

    preview = build_invitation_preview(details)
    return render_template("index.html", values=values, preview=preview, error=None)


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "5000"))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
