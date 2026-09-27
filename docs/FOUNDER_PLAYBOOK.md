# EvalAxis: founder and product playbook

Prepared for Sahil Dharmadhikari · 26 September 2026

## The decision

Build a focused AI evaluation and release-review product for small teams shipping knowledge assistants. The long-term vision is a workspace that connects a proposed AI change to tests, evidence, human assessment and a recorded release decision.

The initial beta is the first slice: compare baseline and candidate responses on a small test suite, explain observable failures and export a review report. It is not the full platform, a certified governance system or a general-purpose autonomous agent.

## Why this fits your profile

Your data science interests support test design, comparison and analysis. Your data quality experience supports clear criteria, missing-data handling and review processes. Your AI/project delivery experience supports scope, stakeholder needs, release gates and prioritisation. Developing this product lets you strengthen API integration, software testing and product discovery without claiming expertise or client outcomes you have not demonstrated.

This is broader than transcription. Initial scenarios cover internal policy assistants, SaaS support, structured AI outputs, ambiguity and instruction handling. Later versions can extend to retrieval pipelines and agent actions after those workflows are defined and tested.

## Target customer and problem hypothesis

Primary early user: a product lead, AI implementation consultant or engineer in a small team developing a knowledge assistant. Buying authority and willingness to pay are unknown.

Hypothesis: some teams can demonstrate a chatbot but struggle to show a reviewer what changed after a prompt edit, where quality regressed and why they approved the change. Today they may compare answers manually or assemble findings across spreadsheets and developer tools. Validate this in interviews; do not present it as established market research.

Job to be done: “Before we release a changed assistant, help me compare it against our current version, understand the failures and present evidence for a human decision.”

## Positioning and competition

Proposed positioning: practical release evidence for small teams that need developers and nontechnical reviewers to understand the same evaluation.

LangSmith already provides evaluation, datasets, human review and comparison capabilities. Promptfoo already supports prompt/provider/test-case evaluations. Do not claim the underlying idea is unique. The product hypothesis is that a focused, approachable release-review workflow and well-designed scenario packs can be valuable for a narrower audience. Validate that hypothesis before expanding the platform.

Primary references checked 26 September 2026:
- https://www.langchain.com/langsmith/evaluation
- https://www.promptfoo.dev/docs/getting-started/

## Product vision, MVP and success

Vision: make AI changes reviewable before they reach users.

MVP promise: “Compare two sets of assistant responses, see which configured checks changed, add your judgement and download the evidence.”

V0.1 scope: public prepared example; user CSV import; deterministic checks; two-variant comparison; manual assessment; rule-based release gate; downloadable reports; optional private live model adapter.

Deliberate exclusions: general chatbot, document retrieval, agent tool execution, autonomous deployments, enterprise certification, accounts, billing, durable run storage and automatic semantic scoring.

Initial validation targets, not achieved results:
1. Five relevant discovery conversations within seven days.
2. Three people complete a sample review without live coaching.
3. Two bring a genuine, non-sensitive test scenario rather than only commenting on the design.
4. At least one asks to use it again on a new assistant change.

Record task completion, confusing steps, report usefulness and requests to return. Do not equate views or likes with adoption.

## User stories and acceptance criteria

| Priority | User story | Acceptance evidence |
|---|---|---|
| P0 | As a new visitor, I want an example I can explore immediately. | Example opens without an API key, clearly labelled as hand-written. |
| P0 | As an evaluator, I want to compare my own responses. | Valid CSV imports; missing IDs, invalid flags and malformed rows are rejected. |
| P0 | As a reviewer, I want to see why a response failed. | Every failed check has a visible rule and detail. |
| P0 | As a product lead, I want to find regressions. | Baseline pass → candidate fail/error is flagged; missing output remains incomplete. |
| P0 | As a subject expert, I want to record my judgement. | Pass/Fail requires a reason and records a timestamp. |
| P0 | As an owner, I want a portable review record. | HTML, JSON and CSV downloads reflect the active run and human reviews. |
| P0 | As an API owner, I want deliberate use of my key. | Live mode disabled without server configuration; access code and consent checked before calls. |
| P1 | As a returning team, I want to retrieve past runs. | Future: authenticated ownership and durable versioned records; not yet shipped. |
| P1 | As an owner, I want a real spending limit. | Future: server-enforced per-account/global budgets and rate limits; session cap alone is insufficient. |
| P2 | As a team, I want semantic assessment. | Future: judge rubric calibrated against human labels; false positives and uncertainty reported. |

