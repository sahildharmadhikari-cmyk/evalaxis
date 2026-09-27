import io
import json
import unittest
import urllib.error

from provider import ENDPOINT, parse_response, request_payload, run_response


class ProviderTests(unittest.TestCase):
    def setUp(self):
        self.case = {"context": "[S1] Source content", "question": "Question", "reference": "SECRET_REFERENCE", "required_terms": ["SECRET_TARGET"]}

    def test_model_input_does_not_leak_answer_or_criteria(self):
        body = request_payload("a-model", "instructions", self.case)
        encoded = json.dumps(body)
        self.assertNotIn("SECRET_REFERENCE", encoded)
        self.assertNotIn("SECRET_TARGET", encoded)
        self.assertFalse(body["store"])
        self.assertNotIn("tools", body)

    def test_completed_text_and_usage(self):
        body = {"status": "completed", "id": "resp_test", "model": "test", "usage": {"total_tokens": 20},
                "output": [{"type": "reasoning"}, {"type": "message", "content": [{"type": "output_text", "text": "hello"}]}]}
        result = parse_response(body)
        self.assertEqual(result["text"], "hello")
        self.assertEqual(result["usage"]["total_tokens"], 20)
        self.assertNotIn("error", result)

    def test_refusal_and_incomplete_are_not_passes(self):
        self.assertIn("error", parse_response({"status": "completed", "output": []}))
        self.assertIn("error", parse_response({"status": "incomplete", "output": []}))

    def test_mock_request_fixed_endpoint_and_no_key_in_result(self):
        def fake_open(request, timeout):
            self.assertEqual(request.full_url, ENDPOINT)
            self.assertEqual(timeout, 45)
            self.assertFalse(json.loads(request.data)["store"])
            return io.BytesIO(json.dumps({"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": "ok"}]}]}).encode())
        result = run_response("test-key-not-real", "model", "instructions", self.case, opener=fake_open)
        self.assertEqual(result["text"], "ok")
        self.assertNotIn("test-key-not-real", json.dumps(result))

    def test_http_error_does_not_echo_body_or_retry(self):
        calls = []
        def fail(request, timeout):
            calls.append(1)
            raise urllib.error.HTTPError(ENDPOINT, 429, "private message", {}, io.BytesIO(b"sensitive provider body"))
        result = run_response("key", "model", "instructions", self.case, opener=fail)
        self.assertEqual(len(calls), 1)
        self.assertIn("429", result["error"])
        self.assertNotIn("private", json.dumps(result))
        self.assertNotIn("sensitive", json.dumps(result))


if __name__ == "__main__":
    unittest.main()
