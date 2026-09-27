# EvalAxis

**A release-review workspace for small teams building AI knowledge assistants.**

Compare baseline and candidate responses, inspect explainable checks, record human verdicts and export a release-evidence pack.

Independent beta by Sahil Dharmadhikari, developed with AI assistance. Working product name. No customers, revenue, model-performance gains or production certifications are claimed.

## Try it

The app opens with six hand-written synthetic examples. They are prepared illustrations, not measured outputs from a model. The example candidate passes 5/6 automated case checks versus 2/6 for the baseline, but introduces one formatting regression. The release gate remains **Hold for changes**. These numbers must not be marketed as product performance.

You can upload a CSV containing your own test cases and responses. Optional private live runs call the OpenAI Responses API using the owner's server-side configuration. Live calls are disabled by default.

## Run locally or in a new GitHub Codespace

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m streamlit run app.py
```

Use Python 3.12. See [START_HERE.md](START_HERE.md) for beginner-friendly deployment steps and [docs/FOUNDER_PLAYBOOK.md](docs/FOUNDER_PLAYBOOK.md) for product strategy.

## Current capabilities

- Up to 50 test cases in a UTF-8 CSV (2 MB).
- Same-case A/B response comparison and regression detection.
- Required/forbidden phrase checks, word limits, JSON-object parsing and source-marker validation.
- Critical-case flags and an explicit rule-based review gate.
- Human Pass/Fail decisions with reasons and UTC timestamps.
- Readable HTML, structured JSON and spreadsheet-safe CSV exports.
- Optional live prompt comparison on the same configured model, capped at 10 cases and 40 requests per browser session; no automatic retries.
- Suite and prompt hashes, run timestamps, provider-returned model IDs, response IDs, token counts and observed request duration when available.

## Reading the results

An automated PASS means only that the configured checks passed. Phrase matching is lexical, not semantic. A source marker such as `[S1]` does not prove that the answer is supported by S1. The JSON check verifies a JSON object, not an application-specific schema. Assess correctness, usefulness and appropriateness manually against a suitable reference.

The denominator includes every case in the active run, including missing and errored responses. A regression is baseline PASS → candidate FAIL/ERROR. NOT RUN is incomplete work. Critical blockers include missing, failed or errored critical candidates. Human review never rewrites automated results.

The gate is Incomplete if any candidate is missing; Hold for changes if any candidate fails/errors, any human verdict fails, or a regression exists; Human review pending if automated checks pass but reviews are missing; otherwise Configured checks met. It is not production approval, a safety score or certification.

## Data contract

See [docs/DATA_CONTRACT.md](docs/DATA_CONTRACT.md). Keep all sample column names. `|` separates required phrases, forbidden phrases and allowed source IDs. `true`/`false` are required for booleans. Blank response columns are allowed. CSV exports prefix formula triggers with an apostrophe, so they are not byte-identical to untrusted source text.

## Data handling and beta limits

Uploads are processed on the Streamlit server. The app does not intentionally save uploaded data to disk or a database. Streamlit session memory is temporary; download reports before leaving. Live runs send selected context, questions and prompt instructions to OpenAI. They do not send the reference answer or test criteria. `store=false` is set, but this is not a zero-retention guarantee; provider policies still apply.

No permanent accounts, multi-user collaboration, global spend enforcement, immutable history, re-import of review reports, billing, production monitoring, tool execution or automatic deployment. An access code is a prototype safeguard, not enterprise authentication. Keep live pilots private. Public visitors can use prepared examples and import responses without any provider key.

## Project map

- `app.py`: interface and session workflow.
- `core.py`: CSV contract, evaluation rules, release gate and exports.
- `provider.py`: optional fixed-endpoint live API adapter.
- `data/sample_cases.csv`: invented test cases and responses.
- `tests/`: evaluation, input, output, mocked-provider and interface tests.
- `docs/`: strategy, roadmap, user stories, governance, Gamma prompt and launch copy.

## Verification

See [docs/VALIDATION.md](docs/VALIDATION.md). Automated and mocked tests do not establish real API compatibility with your account, public deployment health, or production readiness. Complete the launch checklist in your own deployment.

## Next development priorities

Validate the problem with small AI teams; expand meaningful test suites; then add authentication, durable versioned runs, spend controls, calibrated semantic evaluation and provider adapters as demand warrants. See the prioritised roadmap. No future capability is represented as already shipped.

## Technical references

- OpenAI Responses: https://developers.openai.com/api/reference/cli/resources/responses/methods/create
- Provider data controls: https://developers.openai.com/api/docs/guides/your-data
- Streamlit deployment: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
- Gamma publishing: https://help.gamma.app/en/articles/8429268-how-do-i-create-publish-a-site-in-gamma
