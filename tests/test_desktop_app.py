import unittest
from types import SimpleNamespace

from desktop_app import configure_webview_downloads


class DesktopAppTests(unittest.TestCase):
    def test_configure_webview_downloads_enables_attachments(self):
        fake_webview = SimpleNamespace(settings={"ALLOW_DOWNLOADS": False})
        configure_webview_downloads(fake_webview)
        self.assertTrue(fake_webview.settings["ALLOW_DOWNLOADS"])


if __name__ == "__main__":
    unittest.main()
