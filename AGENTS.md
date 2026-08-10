# 91teal.com Website Instructions

This repository is the public GitHub Pages site for 91 Teal Walk. These instructions apply to all work inside this `Website` folder and override broader lease-workspace instructions when they conflict.

## Persistent site memory

- Read `README.md`, this file, and `SITE_CONTEXT.md` before doing site work.
- Do not rely on chat history as the only source of site knowledge.
- Save every durable fact learned about the site, its integrations, its content, its workflow, and its known issues in `SITE_CONTEXT.md` before finishing the task.
- Update the dated activity log in `SITE_CONTEXT.md` when a decision is made, a verification is completed, or repository/deployment state changes.
- Keep credentials, private tenant information, and secrets out of site memory. When a value is already present in public client-side code, point to its source file instead of needlessly duplicating sensitive-looking values.
- If a newly learned fact conflicts with the saved context, record the conflict and its evidence; do not silently choose one.

## Architecture

- Preserve the dependency-free static site unless Adam explicitly approves a framework or hosting change.
- `index.html` is the canonical public page. `styles.css` contains its presentation. JavaScript currently lives inline in `index.html`.
- `Images/` paths are case-sensitive on GitHub Pages. Preserve the exact filename and extension case.
- `CNAME` must contain exactly `www.91teal.com` unless Adam explicitly requests a domain change.
- Do not add `.openai/hosting.json` or migrate the site away from GitHub Pages without explicit approval.

## Content and privacy

- Adam’s direct instructions control public copy and facts.
- Do not infer or invent rates, availability, booking policies, amenities, legal terms, renovation details, contact information, or analytics configuration.
- Never copy leases, tenant data, credentials, access tokens, or other private files from the parent workspace into this public repository.
- Preserve the existing Google Tag Manager, Meta Pixel, map, form, calendar, Instagram, and YouTube integrations unless a requested change affects them.
- Treat `index.html.old` as historical reference only; do not publish it as the primary page.

## Editing workflow

Adam chose this workflow on 2026-08-10, replacing an earlier branch-and-pull-request process that added friction he never asked for. **Do not reintroduce branches or pull requests as a default.** He owns this site alone; a pull request is optional ceremony here.

1. Work directly on `main` for ordinary changes. Branches are for genuinely risky or exploratory work only, and are not required otherwise.
2. Make the change, then run `python scripts/check_site.py`.
3. Preview with `python scripts/preview_server.py` and verify. For visual changes, check desktop and ~375px mobile. For interaction changes, check keyboard and touch behavior. Do not use plain `python -m http.server`; it lets the browser cache stale CSS.
4. **Show Adam the result and wait for his OK before it goes live.** This is the one gate he wants: nothing reaches the public site unseen.
5. On his OK, push to `main`. GitHub Pages publishes automatically in about a minute.
6. Confirm the change is actually live by fetching `https://www.91teal.com/`, not by assuming the push worked.
7. Update `SITE_CONTEXT.md` with durable learnings and the current verification/publishing state.

Pushing to `main` publishes to the public site, so step 4 is not optional. If a change is purely internal — documentation, scripts, tooling that does not alter the rendered page — it may be pushed without a preview gate, but say so plainly when reporting it.

## Quality rules

- Prefer semantic HTML and accessible controls. Every meaningful image needs useful alternative text.
- Keep navigation targets, local files, gallery entries, and captions synchronized.
- Avoid unnecessary dependencies, build tools, or generated assets.
- Preserve responsive behavior and test changes against current Safari/Chrome behavior.
- Run the local checker after every material edit and before any publish handoff.
