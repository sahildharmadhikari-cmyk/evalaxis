# Test suite format

One row represents one independent, single-turn test case. This release evaluates supplied context; it does not retrieve documents or test multi-step agent trajectories.

| Column | Meaning |
|---|---|
| case_id | Unique non-empty ID, up to 80 characters |
| category | Your test category, up to 100 characters |
| critical | true or false; whether failure should be highlighted as critical |
| question | The input sent to the assistant |
| context | The reference material supplied to the assistant; may be blank |
| reference | Guidance for a human reviewer; never sent to the model |
| required_terms | Every listed phrase must appear; separate phrases with `|` |
| forbidden_terms | Every listed phrase must be absent; separate with `|` |
| max_words | Integer from 1 to 2000; words counted by whitespace |
| require_json | true requires a parsable JSON object with no markdown fences |
| source_ids | Allowed citation IDs such as S1 or S2, separated by `|`. If present, at least one marker is required; unknown markers fail. |
| response_a | Baseline response; may be blank |
| response_b | Candidate response; may be blank |

Maximum 50 cases, 2 MB, UTF-8 encoding and 12,000 characters per field. Blank lines are ignored. Duplicate IDs and malformed rows are rejected. Text is trimmed at its edges. Extra columns are ignored.

## Design a useful suite

Use realistic typical questions, incomplete information, ambiguity, instruction-override attempts, output-format constraints and requests the assistant should decline. Write references independently before running the model. Keep test criteria aligned with the task: a mandatory phrase is a brittle proxy, not an answer-quality metric.

Start with public or synthetic content. Version your suite in GitHub. Do not keep tuning only against a tiny public demo; reserve unseen cases when assessing generalisation. Repeat model runs before interpreting variability as a reliable improvement.

## Export meanings

- HTML: readable findings and run metadata. Open locally in a browser; Print → Save as PDF if needed.
- JSON: full case content, per-check outcomes, run metadata and latest human reviews. This release does not import these reports back into the app.
- CSV: compact result table. It is not the same schema as the input suite; use the original suite when starting another run.

Do not share a report containing information you were not authorised to disclose. Results retain prompts and input content for reviewability; API credentials are never included.
