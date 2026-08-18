import unittest
from datetime import date
from io import BytesIO

from discordrec.invitation import (
    InvitationDetails,
    build_invitation_body,
    build_invitation_pdf,
    build_invitation_preview,
    sanitize_filename_part,
)


class InvitationTests(unittest.TestCase):
    def test_requires_recipient_name(self):
        with self.assertRaises(ValueError):
            InvitationDetails(recipient_name="   ")

    def test_build_invitation_body_includes_name_and_site_flow(self):
        details = InvitationDetails(
            recipient_name="Jamie Lee",
            marketing_url="wouldkillforpie.com",
            letter_date=date(2026, 8, 18),
        )
        body = build_invitation_body(details)
        self.assertIn("Jamie Lee", body)
        self.assertIn("https://wouldkillforpie.com", body)
        self.assertIn("Before joining our Discord server fully", body)
        self.assertIn("click the Discord link", body)
        self.assertIn("wouldkillforpie.com", body)

    def test_build_invitation_body_includes_optional_note(self):
        details = InvitationDetails(
            recipient_name="Sam",
            personal_note="You came highly recommended by a fellow exile.",
        )
        body = build_invitation_body(details)
        self.assertIn("You came highly recommended by a fellow exile.", body)

    def test_preview_uses_formal_structure(self):
        details = InvitationDetails(
            recipient_name="Taylor",
            letter_date=date(2026, 8, 18),
        )
        preview = build_invitation_preview(details)
        self.assertEqual(preview["salutation"], "Dear Taylor,")
        self.assertEqual(preview["date"], "August 18, 2026")
        self.assertEqual(preview["footer"], "wouldkillforpie.com")
        self.assertEqual(preview["header"], "Would Kill For PiE")

    def test_sanitize_filename_part(self):
        self.assertEqual(sanitize_filename_part("Jamie Lee!"), "Jamie-Lee")
        self.assertEqual(sanitize_filename_part("@@@"), "guest")

    def test_build_invitation_pdf_returns_pdf_bytes(self):
        details = InvitationDetails(recipient_name="Riley Quinn")
        pdf_bytes = build_invitation_pdf(details)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertGreater(len(pdf_bytes), 1000)

        buffer = BytesIO()
        build_invitation_pdf(details, output=buffer)
        self.assertTrue(buffer.getvalue().startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