## Workflow and architecture

User imports a suite or selects the example → supplies/imports two sets of responses or privately runs two prompts → deterministic evaluation → inspection of regressions and critical cases → human review → downloadable evidence.

Gamma is the public product story and onboarding page. Streamlit is the working beta. GitHub contains the implementation, tests, versioned examples and documentation. Optional live calls use the OpenAI Responses API. V0.1 has no database and no retrieval service.

Live model inputs contain prompt instructions, the selected question and supplied context. References and evaluation criteria are withheld from generation. The app records the returned model ID, token usage and elapsed request time where provided. It requests `store=false`; provider retention policies still apply.

## Roadmap and backlog

| Stage | Deliverable | Evidence needed before progressing |
|---|---|---|
| Launch day: public beta | Working comparison, human review, report export, Gamma page | Own public deployment passes launch checks; all claims match actual behaviour. |
| Week 1: discovery | Interview notes, three observed usability sessions, revised onboarding | Identify a repeated problem and a defined user segment. |
| Weeks 2–3: private pilot | Authentication, persistent runs, owner permissions, global usage controls | A small group wants repeat use and agrees on data boundaries. |
| Weeks 4–6: deeper AI evaluation | Versioned datasets, schema checks, repeat runs, calibrated judge experiment | Human reference set exists; measure where automated judgements disagree. |
| Later, demand-led | Provider adapters, RAG retrieval metrics, agent tool-call traces, integrations | Specific customer requirements and a viable support/security model. |

Prioritise by user impact, risk reduction and implementation effort. Do not begin with a logo redesign, a long list of models, subscription billing or a multi-agent architecture without a proven need.

## Reference-image coverage

| Reference theme | Your credible equivalent |
|---|---|
| Founder and product lead | Own the problem, product choices, feedback, scope and launch of an independent beta. |
| Vision and roadmap | This playbook, the staged roadmap and success hypotheses. |
| MVP strategy | A small end-to-end evaluation and human-review workflow. |
| Backlog and user stories | Priorities and acceptance criteria above. |
| AI-assisted workflow design | Two-prompt testing, context handling, optional real model requests and explicit human assessment. |
| Iterative web development | Tested implementation, versioned changes and upcoming observed usability tests. |
| Validation and feedback | Interview and pilot plan; no completed customer validation claimed. |
| LLM capabilities | Responses API adapter; later calibrated semantic judging, not claimed as shipped. |
| Structured metadata / terminology | Versioned CSV schema, case taxonomy, criticality, source IDs, run/prompt hashes and metadata. Healthcare-specific SNOMED is not applicable here. |
| Governance and explainability | Per-check reasons, human verdicts, documented limitations, data-flow rules and portable evidence. |
| Auditability | Exportable run evidence in beta; durable, immutable audit history is future work. |
| Scale and deployment | Public demo plus controlled pilot; identity, quotas and persistence before wider live access. |
| End-to-end leadership | Discovery → requirements → implementation → tests → launch → feedback → iteration. |

## Business experiment

Start with a free public demo and a small, personally supported pilot. Offer help defining a test suite and reviewing an assistant change. Ask whether the real value is the software, the scenario design or the review process. Do not publish revenue, customer logos or invented testimonials.

Potential later business models: paid workspace, recurring release-review service or setup/pilot package. No pricing is validated. Before offering a paid production service, define service scope, support expectations, data handling, operating costs and customer agreements with appropriate advice where needed.

## Discovery questions

1. Tell me about the last prompt or model change you released.
2. How did you decide it was better? What evidence did you keep?
3. Who reviewed it and who could block the release?
4. What went wrong or took the most time?
5. Could you show a non-sensitive example of your current evaluation process?
6. Would this report help an actual decision? What is missing?
7. What would need to be true for you to use it on the next release?

Capture exact observations. Do not turn polite enthusiasm into a claim of demand.

## Your learning and ownership

Before using the founder description, personally run the app, explain one false-positive phrase check, inspect the JSON regression, write three new cases, review their candidate responses, and make one documented improvement from user feedback. Keep a learning log and credit AI assistance. Your decisions and understanding are stronger interview evidence than the number of generated files.
