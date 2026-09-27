# Validation record

Date: 26 September 2026. Environment: Python 3.12, Streamlit 1.64.0, pandas 2.2.3.

## Completed

19 automated tests passed. Coverage includes:

- Known six-case example: baseline 2/6, candidate 5/6, four improvements, one regression, zero critical blockers and Hold for changes.
- Release gate: incomplete output, failures, missing human review, human failure and all configured checks met.
- Missing/errored candidates remain in denominators; critical errors count as blockers.
- Strict JSON-object validation and allowed/unknown source-marker behaviour.
- CSV schema, duplicate IDs, booleans, byte limits, UTF-8 and malformed rows.
- Required human-review rationale.
- HTML injection escaping and CSV spreadsheet-formula escaping.
- Provider payload excludes references and test criteria; storage disabled; no tool definitions.
- Mocked response extraction, refusal/incomplete handling, safe HTTP errors and no automatic retries.
- App initial load, filters, empty upload state, saving a review and disabled live mode.
- Mocked authorised A/B run: prompt metadata captured, correct selected-case count, two requests.
- Incorrect/non-ASCII access-code input makes no provider call.

## Review and corrections

- Replaced a deprecated dataframe width option with the supported width parameter.
- Made access-code comparison safe for non-ASCII input.
- Preserved failed/missing calls in result counts and stopped batches after provider errors.
- Kept human reviews separate from deterministic outcomes and kept example results labelled as synthetic.
- Explicitly stated that lexical checks and source markers do not prove correctness or grounding.

## Not established by these tests

No real OpenAI requests were made. Account access, billing, provider/model compatibility and latency/cost in real use are unverified. Provider tests use mock responses, not live service results.

Public Streamlit/Gamma deployment and real-user testing have not occurred in this environment. Desktop/mobile visual browser inspection remains a launch check: the local browser installation was unavailable. AppTest verifies application state and interactions, not final visual layout.

This is not a security audit, load test, model benchmark or proof of market demand. Follow START_HERE.md on the actual deployment before publishing launch claims.
