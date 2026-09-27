# Governance and operating boundaries

## Evidence, not certification

The current release checks visible response properties. It does not estimate factual accuracy, robustness against all attacks, bias, legal compliance or suitability for consequential decisions. Avoid an unexplained composite “trust score”. Human assessment must have a task-specific reference and documented reasons.

## Data flow

CSV → Streamlit server session → deterministic checks → review → downloads.

Optional private live flow: prompt instructions + question + supplied context → fixed OpenAI Responses endpoint → generated text + available provider metadata → checks/review/downloads. Reference answers, expected phrases and human verdicts are not sent as generation instructions.

The app has no database, uploaded-data disk writes, model tools, arbitrary HTTP endpoints or browser execution of generated content. Responses render as plain text. Exported HTML escapes supplied content; spreadsheet formula triggers are escaped in CSV. These are implemented safeguards, not a security audit.

## Sensitive information

Public beta is for public or synthetic content. Do not upload private customer records, employee information, credentials or employer documents. Reports include submitted content and prompts. API credentials stay in server-side secrets and are excluded from reports and expected errors.

`store=false` disables provider response storage for later retrieval, but does not mean there is no provider retention. Review the provider's current data controls before any real-data pilot: https://developers.openai.com/api/docs/guides/your-data

## Human oversight

Human verdicts require a reason. They cannot erase automated failures. Only the latest verdict per case remains in the session; this is not an immutable audit log. Refresh, disconnect, dataset change or rerun can lose/reset work. Export before changing runs.

## Usage and errors

Live runs require the configured API key, model ID and access code, plus an explicit usage acknowledgement. Maximum 10 cases/run and 40 requests/session. Session controls can be reset by reconnecting; no global rate limit or budget enforcement exists. Keep live mode private until genuine authentication and central usage controls are built.

Provider requests have a timeout and no automatic retry. A timed-out request may still incur usage. An error stops the batch; unattempted cases remain NOT RUN and are not silently removed from reported denominators.

## Before serving real teams

Define user roles and authentication; implement durable versioned records and tenant isolation; enforce central quotas; document retention/deletion; test backup and recovery; test malicious uploads and access paths; calibrate any model-based judge; define operating support and incident response. Obtain a suitable independent review before making security or compliance assurances.

## Known evaluation limitations

Phrase matching can reject a correct paraphrase or accept an incorrect sentence that contains the required words. Marker checking cannot prove grounding. The JSON check does not enforce a field schema. Small suites are easy to overfit. One run does not measure variability. User-supplied responses can have unverified provenance. No train/test separation or statistical significance is claimed for the demo.
