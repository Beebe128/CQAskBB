import unittest

from backend.hd2d.profiles import build_default_profiles
from backend.hd2d.prototype import PrototypeRenderer
from backend.hd2d.scenes import make_alttp_sample_frame, make_chrono_trigger_sample_frame


class TestHd2dPrototype(unittest.TestCase):
    def test_alttp_render_has_quads(self):
        profile = build_default_profiles()["alttp"]
        payload = PrototypeRenderer(profile).render(make_alttp_sample_frame())

        self.assertEqual(payload["game_id"], "alttp")
        self.assertGreater(payload["quad_count"], 0)
        first = payload["quads"][0]
        self.assertIn("screen", first)
        self.assertIn("brightness", first)

    def test_ui_layer_is_unlit(self):
        profile = build_default_profiles()["chrono_trigger"]
        payload = PrototypeRenderer(profile).render(make_chrono_trigger_sample_frame())
        ui = [q for q in payload["quads"] if q["layer"] == "ui"]
        self.assertTrue(ui)
        self.assertTrue(all(q["brightness"] == 1.0 for q in ui))


if __name__ == "__main__":
    unittest.main()
