# 91teal.com Site Context

This is the durable memory for work on the 91 Teal website. Read it with `README.md` and `AGENTS.md` before making changes. Update it whenever new site knowledge, decisions, open questions, verification results, or publishing state are learned.

Last updated: 2026-08-09

## Identity and repository

| Item | Saved context |
|---|---|
| Public site | `https://www.91teal.com/` |
| GitHub repository | `91teal/91teal.com` |
| Repository visibility | Public |
| Default branch | `main` |
| Hosting | GitHub Pages with the custom domain supplied by `CNAME` |
| Local working copy | `Leases/Website` |
| Architecture | Dependency-free static HTML, CSS, JavaScript, and images; no build step |

The site should remain on GitHub Pages and retain its simple static architecture unless Adam explicitly approves a migration.

## Source map

| Path | Role and source-of-truth notes |
|---|---|
| `index.html` | Canonical public page. Contains page copy, metadata, structured data, integrations, inline JavaScript, gallery order, and gallery captions. |
| `styles.css` | Canonical visual styling and responsive rules. |
| `Images/` | Public production image assets. GitHub Pages paths are case-sensitive. |
| `Images/gallery/` | Larger pool of source gallery photos not currently used by the main gallery. |
| `captions.txt` | Caption reference. It currently duplicates gallery captions embedded in `index.html`; both must stay synchronized. |
| `photo-organizer.html` | Standalone browser tool for arranging gallery photos and captions. Because it is in the repository root, GitHub Pages may serve it publicly. |
| `index.html.old` | Historical page snapshot. It is not the canonical page but may still be directly reachable on GitHub Pages. |
| `CNAME` | Must remain exactly `www.91teal.com` unless the domain is intentionally changed. |
| `scripts/check_site.py` | Local and automated checks for anchors, referenced files, filename case, gallery images, CSS URLs, and `CNAME`. |
| `.github/workflows/check-site.yml` | Runs the static-site checker on pull requests and selected pushes after it is published to GitHub. |
| `design/availability-section-options.md` | Saved assessment, CSV data contract, and three replacement concepts for the availability section. |

## Current page structure

`index.html` is a one-page site with these major sections and navigation targets:

1. Hero
2. About (`#about`)
3. Location/map (`#map`)
4. Amenities (`#amenities`)
5. Gallery (`#gallery`)
6. Tour (`#tour`)
7. Availability (`#availability`)
8. Booking/inquiry (`#book`)
9. Footer

The page also includes a fixed header, share button, back-to-top button, expandable 22-photo gallery, and keyboard-navigable lightbox.

## Existing external integrations

The exact identifiers and URLs live in `index.html`; consult the file before changing them.

| Integration | Current purpose |
|---|---|
| Google Tag Manager | Page and custom interaction analytics |
| Meta Pixel | Page-view and lead/contact tracking |
| Google Maps embed | Property-location map |
| Published Google Sheet | Public CSV source for the custom availability ribbon on the local implementation branch; the exact URL lives in `index.html` |
| Google Form | Booking inquiry destination |
| Instagram `@91teal` | External photo/social destination |
| YouTube | Embedded house walkthrough |
| Schema.org JSON-LD | `VacationRental` structured data |
| Open Graph and X/Twitter metadata | Link-preview content |

Do not change these integrations or their public client-side identifiers without a request that specifically affects them. Never copy private credentials from the parent lease workspace into this repository.

## Existing public content facts

These facts are observations from the current public source in `index.html`, not independent verification. Adam’s later instruction or approved source controls if anything changes.

- Property: 91 Teal Walk, Fire Island Pines, New York 11782.
- Public contact: `hello@91teal.com`.
- The current site describes a 2023 renovation by BoND.
- The current site describes four bedrooms sleeping eight guests, with three king beds and one queen bed.
- The current site describes a heated saltwater pool, hot tub, outdoor shower, climate control, high-speed Wi-Fi, a new kitchen with two dishwashers, and pet-friendly stays.
- The booking section says rentals run Wednesday to Wednesday, with 4:00 p.m. check-in and 10:00 a.m. check-out.
- The current gallery contains 22 ordered photos. The first six render as the featured gallery; the remaining sixteen appear after expansion.

Do not infer new rates, availability, policies, amenities, legal terms, or renovation claims from these observations.

## Workflow decisions

- Work in descriptive `codex/<slug>` branches based on an up-to-date `main`.
- Preview through `./scripts/serve.sh`; run `python3 scripts/check_site.py` after material edits.
- Review changes before publishing. Editing or previewing does not authorize pushing, opening a pull request, merging, or deploying.
- Preserve the dependency-free structure unless a change genuinely requires more machinery and Adam approves it.
- Keep site-specific knowledge in this file rather than only in conversations.

## Known issues and open review items

These were observed from the cloned source and have not been fixed unless a later activity-log entry says otherwise.

