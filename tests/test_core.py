import json
import unittest
from pathlib import Path

from core import (FIELDS, check_response, csv_bytes, evaluate, html_report, make_report,
                  parse_csv, record_review, summary)

SAMPLE = Path(__file__).resolve().parents[1] / "data/sample_cases.csv"


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = parse_csv(SAMPLE.read_bytes())
        self.outputs = {c["case_id"]: {"a": {"text": c["response_a"]}, "b": {"text": c["response_b"]}}
                        for c in self.cases}

    def test_demo_has_expected_regression_and_no_false_release(self):
        rows = evaluate(self.cases, self.outputs)
        result = summary(rows, {})
        self.assertEqual(result["baseline_pass"], 2)
        self.assertEqual(result["candidate_pass"], 5)
        self.assertEqual(result["regressions"], 1)
        self.assertEqual(result["improvements"], 4)
        self.assertEqual(result["critical_blockers"], 0)
        self.assertEqual(result["gate"], "Hold for changes")

    def test_gate_requires_completed_responses_and_human_review(self):
        case = self.cases[-1]
        outputs = {case["case_id"]: self.outputs[case["case_id"]]}
        rows = evaluate([case], outputs)
        self.assertEqual(summary(rows, {})["gate"], "Human review pending")
        reviews = {case["case_id"]: record_review("Pass", "The clarification request matches the reference.")}
        self.assertEqual(summary(rows, reviews)["gate"], "Configured checks met")
        reviews[case["case_id"]] = record_review("Fail", "The reference is incomplete.")
        self.assertEqual(summary(rows, reviews)["gate"], "Hold for changes")
        rows = evaluate([case], {})
        self.assertEqual(summary(rows, {})["gate"], "Incomplete")

    def test_missing_and_failed_requests_remain_in_denominator(self):
        self.outputs["C01"]["b"] = {"text": ""}
        self.outputs["C02"]["b"] = {"text": "partial", "error": "timeout"}
        result = summary(evaluate(self.cases, self.outputs), {})
        self.assertEqual(result["case_count"], 6)
        self.assertEqual(result["candidate_pass"], 3)
        self.assertEqual(result["critical_blockers"], 1)
        self.assertEqual(result["candidate_rate"], .5)

    def test_json_strictness(self):
        c = self.cases[4]
        for text in ['```json {"status":"pending"} ```', '{"status":"pending","x":NaN}', '"pending"']:
            self.assertEqual(check_response(c, text)["status"], "FAIL")
        self.assertEqual(check_response(c, '{"status":"pending"}')["status"], "PASS")

    def test_citation_presence_and_unknown_marker(self):
        c = self.cases[0]
        self.assertEqual(check_response(c, "30 days")["status"], "FAIL")
        self.assertEqual(check_response(c, "30 days [S99]")["status"], "FAIL")
        self.assertEqual(check_response(c, "30 days [S1] [S99]")["status"], "FAIL")
        self.assertEqual(check_response(c, "30 days [S1]")["status"], "PASS")

    def test_schema_rejects_duplicate_ids_and_invalid_booleans(self):
        raw = SAMPLE.read_text()
        for content in [raw.replace("C02,", "C01,"), raw.replace("false,", "maybe,", 1), "case_id\n1"]:
            with self.assertRaises(ValueError):
                parse_csv(content.encode())

    def test_utf8_size_and_shape(self):
        for blob in [b"\xff", b"x" * (2*1024*1024+1), b"", (",".join(FIELDS) + "\nx,y\n").encode()]:
            with self.assertRaises(ValueError):
                parse_csv(blob)

    def test_review_requires_a_reason(self):
        with self.assertRaises(ValueError):
            record_review("Pass", " ")
        with self.assertRaises(ValueError):
            record_review("Maybe", "Not sure")

    def test_export_escapes_formulas_and_html(self):
        csv = csv_bytes([{"value": "  =HYPERLINK(1)"}], ["value"]).decode("utf-8-sig")
        self.assertIn("'  =HYPERLINK", csv)
        self.outputs["C01"]["b"]["text"] = "<script>alert(1)</script>"
        report = make_report(self.cases, self.outputs, {"source": "test"}, {})
        page = html_report(report).decode()
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)
        json.dumps(report, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
