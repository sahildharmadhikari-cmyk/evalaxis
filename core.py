"""Deterministic, explainable checks; no automatic semantic correctness claim."""
import csv
import hashlib
import html
import io
import json
import re
from datetime import datetime, timezone

VERSION = "0.1.0"
FIELDS = ["case_id", "category", "critical", "question", "context", "reference",
          "required_terms", "forbidden_terms", "max_words", "require_json", "source_ids",
          "response_a", "response_b"]
MAX_BYTES = 2 * 1024 * 1024
MAX_CASES = 50


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def terms(raw):
    return [t.strip() for t in raw.split("|") if t.strip()]


def parse_csv(blob):
    if len(blob) > MAX_BYTES:
        raise ValueError("Use a CSV of 2 MB or less.")
    try:
        text = blob.decode("utf-8-sig")
        if "\x00" in text:
            raise ValueError("Null characters are not supported.")
        rows = list(csv.reader(io.StringIO(text), strict=True))
    except (UnicodeDecodeError, csv.Error) as exc:
        raise ValueError("Use valid UTF-8 CSV with correctly quoted fields.") from exc
    if not rows:
        raise ValueError("The file is empty.")
    headers = [s.strip() for s in rows[0]]
    if len(set(headers)) != len(headers):
        raise ValueError("Column names must be unique.")
    if any(key not in headers for key in FIELDS):
        raise ValueError("Keep every column from the downloadable sample CSV, including blank response columns.")
    body = [r for r in rows[1:] if r]
    if not 1 <= len(body) <= MAX_CASES:
        raise ValueError("Include between 1 and 50 test cases.")
    cases, ids = [], set()
    for line, row in enumerate(body, 2):
        if len(row) != len(headers):
            raise ValueError(f"Row {line}: the number of fields does not match the header.")
        record = dict(zip(headers, row))
        case = {k: record[k].strip() for k in FIELDS}
        if not case["case_id"] or case["case_id"] in ids:
            raise ValueError(f"Row {line}: case_id must be non-empty and unique.")
        ids.add(case["case_id"])
        if len(case["case_id"]) > 80 or len(case["category"]) > 100:
            raise ValueError(f"Row {line}: keep IDs within 80 and categories within 100 characters.")
        if not case["question"] or not case["category"]:
            raise ValueError(f"Row {line}: question and category are required.")
        if any(len(case[k]) > 12000 for k in FIELDS):
            raise ValueError(f"Row {line}: each field must be at most 12,000 characters.")
        for key in ["critical", "require_json"]:
            if case[key].lower() not in ["true", "false"]:
                raise ValueError(f"Row {line}: {key} must be true or false.")
            case[key] = case[key].lower() == "true"
        try:
            case["max_words"] = int(case["max_words"])
        except ValueError as exc:
            raise ValueError(f"Row {line}: max_words must be a whole number.") from exc
        if not 1 <= case["max_words"] <= 2000:
            raise ValueError(f"Row {line}: max_words must be between 1 and 2,000.")
        for key in ["required_terms", "forbidden_terms", "source_ids"]:
            case[key] = terms(case[key])
        if any(not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", sid) for sid in case["source_ids"]):
            raise ValueError(f"Row {line}: use simple source IDs such as S1, separated by |.")
        cases.append(case)
    return cases


def csv_bytes(rows, columns):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        safe = {}
        for key in columns:
            value = row.get(key, "")
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False)
            if isinstance(value, bool):
                value = str(value).lower()
            value = str(value)
            if value.lstrip().startswith(("=", "+", "-", "@")) or value.startswith(("\t", "\r", "\n")):
                value = "'" + value
            safe[key] = value
        writer.writerow(safe)
    return out.getvalue().encode("utf-8-sig")


def check_response(case, text, error=None):
    if error:
        return {"status": "ERROR", "checks": [{"check": "Response generation", "passed": False, "detail": error}]}
    if not text.strip():
        return {"status": "NOT RUN", "checks": []}
    checks = []

    def add(name, passed, detail):
        checks.append({"check": name, "passed": bool(passed), "detail": detail})

    word_count = len(text.split())
    add("Word limit", word_count <= case["max_words"], f"{word_count} words; limit {case['max_words']}")
    lower = " ".join(text.casefold().split())
    for phrase in case["required_terms"]:
        add("Required phrase", " ".join(phrase.casefold().split()) in lower, phrase)
    for phrase in case["forbidden_terms"]:
        add("Forbidden phrase absent", " ".join(phrase.casefold().split()) not in lower, phrase)
    if case["require_json"]:
        try:
            def reject_constant(value):
                raise ValueError(value)
            parsed = json.loads(text, parse_constant=reject_constant)
            valid = isinstance(parsed, dict)
        except (json.JSONDecodeError, ValueError):
            valid = False
        add("JSON object", valid, "Must parse as a JSON object without markdown fences.")
    if case["source_ids"]:
        found = set(re.findall(r"\[([A-Za-z0-9_-]+)\]", text))
        invalid = sorted(found - set(case["source_ids"]))
        add("Source markers", bool(found) and not invalid,
            f"Found: {', '.join(sorted(found)) or 'none'}; allowed: {', '.join(case['source_ids'])}. Checks markers only, not whether claims are supported.")
    return {"status": "PASS" if all(c["passed"] for c in checks) else "FAIL", "checks": checks}