- `styles.css` contains `.hero-name is` inside a media query; this appears to be an ineffective selector.
- `styles.css` contains `lightbox-close:hover` without the leading period used by the class selector, so the close-button hover rule may not apply.
- Gallery photo 18 still has the placeholder caption `Photo description needed` in both `index.html` and `captions.txt`.
- `photo-organizer.html` and `index.html.old` are repository-root files and may therefore be publicly accessible even though they are not linked from the main page.
- The map’s browser API key is present in client-side HTML as required by the embed. Its Google Cloud domain/API restrictions have not been verified.
- `trackFormSubmission()` exists in `index.html`, but the inquiry buttons open an external Google Form, so the site itself does not observe a successful form submission.
- The lightbox controls do not currently have explicit accessible labels, and focus management has not been verified.
- Mobile and desktop visual QA of the cloned baseline has not yet been performed in this local workspace.
- The live `main` page still embeds an older published sheet whose `gid=0` CSV returned `#REF!` on 2026-08-09. The local availability branch replaces that iframe with the newer public CSV module; the live issue remains until the website change is published.

## Activity log

### 2026-08-09 — Collaborative editing setup

- Located the public GitHub repository `91teal/91teal.com` through the connected GitHub account.
- Cloned the repository into `Leases/Website`.
- Confirmed the repository is a static GitHub Pages site with `main` as its default branch.
- Added `README.md`, website-specific `AGENTS.md`, `.gitignore`, local preview and site-check scripts, and a GitHub Actions check workflow.
- Created local branch `codex/setup-collaborative-editing` and local commit `0eebaef` (`Set up collaborative website editing`).
- Ran `python3 scripts/check_site.py`; all implemented checks passed.
- Started the local preview server and confirmed `index.html` returned HTTP 200.
- Did not push the branch, open a pull request, merge, or change the live site.

### 2026-08-09 — Persistent context rule

- Adam directed that everything learned for future use about the website be saved inside `Leases/Website`.
- Added this file and made updating it a required step in `AGENTS.md`.

### 2026-08-09 — Availability section concepts

- Reviewed the live site and current embedded Google Sheet availability section.
- Confirmed the design language is warm off-white, white surfaces, terracotta accents, serif headings, thin warm borders, and soft corners.
- Confirmed the published sheet supports a browser-readable CSV endpoint and returns permissive cross-origin headers.
- Found the current `gid=0` CSV has `#REF!` errors and no usable availability rows, so a clean dedicated public feed tab is required before implementation.
- Saved three concepts in `design/availability-section-options.md`: editorial week list, season ribbon, and monthly calendar.
- Recommended the editorial week list as the best fit for the current site and the most robust mobile option.
- Created local branch `codex/availability-section-concepts`; no production page files were changed and nothing was published.

### 2026-08-09 — Season ribbon selected for refinement

- Adam selected Option 2, the season ribbon, for further development.
- Each week tile must include a separate holiday/event line when relevant, between the date range and availability status.
- Holiday/event text must be supplied explicitly by the public feed’s `label` field and must not be inferred by the website.
- Updated the saved design specification; the live site remains unchanged.

### 2026-08-09 — Season ribbon status palette

- Adam rejected red as the available color.
- The selected mapping is gold for `available`, red for `held`/on hold, and neutral gray for `booked`.
- Status text remains required in every tile and in the legend so meaning does not rely on color alone.
- Updated the refined mockup and saved design specification; the live site remains unchanged.

### 2026-08-09 — Existing CSV feed wired into the website

- Adam required using the existing Google Sheet and explicitly prohibited creating another spreadsheet.
- Adam supplied an already-published CSV from the existing availability sheet. The public endpoint is stored in `index.html`; no new spreadsheet or tab was created, and no existing sheet cells or permissions were changed.
- Verified the feed returns `Access-Control-Allow-Origin: *` and the columns `week_id`, `start_date`, `end_date`, `dates`, `event`, `status`, `requestable`, and `last_updated`.
- Replaced the availability iframe locally with the selected dependency-free season ribbon driven by that CSV.
- The renderer groups weeks by start month, preserves the feed’s `event` text as the holiday/event line, filters expired periods by `end_date`, and shows a calm contact fallback if the feed cannot be loaded or validated.
- Status mapping is `AVAILABLE` to gold, `HELD`/`ON HOLD`/`HOLD` to red, and `BOOKED` or any other non-available status to neutral gray. Booked weeks and rows with `requestable=FALSE` are disabled; requestable available or held weeks expose an inquiry detail.
- The supplied 2027 feed rendered all 25 rows from May through October during verification. It currently contains available and booked rows but no held row; held rendering is implemented from the status value and palette.
- Verified the real CSV transformation, holiday labels, disabled booked controls, selected-week detail, desktop layout, and a 390-pixel mobile layout in a local browser preview.
- `python3 scripts/check_site.py`, `git diff --check`, and inline JavaScript syntax validation passed. Nothing was pushed, merged, or published, so 91teal.com remains unchanged.
