import unittest
from runtime.taskfit import evaluate_task_fit
from runtime.policy import transfer_action


class RuntimeTests(unittest.TestCase):
    def test_active_fit(self):
        result = evaluate_task_fit({"scores": {"genre_fit": 80, "decision_structure_fit": 90, "evidence_fit": 80, "added_value_fit": 80}})
        self.assertEqual(result["activation"], "active")

    def test_bootstrap_does_not_force_han_yu(self):
        result = evaluate_task_fit({"scores": {"genre_fit": 55, "decision_structure_fit": 85, "evidence_fit": 20, "added_value_fit": 35}})
        self.assertNotEqual(result["activation"], "active")

    def test_transfer_policy(self):
        self.assertEqual(transfer_action("high"), "revision_allowed")
        self.assertEqual(transfer_action("reject"), "abstain")


if __name__ == "__main__":
    unittest.main()
