import json
import tempfile
import unittest
from pathlib import Path

from runtime.core import build_skill, dump_json
from runtime.personal import build_personal_skill, init_personal_profile, record_revision
from runtime.policy import transfer_action
from runtime.taskfit import evaluate_task_fit


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

    def test_writer_build_preserves_coaching_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = root / "data" / "demo"
            (base / "heuristics").mkdir(parents=True)
            dump_json(base / "writer_profile.json", {"name": "Demo Writer"})
            dump_json(base / "heuristics" / "H1.json", {
                "heuristic_id": "H1",
                "name": "Demo",
                "lens_family": "revision_judgment",
                "decision_structure": "A concrete decision structure.",
                "rule": "Keep the governing move, not borrowed wording.",
                "operational_actions": ["Mark the function of each paragraph."],
                "diagnostic_questions": ["Could this sentence survive unchanged in another topic?"],
                "boundary_conditions": ["Do not remove necessary technical terms."],
                "failure_signals": ["The rewrite merely swaps one cliché for another."],
                "supporting_episodes": ["E1", "E2"],
                "specificity": {"writer_added_delta": "A test delta."},
                "composition_audit": {"fabrication_risk": "low"},
                "routing": {"lens_eligibility": "active_lens"}
            })
            output = build_skill("demo", root=root)
            text = output.read_text(encoding="utf-8")
            self.assertIn("Operational actions", text)
            self.assertIn("Diagnostic questions", text)
            self.assertIn("Boundary conditions", text)
            self.assertIn("Writer-added delta", text)
            self.assertIn("Supporting Episodes", text)

    def test_personal_revision_promotes_repeated_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # minimal policy required by personal learning
            (root / "config").mkdir(parents=True)
            (root / "config" / "policy.json").write_text(json.dumps({
                "personal_learning": {
                    "require_explicit_feedback": True,
                    "candidate_after": 1,
                    "provisional_after": 2,
                    "validated_after": 3
                }
            }), encoding="utf-8")
            init_personal_profile("Demo", "demo", root=root)
            rule = "事实已经能说明问题时，不再补一个总结句。"
            for i in range(3):
                record_revision("demo", {
                    "episode_id": f"REV-{i}",
                    "context": "公众号改稿",
                    "platform": "wechat",
                    "original_text": "原稿",
                    "final_text": "终稿",
                    "user_feedback": "删除多余总结。",
                    "candidate_personal_rules": [rule]
                }, root=root)
            profile = json.loads((root / "personal" / "demo" / "style_profile.json").read_text(encoding="utf-8"))
            self.assertEqual(profile["personal_heuristics"][0]["confidence"], "validated")
            self.assertEqual(profile["personal_heuristics"][0]["evidence_count"], 3)
            skill = build_personal_skill("demo", root=root)
            self.assertIn(rule, skill.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
