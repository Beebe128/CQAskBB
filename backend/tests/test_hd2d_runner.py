import unittest

from backend.hd2d.run_prototype import build_render_payload


class TestHd2dRunner(unittest.TestCase):
    def test_build_render_payload_for_alttp(self):
        payload = build_render_payload("alttp")
        self.assertEqual(payload["game_id"], "alttp")
        self.assertGreater(payload["quad_count"], 0)

    def test_custom_camera_parameters(self):
        payload = build_render_payload("chrono_trigger", yaw_deg=5.0, pitch_deg=8.0, zoom=1.25)
        self.assertEqual(payload["camera"]["yaw_deg"], 5.0)
        self.assertEqual(payload["camera"]["pitch_deg"], 8.0)
        self.assertEqual(payload["camera"]["zoom"], 1.25)

    def test_unsupported_game_raises(self):
        with self.assertRaises(ValueError):
            build_render_payload("super_metroid")


if __name__ == "__main__":
    unittest.main()
