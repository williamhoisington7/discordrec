import unittest

from discordrec.poe2_inviter import build_invite_message, is_poe2_player, normalize_names


class Poe2InviterTests(unittest.TestCase):
    def test_normalize_names_removes_whitespace_and_case(self):
        self.assertEqual(normalize_names(["  PoE2", "Path Of Exile 2  ", ""]), {"poe2", "path of exile 2"})

    def test_is_poe2_player_true_when_member_has_matching_role(self):
        self.assertTrue(is_poe2_player(["Raider", "Path of Exile 2"]))

    def test_is_poe2_player_false_when_no_matching_role(self):
        self.assertFalse(is_poe2_player(["Raider", "General"] ))

    def test_build_invite_message_includes_optional_link(self):
        message = build_invite_message("https://discord.gg/example", "https://example.com/builds")
        self.assertIn("https://discord.gg/example", message)
        self.assertIn("https://example.com/builds", message)


if __name__ == "__main__":
    unittest.main()