def evaluate(cases, outputs):
    results = []
    for case in cases:
        output = outputs.get(case["case_id"], {})
        row = {"case_id": case["case_id"], "category": case["category"], "critical": case["critical"]}
        for variant in ["a", "b"]:
            value = output.get(variant, {})
            row[variant] = {**value, **check_response(case, value.get("text", ""), value.get("error"))}
        row["regression"] = row["a"]["status"] == "PASS" and row["b"]["status"] in ["FAIL", "ERROR"]
        row["improvement"] = row["a"]["status"] in ["FAIL", "ERROR"] and row["b"]["status"] == "PASS"
        results.append(row)
    return results


def summary(results, reviews):
    n = len(results)
    a_pass = sum(r["a"]["status"] == "PASS" for r in results)
    b_pass = sum(r["b"]["status"] == "PASS" for r in results)
    regressions = sum(r["regression"] for r in results)
    missing = sum(r["b"]["status"] == "NOT RUN" for r in results)
    blocked = sum(r["critical"] and r["b"]["status"] != "PASS" for r in results)
    human_fail = sum(reviews.get(r["case_id"], {}).get("verdict") == "Fail" for r in results)
    human_done = sum(r["case_id"] in reviews for r in results)
    candidate_fail = sum(r["b"]["status"] in ["FAIL", "ERROR"] for r in results)
    if n == 0 or missing:
        gate = "Incomplete"
    elif candidate_fail or human_fail or regressions:
        gate = "Hold for changes"
    elif human_done < n:
        gate = "Human review pending"
    else:
        gate = "Configured checks met"
    return {"case_count": n, "baseline_pass": a_pass, "candidate_pass": b_pass,
            "baseline_rate": a_pass / n if n else None, "candidate_rate": b_pass / n if n else None,
            "regressions": regressions, "improvements": sum(r["improvement"] for r in results),
            "candidate_missing": missing, "candidate_failures": candidate_fail,
            "critical_blockers": blocked, "human_reviews": human_done, "human_failures": human_fail,
            "gate": gate}


def record_review(verdict, rationale):
    if verdict not in ["Pass", "Fail"] or not rationale.strip():
        raise ValueError("Select Pass or Fail and explain your assessment.")
    if len(rationale) > 2000:
        raise ValueError("Keep your assessment within 2,000 characters.")
    return {"verdict": verdict, "rationale": rationale.strip(), "reviewed_at_utc": now()}


def make_report(cases, outputs, metadata, reviews):
    results = evaluate(cases, outputs)
    return {"product": "EvalAxis", "version": VERSION, "generated_at_utc": now(),
            "run": metadata, "suite_sha256": digest(cases), "summary": summary(results, reviews),
            "cases": cases, "results": results, "human_reviews": reviews,
            "limitations": ["Automated checks are heuristics, not measurements of factual accuracy or safety.",
                            "Phrase checks use case-insensitive substrings, not semantic equivalence.",
                            "Source checks validate markers, not factual grounding.",
                            "The gate is a rule-based review aid, not certification or production approval.",
                            "Prepared examples are illustrative; no real model performance is implied.",
                            "Single-run results vary; no statistical significance is asserted.",
                            "Only the latest human review is retained per case; no immutable audit history."]}


def html_report(report):
    esc = lambda x: html.escape(str(x), quote=True)
    details = []
    lookup = {c["case_id"]: c for c in report["cases"]}
    for row in report["results"]:
        c = lookup[row["case_id"]]
        review = report["human_reviews"].get(row["case_id"], {})
        check_html = "".join(f"<li>{esc(v)}: {esc(check['check'])} — {'pass' if check['passed'] else 'fail'} — {esc(check['detail'])}</li>"
                             for v in ["a", "b"] for check in row[v]["checks"])
        details.append(f"<section><h2>{esc(row['case_id'])} · {esc(row['category'])}</h2>"
                       f"<p><b>Question:</b> {esc(c['question'])}</p><p><b>Reference:</b> {esc(c['reference'])}</p>"
                       f"<h3>Baseline · {esc(row['a']['status'])}</h3><pre>{esc(row['a'].get('text',''))}</pre>"
                       f"<h3>Candidate · {esc(row['b']['status'])}</h3><pre>{esc(row['b'].get('text',''))}</pre>"
                       f"<ul>{check_html}</ul><p><b>Human review:</b> {esc(review.get('verdict','Pending'))} — {esc(review.get('rationale',''))}</p></section>")
    return ("<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>EvalAxis review report</title><style>body{font:16px/1.6 system-ui,sans-serif;color:#14213d;max-width:960px;margin:40px auto;padding:0 24px}"
            "section{border-top:1px solid #ccd3e1;margin-top:28px;padding-top:18px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f0f3fa;padding:16px}h1{font-size:36px}"
            "@media print{section{break-inside:avoid}}</style><h1>EvalAxis / release review</h1>"
            f"<p>{esc(report['generated_at_utc'])}</p><p><b>{esc(report['summary']['gate'])}</b></p>"
            f"<p>Source: {esc(report['run'].get('source',''))}</p><pre>{esc(json.dumps(report['summary'],indent=2))}</pre>"
            + "".join(details) + "<section><h2>Run metadata</h2><pre>" + esc(json.dumps(report['run'], indent=2))
            + "</pre><h2>Limits</h2><ul>" + "".join(f"<li>{esc(x)}</li>" for x in report["limitations"])
            + "</ul></section></html>").encode()
