import unittest

from backend.api import app


class TestHd2dApi(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_hd2d_endpoint_success(self):
        response = self.client.get("/hd2d/prototype?game=alttp&yaw=4&pitch=9&zoom=1.05")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["game_id"], "alttp")
        self.assertEqual(payload["camera"]["yaw_deg"], 4.0)
        self.assertEqual(payload["camera"]["pitch_deg"], 9.0)
        self.assertEqual(payload["camera"]["zoom"], 1.05)
        self.assertGreater(payload["quad_count"], 0)

    def test_hd2d_endpoint_invalid_game(self):
        response = self.client.get("/hd2d/prototype?game=invalid")
        self.assertEqual(response.status_code, 400)
        payload = response.get_json()
        self.assertIn("Unsupported game", payload["error"])


if __name__ == "__main__":
    unittest.main()
