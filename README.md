# 91teal.com

This repository contains the public website for [91teal.com](https://www.91teal.com/). It is a dependency-free static site hosted by GitHub Pages.

## Edit with Codex

The local working copy lives in the `Website` folder of the 91 Teal lease workspace. Ask Codex for a change in plain language, for example:

- “Update the amenities copy and show me the exact wording before publishing.”
- “Add these photos to the gallery and preview the result.”
- “Make the navigation work better on phones.”
- “Prepare this website change as a draft pull request.”

Codex should make changes on a short-lived `codex/<description>` branch, preview them locally, run the site checks, and show you the result. Publishing is a separate step: nothing should be merged into `main` without your explicit approval.

## Preview locally

From this folder, run:

```sh
./scripts/serve.sh
```

Then open [http://localhost:8000](http://localhost:8000). Stop the preview with `Control-C`.

To use another port:

```sh
./scripts/serve.sh 8080
```

## Check before publishing

```sh
python3 scripts/check_site.py
```

The same check runs automatically on GitHub when a branch is pushed or a pull request is opened.

## File map

| Path | Purpose |
|---|---|
| `index.html` | The live one-page website, including content and JavaScript |
| `styles.css` | Layout, colors, typography, and responsive styles |
| `Images/` | Public website photography |
| `captions.txt` | Gallery caption reference |
| `photo-organizer.html` | Standalone gallery-ordering helper |
| `CNAME` | Connects GitHub Pages to `www.91teal.com` |
| `AGENTS.md` | Editing and publishing guardrails for Codex |
| `SITE_CONTEXT.md` | Durable site knowledge, decisions, known issues, and activity log |
| `scripts/serve.sh` | Local preview command |
| `scripts/check_site.py` | Dependency-free site checks |

## Publishing model

GitHub Pages publishes the site from the repository’s configured source. The default branch is `main`, so changes should normally be reviewed in a pull request before they are merged. Keep `CNAME` set to `www.91teal.com`; changing or removing it can disconnect the custom domain.

Do not place lease files, access keys, tenant information, or other private business records in this public repository.
