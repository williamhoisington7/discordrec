import unittest

from app import app


class InvitationAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_index_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"wouldkillforpie.com", response.data)

    def test_preview_personalizes_letter(self):
        response = self.client.post(
            "/",
            data={
                "recipient_name": "Test User",
                "marketing_url": "https://wouldkillforpie.com",
                "community_name": "Would Kill For PiE",
                "signer_name": "The Would Kill For PiE Community",
                "personal_note": "",
                "action": "preview",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Dear Test User", response.data)
        self.assertIn(b"Before joining our Discord server fully", response.data)

    def test_download_returns_pdf(self):
        response = self.client.post(
            "/",
            data={
                "recipient_name": "Test User",
                "action": "download",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.startswith(b"%PDF"))
        self.assertIn("pdf", response.headers.get("Content-Type", ""))


if __name__ == "__main__":
    unittest.main()
