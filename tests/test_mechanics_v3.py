import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))
from mechanics_v3 import momentum_after_turn, momentum_after_victory, resolve_siege_pressure, victory_alarm_tier, compute_roster_losses

class Rules(unittest.TestCase):
    def test_momentum(self):
        self.assertEqual(momentum_after_victory(5, 2), 6)
        self.assertEqual(momentum_after_turn(2, False), 1)
        self.assertEqual(momentum_after_turn(2, True), 2)
        self.assertEqual(momentum_after_turn(0, False), 0)
        with self.assertRaises(ValueError): momentum_after_victory(1, 5)
    def test_siege(self):
        self.assertEqual(resolve_siege_pressure(.58, False, 0, 0, 1), 0)
        self.assertLess(resolve_siege_pressure(2, True, 90, 1, 1), resolve_siege_pressure(2, False, 20, 0, 1))
    def test_alarm(self):
        self.assertEqual([victory_alarm_tier(x) for x in (0,.50,.70,.85,.95)], [0,1,2,3,4])
        with self.assertRaises(ValueError): victory_alarm_tier(float("nan"))
    def test_roster(self):
        self.assertEqual(compute_roster_losses(0,100), 0)
        self.assertEqual(compute_roster_losses(2,100), .038)
        self.assertLessEqual(compute_roster_losses(200,1), .075)

if __name__ == "__main__": unittest.main()
