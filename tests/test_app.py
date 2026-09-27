import unittest
from pathlib import Path
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def launch(self):
        return AppTest.from_file(str(APP), default_timeout=30).run()

    def test_initial_working_example_and_disabled_live_mode(self):
        app = self.launch()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric], ["2/6", "5/6", "1", "0"])
        button = next(b for b in app.button if b.label == "Run A/B evaluation")
        self.assertTrue(button.disabled)

    def test_save_review_and_gate_remains_hold(self):
        app = self.launch()
        next(s for s in app.selectbox if s.label == "Human verdict").select("Pass")
        next(a for a in app.text_area if a.label == "Evidence and reasoning").input("The candidate correctly gives 30 days and cites the supplied source.")
        next(b for b in app.button if b.label == "Save human review").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["reviews"]["C01"]["verdict"], "Pass")
        self.assertTrue(any("Hold for changes" in w.value for w in app.warning))

    def test_regression_view_and_upload_empty_state(self):
        app = self.launch()
        next(s for s in app.selectbox if s.label == "Cases to show").select("Regressions").run()
        self.assertFalse(app.exception)
        self.assertEqual(next(s for s in app.selectbox if s.label == "Inspect case").value, "C05")
        app.sidebar.radio[0].set_value("Your CSV").run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Upload the CSV" in i.value for i in app.info))

    def test_authorised_live_run_snapshots_prompts_and_resets_reviews(self):
        app = self.launch()
        app.secrets["OPENAI_API_KEY"] = "fake-key-for-mocked-test"
        app.secrets["RUN_ACCESS_CODE"] = "test-access"
        app.secrets["OPENAI_MODEL"] = "test-model"
        app.run()
        next(n for n in app.number_input if n.label.startswith("Cases in this run")).set_value(1)
        next(t for t in app.text_input if t.label == "Private pilot access code").input("test-access")
        app.checkbox[0].check()
        fake = {"text": "30 days [S1]", "model": "test-model", "usage": {"total_tokens": 12}, "latency_seconds": .1}
        with patch("provider.run_response", return_value=fake) as mock:
            next(b for b in app.button if b.label == "Run A/B evaluation").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(mock.call_count, 2)
        self.assertEqual(app.session_state["metadata"]["requests_attempted"], 2)
        self.assertEqual(len(app.session_state["run_cases"]), 1)
        self.assertIn("prompt_b_sha256", app.session_state["metadata"])
        self.assertTrue(any("Human review pending" in w.value for w in app.warning))

    def test_wrong_access_code_prevents_requests(self):
        app = self.launch()
        app.secrets["OPENAI_API_KEY"] = "fake-key-for-mocked-test"
        app.secrets["RUN_ACCESS_CODE"] = "expected"
        app.secrets["OPENAI_MODEL"] = "test-model"
        app.run()
        next(t for t in app.text_input if t.label == "Private pilot access code").input("wrong-🔒")
        app.checkbox[0].check()
        with patch("provider.run_response") as mock:
            next(b for b in app.button if b.label == "Run A/B evaluation").click().run()
        self.assertFalse(app.exception)
        mock.assert_not_called()
        self.assertTrue(any("incorrect" in e.value for e in app.error))


if __name__ == "__main__":
    unittest.main()
