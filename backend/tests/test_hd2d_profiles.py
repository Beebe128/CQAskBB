import unittest

from backend.hd2d.frame_graph import FrameGraph, Layer, LayerType, Sprite
from backend.hd2d.profiles import build_default_profiles


class TestHd2dProfiles(unittest.TestCase):
    def test_contains_requested_games(self):
        profiles = build_default_profiles()
        self.assertIn("alttp", profiles)
        self.assertIn("chrono_trigger", profiles)

    def test_depth_table_uses_profile_override(self):
        graph = FrameGraph(width=256, height=224)
        graph.add_layer(Layer(name="bg_mid", layer_type=LayerType.BG, priority=1))
        graph.add_layer(Layer(name="sprites", layer_type=LayerType.SPRITE, priority=2))

        table = graph.depth_table({"bg_mid": -3.0})
        self.assertEqual(table["bg_mid"], -3.0)
        self.assertEqual(table["sprites"], 1.0)

    def test_sprite_bounds(self):
        graph = FrameGraph(width=256, height=224)
        graph.add_layer(
            Layer(
                name="sprites",
                layer_type=LayerType.SPRITE,
                priority=1,
                sprites=[Sprite(sprite_id=1, x=4, y=8, width=16, height=24)],
            )
        )

        self.assertEqual(list(graph.sprite_bounds()), [(4, 8, 20, 32)])


if __name__ == "__main__":
    unittest.main()
