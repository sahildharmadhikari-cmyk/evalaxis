# Launch EvalAxis

Target public beta: Sunday, 27 September 2026, UK time.

This pack contains a working app and founder materials. It has not been published to your accounts. Public demo/CSV comparison needs no API key. Real model generation is an optional private pilot that requires your own API account and a live smoke test.

## What you are launching

EvalAxis helps teams compare two versions of an AI assistant's responses, see regressions, record a human assessment and export a release report.

- **Gamma:** public product page and explanation.
- **Streamlit:** working evaluation app.
- **GitHub:** source code, test suite and product documentation.

Keep SupportLens unchanged. This is a separate repository and project. The earlier annotation-only idea is not the product in this pack.

## A. Create the repository

1. Download `EvalAxis_Launch_Pack.zip`. Keep the filename exactly as shown; do not extract it yet.
2. Open https://github.com/new while signed in to your own account.
3. Repository name: `evalaxis`.
4. Choose Public. Enable Add a README file. Click Create repository.
5. In the repository, choose Code → Codespaces → Create codespace on main.
6. Use this new Codespace, not the SupportLens workspace.
7. Drag `EvalAxis_Launch_Pack.zip` into the Explorer file list beside README.md.
8. Open Terminal → New Terminal.
9. Run:

```bash
pwd
```

The path should end in `/evalaxis`.

10. Extract the pack directly into that folder:

```bash
python -m zipfile -e EvalAxis_Launch_Pack.zip .
```

11. Confirm the app files:

```bash
ls app.py core.py provider.py requirements.txt
```

All four filenames should appear.

## B. Run and understand your app

12. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

13. Run the tests:

```bash
python -m unittest discover -s tests -v
```

Expect 19 tests and OK. If any test fails, keep the full error output for troubleshooting.

14. Start the app:

```bash
python -m streamlit run app.py
```

15. Click Open in Browser. If needed, open Ports and use the browser icon for port 8501.
16. Confirm the sample shows baseline 2/6, candidate 5/6, one regression, zero critical blockers. These are hand-written example outcomes, not real model results.
17. In Compare responses, filter to Regressions. Inspect C05: the candidate wraps JSON in markdown, breaking the configured format requirement.
18. In Human review, select C01. Compare its candidate against the supplied source. Choose a verdict and explain why. Save the review.
19. Open Release report. Confirm the gate still says Hold for changes because C05 fails.
20. Download the HTML and JSON reports. Open the HTML in a browser and check that your review appears.
21. In your terminal, press Ctrl+C to stop the local preview.

## C. Commit and upload

22. Run each command separately:

```bash
git add app.py core.py provider.py requirements.txt README.md START_HERE.md .gitignore .github .streamlit/config.toml data docs tests
```

```bash
git commit -m "Build EvalAxis AI evaluation beta with AI assistance"
```

```bash
git push origin main
```

If a command fails, stop and copy the whole error. Do not force-push or delete your repository.

23. Open your repository on github.com. Refresh and confirm `app.py` and `requirements.txt` are in the top-level file list. The ZIP should not be committed.

## D. Publish the working beta

24. Open https://share.streamlit.io and sign in with GitHub.
25. Click Create app and choose the option for an existing app.
26. Set these fields:

| Field | Value |
|---|---|
| Repository | Your actual GitHub account / evalaxis |
| Branch | main |
| Main file path | app.py |
| App URL | Choose an available name, e.g. evalaxis-sahil |
| Advanced settings: Python | 3.12 |
| Secrets | Leave empty for the public demo |

27. Click Deploy and wait for the app to open.
28. Copy the real `.streamlit.app` URL. Open it in an incognito window. Confirm no sign-in is required and repeat steps 16–20.
29. Check Your CSV using the sample file. Confirm it loads and says user-supplied responses. Do not upload private employer or customer content.
30. Add the live URL to your GitHub repository's About → Website field.

Deployment reference: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy

## E. Build your Gamma product page

31. Open https://gamma.app. Choose Sites → Create new Site.
32. Open `docs/GAMMA_PROMPT.txt` from this pack.
33. Paste it into Gamma and generate the page.
34. Check every claim. The page must say beta and must distinguish public comparison from optional private live generation.
35. Replace every placeholder before publishing:

| Placeholder | Use |
|---|---|
| LIVE_APP_URL | Your verified Streamlit URL |
| GITHUB_URL | Your actual evalaxis repository URL |
| LINKEDIN_URL | Your personal LinkedIn profile URL |

36. Make Try the beta open LIVE_APP_URL. Make View source open GITHUB_URL. Make Contact the builder open LINKEDIN_URL.
37. Remove any invented customers, testimonials, security badges, performance numbers, pricing or unavailable sign-up forms.
38. Preview on desktop and mobile. Click every button.
39. Publish to an available free `.gamma.site` address. Test it in an incognito window.

Gamma reference: https://help.gamma.app/en/articles/8429268-how-do-i-create-publish-a-site-in-gamma

## F. Optional: enable a private live model pilot

The public comparison app is useful without this step. Do not present prepared examples as live AI runs.

1. Use a separate private deployment or a local instance for live testing. Confirm that its audience is restricted before adding credentials. An access code alone is not production authentication.
2. In your API account, choose a text model available to your project and record its exact model ID. Review current pricing and account usage controls.
3. Create a project-scoped API key. Do not paste the key into ChatGPT, Gamma, GitHub or the source code.
4. In the private Streamlit app's Secrets settings, enter:

```toml
OPENAI_API_KEY = "your-private-key"
OPENAI_MODEL = "exact-model-id-available-to-your-account"
RUN_ACCESS_CODE = "a-long-unique-random-access-code"
```

For local use, put the same settings in `.streamlit/secrets.toml`, which is ignored by Git.

5. Reload the app. Open Run prompts and select just one case first.
6. Enter your access code and confirm the data/usage checkbox. Run the A/B comparison.
7. Check both outputs, the returned model ID, usage and request times. Download the evidence JSON.
8. If a request fails, the app stops the batch and shows missing/error states. Check the account, model ID and billing; do not describe this integration as verified until one real request succeeds.
9. Keep the pilot small. The session allowance is not a global cost cap; do not rely on it for an unrestricted public endpoint.

No live API calls were made while preparing this pack. Mocked provider tests passed, but real account/model compatibility remains to be verified.

## G. Your launch checklist

- [ ] Public app opens without login and displays the synthetic-example label.
- [ ] CSV import works with the provided sample.
- [ ] C05 is visible as a regression.
- [ ] A human review is saved and included in a downloaded report.
- [ ] A failed case keeps the release gate on Hold for changes.
- [ ] Gamma buttons open the actual app, code and profile.
- [ ] There are no placeholder URLs or invented business claims.
- [ ] Public deployment contains no API secrets or paid live access.
- [ ] You have written three original test cases and can explain their checks.
- [ ] One other person has tried the main workflow.
- [ ] Your launch wording matches what is actually deployed.

Suggested launch order for 27 September: deploy and inspect the beta, build Gamma, ask one tester to complete a review, then fix observed problems before sharing. Target deployment: 12 noon, London time.

## H. Add it to your professional profile

Use `docs/LAUNCH_COPY.md` after completing the checks. Put the working app first in LinkedIn Featured, with the Gamma product page or GitHub repository beside it. Use the actual launch date. If you choose a founder title, qualify it as an independent project/beta and describe what you personally own.

Continue with `docs/FOUNDER_PLAYBOOK.md`. The next milestone is evidence of a useful problem, not adding features for the sake of appearing advanced.
