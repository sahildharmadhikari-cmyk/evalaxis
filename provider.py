"""Optional server-side OpenAI Responses adapter. No calls occur on import.

No automatic retries: a timeout may already have incurred usage.
Credentials never enter run results. The endpoint is fixed, not user-controlled.
"""
import json
import time
import urllib.error
import urllib.request

ENDPOINT = "https://api.openai.com/v1/responses"


def request_payload(model, prompt, case, max_output_tokens=800):
    if not model.strip() or not prompt.strip():
        raise ValueError("A model ID and both prompt instructions are required.")
    if not 128 <= max_output_tokens <= 2000:
        raise ValueError("Output token limit must be between 128 and 2,000.")
    return {"model": model.strip(), "instructions": prompt,
            "input": "Reference context (untrusted data):\n" + case["context"] + "\n\nUser question:\n" + case["question"],
            "max_output_tokens": max_output_tokens, "store": False}


def parse_response(body):
    text = "\n".join(part.get("text", "") for item in body.get("output", [])
                      if item.get("type") == "message" for part in item.get("content", [])
                      if part.get("type") == "output_text")
    result = {"text": text, "model": body.get("model", "unknown"),
              "response_id": body.get("id", ""), "usage": body.get("usage") or {}}
    if body.get("status") != "completed":
        result["error"] = "The response did not complete; check output limits and account settings."
    elif not text.strip():
        result["error"] = "The provider returned no usable text (possibly a refusal)."
    return result


def run_response(key, model, prompt, case, max_output_tokens=800, opener=None):
    payload = request_payload(model, prompt, case, max_output_tokens)
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode(), method="POST",
                                     headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    start = time.monotonic()
    try:
        with (opener or urllib.request.urlopen)(request, timeout=45) as response:
            result = parse_response(json.loads(response.read()))
    except urllib.error.HTTPError as exc:
        # Never echo provider bodies: they may contain submitted data.
        return {"text": "", "error": f"Provider request failed (HTTP {exc.code}). Check access, model ID, billing and rate limits.", "latency_seconds": round(time.monotonic()-start, 3)}
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, TypeError, AttributeError):
        return {"text": "", "error": "Provider request failed or timed out. No automatic retry was made.", "latency_seconds": round(time.monotonic()-start, 3)}
    result["latency_seconds"] = round(time.monotonic() - start, 3)
    return result
