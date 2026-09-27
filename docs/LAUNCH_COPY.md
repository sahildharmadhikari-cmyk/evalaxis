# Launch and profile copy

Use only after deploying and personally testing the public beta. Replace every placeholder. Do not describe live generation as verified until the private smoke test succeeds.

## LinkedIn experience

**Title:** Founder & Product Builder — Independent Project

**Organisation/project:** EvalAxis

**Dates:** Use the actual month and year you start this work. Do not backdate.

I am building EvalAxis, an independent beta that helps small teams compare AI assistant responses, investigate regressions and document human release reviews.

- Defined the initial product problem, target users, MVP scope, user stories and staged roadmap.
- Developed an AI-assisted prototype with test-case imports, explainable response checks, A/B comparison and human review.
- Designed structured evaluation records and downloadable evidence reports to make release decisions easier to inspect.
- Added automated tests for evaluation logic, application workflows and a mocked live-model integration.
- Am seeking pilot feedback to validate the problem and prioritise the next iteration.

If you have not personally reviewed/owned the requirements and tested the app, complete those steps before using this wording. Add completed discovery, users or measured results only when you have evidence.

## CV project entry

**EvalAxis — AI Evaluation & Release Review | Independent Project**

Built an AI-assisted Python/Streamlit prototype to compare assistant responses using versioned test cases, explainable checks and human assessment. Implemented regression reporting, structured evidence exports and an optional server-side model API adapter; documented the MVP, governance limits and product roadmap.

## LinkedIn launch post

A better average result can hide a worse individual answer.

That is the problem I wanted to explore with EvalAxis, an independent AI evaluation beta I am building.

It lets you compare two sets of assistant responses, inspect checks such as output formatting and required content, record a human assessment and download the evidence behind a release review.

The example includes a deliberate regression: the candidate improves several responses but breaks a JSON requirement. The app keeps that failure visible instead of treating a higher pass count as a reason to release.

This is an early product, developed with AI assistance. The sample responses are hand-written, and automated checks do not prove an answer is correct or safe. I am using the beta to learn what teams actually need before expanding it.

For me, it brings together data quality, AI evaluation and product delivery—and gives me a chance to take responsibility for the full journey from problem definition to feedback.

Try the beta: [LIVE_APP_URL]
Product page: [GAMMA_URL]
Code: [GITHUB_URL]

If you build or review AI knowledge assistants, how do you decide whether a prompt change is ready to release? I would welcome feedback and a few pilot conversations.

#AIEvaluation #GenerativeAI #ProductDevelopment #DataQuality #BuildInPublic

## A short pilot invitation

Hi [Name], I am building an early evaluation tool for teams changing AI assistant prompts. It compares responses, highlights configured-check regressions and exports a human review report. Would you be open to trying a synthetic example and telling me whether the workflow would help with a real release decision? It takes about 10 minutes, and I am looking for candid feedback rather than a testimonial. [LIVE_APP_URL]

## Sixty-second demo script

1. “This is a prepared example, not a real model benchmark.”
2. Show baseline 2/6, candidate 5/6 and one regression.
3. Filter to regressions. Open C05 and explain the JSON requirement.
4. Show the supplied context and human reference on C01.
5. Record a reasoned human verdict.
6. Show that the release gate remains Hold for changes.
7. Download/open the readable report.
8. “Next I am validating whether small teams need this workflow before adding durable private workspaces.”
