import unittest

import core


class TestCore(unittest.TestCase):
    def test_01_no_duplicate_distill(self):
        state = core.new_game()
        self.assertTrue(core.distill(state, 1, 10))
        self.assertFalse(core.distill(state, 1, 10))

    def test_02_tower_capacity(self):
        state = core.new_game()
        state["tower_load"] = 90
        result = core.distill(state, 2, 20)
        self.assertFalse(result)

    def test_03_temp_boundary(self):
        state = core.new_game()
        self.assertEqual(core.check_temp(state, 35), "over")

    def test_04_cancel_releases_catalyst(self):
        state = core.new_game()
        state["catalyst"] = 8
        core.cancel_distill(state, 1)
        self.assertEqual(state["catalyst"], 10)

    def test_05_no_produce_when_inactive(self):
        state = core.new_game()
        state["catalyst_active"] = False
        result = core.produce(state, 5)
        self.assertFalse(result)

    def test_06_leak_once(self):
        state = core.new_game()
        core.leak(state)
        self.assertEqual(state["safety"], 90)

    def test_07_no_output_abnormal_pressure(self):
        state = core.new_game()
        state["pressure"] = 0
        result = core.output(state, 5)
        self.assertFalse(result)

    def test_08_load_preserves_batch(self):
        state = core.new_game()
        state["batch_id"] = 6
        loaded = core.load_state(core.save_state(state))
        self.assertEqual(loaded["batch_id"], 6)


if __name__ == "__main__":
    unittest.main()
