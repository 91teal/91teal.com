# 91teal.com Website Instructions

This repository is the public GitHub Pages site for 91 Teal Walk. These instructions apply to all work inside this `Website` folder and override broader lease-workspace instructions when they conflict.

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

1. Start from an up-to-date `main` and create a descriptive `codex/<slug>` branch before making requested site changes.
2. Keep each branch focused on one user-visible change or one closely related set of changes.
3. Preview with `./scripts/serve.sh` and run `python3 scripts/check_site.py`.
4. For visual changes, verify desktop and narrow/mobile layouts. For interaction changes, test keyboard and touch-relevant behavior.
5. Summarize the visible result and any content assumptions for Adam.
6. Do not push, open a pull request, merge, or otherwise publish unless Adam asks for that action. A request to edit or preview is not publishing approval.

## Quality rules

- Prefer semantic HTML and accessible controls. Every meaningful image needs useful alternative text.
- Keep navigation targets, local files, gallery entries, and captions synchronized.
- Avoid unnecessary dependencies, build tools, or generated assets.
- Preserve responsive behavior and test changes against current Safari/Chrome behavior.
- Run the local checker after every material edit and before any publish handoff.
