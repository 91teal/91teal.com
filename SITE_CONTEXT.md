# 91teal.com Site Context

This is the durable memory for work on the 91 Teal website. Read it with `README.md` and `AGENTS.md` before making changes. Update it whenever new site knowledge, decisions, open questions, verification results, or publishing state are learned.

Last updated: 2026-08-11

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
| `scripts/preview_server.py` | No-cache local preview server. Use it instead of plain `python -m http.server` so edits are never masked by browser caching. |
| `.github/workflows/check-site.yml` | Runs the static-site checker on pull requests and selected pushes after it is published to GitHub. |
| `design/availability-section-options.md` | Saved assessment, CSV data contract, and three replacement concepts for the availability section. |
| `design/week-interest-form-spec.md` | Build spec for the new week-interest Google Form, and the two values needed to switch prefill on. |
| `docs/when-a-week-sells.md` | Runbook for keeping the availability sheet and the form's week checkboxes aligned by hand. Written to be executed by the separate lease-signing workflow. |
| `.claude/launch.json` | Preview-server definition used by the Claude Code browser preview. Local tooling only; not served content. |

## Current page structure

`index.html` is a one-page site with these major sections and navigation targets:

1. Hero
2. About (`#about`)
3. Location/map (`#map`)
4. Amenities (`#amenities`)
5. Gallery (`#gallery`)
6. Tour (`#tour`)
7. Availability (`#availability`) — also the inquiry section since 2026-08-14
8. Footer

The separate booking section (`#book`) was removed on 2026-08-14 and merged into Availability. Its nav link went with it. `section[id]` carries a `scroll-margin-top` in `styles.css` so anchored sections stop clear of the fixed header; without it every nav target lands with its heading hidden.

The page also includes a fixed header, share button, back-to-top button, expandable 22-photo gallery, and keyboard-navigable lightbox.

## Existing external integrations

The exact identifiers and URLs live in `index.html`; consult the file before changing them.

| Integration | Current purpose |
|---|---|
| Google Tag Manager | Page and custom interaction analytics |
| Meta Pixel | Page-view and lead/contact tracking |
| Google Maps embed | Property-location map |
| Published Google Sheet | Public CSV source for the custom availability ribbon on the local implementation branch; the exact URL lives in `index.html` |
| Google Form | Single inquiry destination for all three CTAs. See "Week-interest form" below |
| Instagram `@91teal` | External photo/social destination |
| YouTube | Embedded house walkthrough |
| Schema.org JSON-LD | `VacationRental` structured data |
| Open Graph and X/Twitter metadata | Link-preview content |

Do not change these integrations or their public client-side identifiers without a request that specifically affects them. Never copy private credentials from the parent lease workspace into this repository.

## Week-interest form

Created 2026-08-10 in Adam's **adam.m.tho@gmail.com** account, replacing `91 Teal 2026 Rental Interest`. Title is deliberately season-neutral so it does not need renaming each year.

| Item | Value |
|---|---|
| Title | `91 Teal Rental Interest` |
| Public URL | `https://docs.google.com/forms/d/e/1FAIpQLSeyb3Sc93TWQ4cn5lgYTIGilZPN7VEvyOfsfQrzq6cTDguQiA/viewform` |
| Edit URL | `https://docs.google.com/forms/d/1c0wL9FLM1mT4q30IENd5dg-a3CvmLz1Xdxjd-W-D8EM/edit` |
| Weeks question entry id | `entry.1418677425` (checkboxes, since 2026-08-14) |
| Questions | Name, email, phone (short answer); Weeks you selected (**checkboxes**, one option per bookable week); How firm is your interest? (multiple choice); free-text notes (paragraph). All required |

The weeks question was a paragraph until 2026-08-14, on `entry.586370353`. That field is deleted; the id is dead and must not be reused.
| Interest options | `Ready to book now`, `Strong interest`, `Just exploring` |

Rules that must survive future edits:

- Use the long `docs.google.com/forms/d/e/.../viewform` URL. A `forms.gle` short link can drop prefill parameters on redirect.
- **Never hand-write or guess the entry id.** It must come from a real prefilled URL (form editor **⋮ → Get pre-filled link**, or `toPrefilledUrl()` in Apps Script).
- Checkbox prefill repeats the same parameter once per week: `entry.1418677425=<week>&entry.1418677425=<week>`.
- **The site sends the date range only, never the holiday label.** Option text must match exactly, and holiday text comes from the feed's editable `event` column, so including it would break the match whenever that column is edited. `buildInquiryUrl()` in `index.html` enforces this.
- The option labels use an **en dash** (U+2013), spaced when the week crosses a month (`Jul 28 – Aug 4, 2027`) and unspaced when it does not (`Jul 14–21, 2027`). Never hand-type one; see `docs/when-a-week-sells.md`.
- Deleting and recreating the form changes both the URL and the entry id, so `index.html` must be updated in the same change.
- Keep the form's responses away from the published availability sheet. The availability CSV is public; responses contain names, emails, and phone numbers. As of 2026-08-11 the form has no linked response spreadsheet — responses live in the form itself, which satisfies this.

Adam's direction on 2026-08-11 was that all three inquiry CTAs point at this one form. **Superseded on 2026-08-14:** the form is now reachable *only* from the availability section's "Request these weeks" button. The hero button scrolls to the week picker instead, and the bottom CTA was removed with the booking section. Every inquiry therefore arrives with weeks already ticked, which is what closed the "someone off the internet types anything" problem rather than merely mitigating it.

### Verified behaviour of Google Forms prefill (tested 2026-08-13 on a throwaway form)

- **Checkbox questions can be prefilled**, including several boxes at once: repeat the same `entry.<id>=<option text>` parameter once per box.
- **The match must be exact, character for character.** A value matching no option is **silently discarded** — no error shown, nothing recorded. This is the dominant risk in any checkbox design.
- An `Other` box can be prefilled with arbitrary text via `entry.<id>=__other_option__` plus `entry.<id>.other_option_response=<text>`.
- Google strips `usp=pp_url` from the URL on load. Prefill still works without it.
- **Do not trust `aria-checked` when inspecting a rendered Google Form** — it reads `false` even for a box that was just clicked. The reliable state is the hidden `input[name="entry.<id>"]` elements, one per selected value.

Adam's decision on 2026-08-13: keep sheet-to-form alignment **manual**, with no sync script. Most visitors arrive through the website, which reads the CSV live and is always accurate, and a request for an already-sold week is still a lead worth having. The procedure is `docs/when-a-week-sells.md`; the ordering rule in it (sheet before form) is what keeps the manual approach safe.

The form was built by a throwaway Apps Script project (`Untitled project`, owned by `adam.m.tho@gmail.com`, script id `1l0BcLUEUVM1l16H-P89amI8BGkYE9BZWL8xFGXmTBh3_1uuMuRpuzObZ`) that calls `FormApp.create`. It has served its purpose; deleting it does not affect the form. Do not re-run `create91TealForm` — each run creates another duplicate form.

## Existing public content facts

These facts are observations from the current public source in `index.html`, not independent verification. Adam’s later instruction or approved source controls if anything changes.

- Property: 91 Teal Walk, Fire Island Pines, New York 11782.
- Public contact: `hello@91teal.com`.
- The current site describes a 2023 renovation by BoND.
- The current site describes four bedrooms sleeping eight guests, with three king beds and one queen bed.
- The current site describes a heated saltwater pool, hot tub, outdoor shower, climate control, high-speed Wi-Fi, a new kitchen with two dishwashers, and pet-friendly stays.
- Rentals run Wednesday to Wednesday. **The 4:00 p.m. check-in and 10:00 a.m. check-out times are no longer stated anywhere on the site** — they lived only in the removed booking section, and Adam's replacement copy on 2026-08-14 dropped them. He was told; re-adding is a one-line change if he wants them back.
- The availability section invites requests for `On Hold` weeks, explicitly not guaranteed. The renderer supports this (`status === 'available' || status === 'held'` is selectable), but a held week is only selectable when its sheet row also has `requestable` set to TRUE. The feed contained no held rows as of 2026-08-14, so this path is unexercised in production.
- The current gallery contains 22 ordered photos. The first six render as the featured gallery; the remaining sixteen appear after expansion.

Do not infer new rates, availability, policies, amenities, legal terms, or renovation claims from these observations.

## Workflow decisions

- **Current workflow (Adam's decision, 2026-08-10, supersedes everything below it):** work directly on `main`, show him the result, publish on his OK. **No branches and no pull requests by default** — he owns this site alone and explicitly rejected that ceremony as friction he never asked for. Do not reintroduce it. `AGENTS.md` is the authority.
- Publishing **is** pushing to `main`. GitHub Pages redeploys in about a minute. There is no staging environment.
- Superseded on 2026-08-10 (kept for history, do not act on): an earlier direction to work in `codex/<slug>` branches, push them, and review as pull requests before merging.
- GitHub Pages has no per-branch preview URLs, so a local preview is the only way to see a change before it is public.
- Preview through `python scripts/preview_server.py 8000`; run `python scripts/check_site.py` after material edits.
- Review changes before publishing. Editing or previewing does not authorize pushing or deploying.
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
- ~~The live `main` page still embeds an older published sheet whose `gid=0` CSV returned `#REF!`.~~ Resolved 2026-08-10: the iframe is gone from the live page, replaced by the CSV-driven season ribbon.
- No local git identity is configured, and there is no global one either. Commits made from this Windows workspace use the repository-local `user.name`/`user.email` set on 2026-08-10 to match existing history; Adam has not yet confirmed the identity he wants on public commits.
- `gh` is not installed on this Windows machine. This does **not** block pushing: `git push` authenticates through the `manager` credential helper and works. `gh` is only needed for creating pull requests, merging, and querying Pages state. Actions results can be read unauthenticated from `api.github.com` because the repository is public.
- The clone lives inside OneDrive, which is actively harmful to a git repository. On 2026-08-10 a second machine saw `.git` with every top-level file (`HEAD`, `config`, `index`, `packed-refs`) missing while subdirectories survived. The original clone was verified uncorrupted at the same moment, so this was an incomplete OneDrive sync, not repository damage. The working clone should be moved out of OneDrive.
- ~~The published availability CSV contains only 2027 weeks while the Google Form is titled `91 Teal 2026 Rental Interest`, so form and feed disagree about the season.~~ Resolved 2026-08-11 by Adam: **2027 is the season being sold, and the CSV feed is the source of truth.** Everything in the old 2026 form was only ever an example. The new season-neutral form carries no year at all, so this cannot recur.
- The old form `91 Teal 2026 Rental Interest` (`https://forms.gle/ENvfe7acgyBqA6zC8`) is no longer linked from the site but is still live and still accepting responses anywhere that short link was shared. Adam was advised on 2026-08-11 to close it to responses; not confirmed done.
- Adam's Chrome has two Google accounts signed in. Apps Script and Drive URLs need an explicit account index: **`/u/1/` is `adam.m.tho@gmail.com`** (which owns the form) and `/u/0/` is his work account `a.thompson@cadogantate.com`. A bare `script.google.com/home/projects/<id>/edit` can redirect to the wrong account and show "Page Not Found".
- The embedded fallback CSV in `index.html` is drifting from the live feed. As of 2026-08-11 the live feed labels Jul 14–21, 2027 as `Dance Festival (TBC)`, which the snapshot does not contain. The 45-day freshness gate still accepts the snapshot (`Aug 6, 2026`), so this is cosmetic, but the snapshot expires around 2026-09-20 and will then stop rendering.
- Chrome heuristically cached `styles.css` when the preview was served by `python -m http.server`, which sends `Last-Modified` but no `Cache-Control`, so CSS edits could appear not to apply. Resolved on 2026-08-10 by `scripts/preview_server.py`, which strips the validators and sends `no-store`. If a preview ever looks stale again, confirm the preview is running that script and not plain `http.server`.

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

### 2026-08-09 — Availability preview fallback

- Adam reported that the new availability section showed only its contact fallback instead of the season ribbon in the preview he was viewing.
- Confirmed the module markup was present but that preview could not reach Google’s CSV. Also confirmed the public `www.91teal.com` page still served the older iframe version because the local branch had not been published.
- Added an embedded last-known-good copy of the same reviewed public CSV to `index.html`. The module now prefers the live Google feed and automatically renders the embedded copy only when the network request fails.
- The embedded copy retains the public feed’s `last_updated` value so visitors can see its freshness. It contains no tenant, contact, payment, or private lease data.
- Forced the Google request to fail during local testing and verified the ribbon still rendered 25 weeks, hid the error message, and showed `Updated Aug 6, 2026`. Restored the real Google URL and reverified the same result.
- This resiliency change remains local and unpublished.

### 2026-08-10 — Session moved to Claude Code; multi-week selection built

- Adam moved website work from the previous agent to Claude Code and asked that GitHub, not the local clone, be the place the site is managed. He also directed that work stay inside `Leases/Website` and not touch the parent lease workspace.
- Reverified the live state: the published CSV returns HTTP 200 with `Access-Control-Allow-Origin: *` and 25 data rows, and `www.91teal.com` still serves the old Google Sheet iframe because the availability branch was never pushed.
- Reviewed the existing Google Form (`91 Teal 2026 Rental Interest`). It collects name, email, phone, a hardcoded per-week High/Medium/Low grid, and a free-text question. The grid cannot accept a dynamic set of weeks, so Adam asked for a new form built from scratch using it as the style reference.
- Fixed three defects in the availability module:
  - Added a season heading (`2027 Season`) because no year appeared anywhere; a visitor in 2026 could read the 2027 weeks as 2026 dates. Two-year feeds render as a range.
  - A blank or unrecognized `status` previously resolved to `available`, so an unfilled sheet row advertised itself as bookable. Unknown statuses now resolve to a disabled `unavailable` state.
  - The embedded fallback is now only rendered when its `last_updated` parses and is within 45 days, so a frozen snapshot cannot silently advertise stale availability.
- Replaced single-week selection with multi-week selection. A persistent summary sits above the ribbon with a live count, removable chips, `Clear selection`, and a disabled-until-valid `Request these weeks` button. Selection order is preserved and weeks are keyed by the feed's `week_id`.
- Wired the selected weeks into a Google Form prefill payload, gated behind `availabilityFormWeeksEntry`. That constant is intentionally empty until Adam supplies the real long form URL and entry id, so the button currently opens the existing form unprefilled rather than sending a broken link.
- Saved `design/week-interest-form-spec.md` with the questions to create and the exact two values to send back.
- Verified in a local browser preview: 25 tiles across six months, 21 selectable, `2027 Season` heading, select/deselect via tile and via chip, clear-all, correct counts, payload `May 26 – Jun 2, 2027 — Memorial Day (Mon May 31); Jul 14–21, 2027`, unconfigured button falling back to the plain form URL, status mapping across twelve inputs including blanks and typos, fallback age accepted at 4 days and rejected at 1 year, plus desktop (1280px) and mobile (375px) layouts with no horizontal overflow.
- `python scripts/check_site.py` and `git diff --check` passed. Nothing was pushed, merged, or published, so 91teal.com remains unchanged.

### 2026-08-10 — PUBLISHED: availability ribbon is live; workflow simplified

- Adam pushed back on the branch-and-pull-request process, asking why the site was not simply being updated as he had asked. That process came from the previous agent's `AGENTS.md` and was not something he requested. He is the sole owner of this site, so a pull request adds no value here.
- Adam's chosen workflow going forward: **work on `main`, show him the result, then publish on his OK.** No branches or pull requests by default. `AGENTS.md` has been rewritten accordingly, including an explicit instruction not to reintroduce them.
- With his approval, fast-forwarded `main` from `316ad8e` to `1443daa` and pushed. **This replaced the live Google Sheets iframe with the season ribbon. 91teal.com is now changed.**
- Verified on the real domain, not just locally: the live page fetches the published CSV successfully from `https://www.91teal.com` (HTTP 200, 25 rows, no fallback and no error state), renders `2027 Season` with 25 tiles and 21 selectable, starts with nothing selected, and multi-select, chips, and clear all work. The old spreadsheet iframe is gone.
- The `Request these weeks` button still opens the existing 2026 form unprefilled, because the new form does not exist yet. This is unchanged from the previous live behavior, so publishing did not regress it.
- Fixed a line-ending trap that blocked the publish: `scripts/check_site.py` and `scripts/serve.sh` were committed with CRLF while `core.autocrlf` is true, so git reported them as permanently modified and refused a branch switch. Added `.gitattributes` and renormalized them. Content is unchanged and `check_site.py` still passes.

### 2026-08-10 — First push to GitHub; OneDrive sync damage on a second machine

- Adam moved to a second machine to get GitHub access. That machine's agent reported `.git` as damaged: every top-level file missing, only subdirectories surviving.
- Verified the original clone was healthy at that moment: `git fsck --full` reported no corruption, all 7 refs present, all 9 commits reachable, `HEAD` at `679a824`. Because the two machines see the same folder, the asymmetry proves an incomplete OneDrive sync rather than repository corruption.
- Created a verified backup at `C:\Users\a.thompson\91teal-git-backup\91teal-all.bundle` (outside OneDrive). `git bundle verify` reports a complete history with all 7 refs.
- Established that `gh` was never required for pushing. `git push --dry-run` succeeded from the original machine, so the credential helper already holds working GitHub credentials. An earlier session note implying push was blocked was wrong.
- With Adam's approval, pushed `codex/availability-section-concepts` to `origin`. Remote SHA `679a824` matches local `HEAD`. `origin/main` remains `316ad8e`, so the live site is unaffected.
- `.github/workflows/check-site.yml` ran for the first time and passed: run `31434420729`, conclusion `success` on `679a824`.
- No pull request has been opened, nothing has been merged, and 91teal.com is unchanged.
- Outstanding: move the working clone out of OneDrive, and decide whether the branch is opened as one pull request or split.

### 2026-08-10 — Selection summary moved to the bottom

- Adam reviewed the preview and asked for the selection summary at the bottom of the section rather than the top. Section order is now season heading, ribbon, legend, selection summary.
- Adam also reported weeks appearing pre-selected on open. Verified in an isolated fresh load that nothing is selected on load: zero pressed tiles, zero chips, `No weeks selected yet`, inquiry disabled, clear hidden. The pre-selected state he saw was leftover from agent test clicks in the shared preview tab, not site behavior. `renderWeeks` resets the selection on every draw.
- Added `scripts/preview_server.py` after browser caching repeatedly masked CSS edits during verification, and pointed `.claude/launch.json` at it. Confirmed responses now carry `Cache-Control: no-store` with no `Last-Modified` or `ETag`.
- Reverified after the move on a plain reload with no cache workaround: correct child order, summary below the ribbon and legend, nothing pre-selected, `2027 Season`, 25 weeks, and a 375-pixel mobile layout with stacked full-width buttons and no horizontal overflow.

### 2026-08-11 — PUBLISHED: week-interest form built and wired into every CTA

- Built the replacement form `91 Teal Rental Interest` in `adam.m.tho@gmail.com` with Apps Script rather than the Forms editor UI, because `toPrefilledUrl()` returns the real entry id directly and removes any temptation to guess it. See "Week-interest form" above for its URLs and entry id.
- Adam clicked the OAuth consent himself; the agent did not. Exactly one `create91TealForm` execution ran (Completed, 6.5 s), so exactly one form exists.
- **Two decisions Adam made:**
  - All three inquiry CTAs point at the new form, not just the availability section. Responses land in one place instead of split across two forms.
  - 2027 is the season being sold and the CSV feed is the source of truth. The old 2026 form was only ever an example.
- Extended the weeks question's help text beyond the spec to cover the direct-arrival path Adam described: "Prefilled from the website — edit if you want to add or remove weeks. If you came here directly, list the weeks you're interested in." The question is required, so visitors arriving from the generic CTAs need to know what to type.
- Verified the prefill genuinely lands in the field, not just that the URL looked right: loading the site-generated URL put `May 26 – Jun 2, 2027 — Memorial Day (Mon May 31); Jul 14–21, 2027 — Dance Festival (TBC)` into the weeks textarea with en/em dashes intact and every other field untouched. The form is publicly reachable with no Google session.
- Confirmed the form's shape from the rendered page: six questions in order, all required, two `<textarea>` elements (weeks and notes) and three text inputs, and the three interest options.
- Also verified: nothing selected on a fresh load, 25 tiles over six months with 21 selectable, chip removal from a three-week selection leaving the correct two in click order, clear-all resetting to the disabled state, and the two generic CTAs opening the form with the weeks field empty. No horizontal overflow at 1280×800 or 375×812, buttons stacked on mobile. `python scripts/check_site.py` and `git diff --check` passed.
- Could not capture screenshots this session — the browser preview pane was hidden, so the page was not compositing frames. Verification was measurement-based via the DOM instead, which covered the same claims.
- **Published on Adam's word: pushed `a9192e9..7b43e87` to `main`.** Confirmed live rather than assumed: `https://www.91teal.com/` serves the new form URL and `entry.586370353`, the only remaining `forms.gle` string is inside a source comment, and a click-through on the real domain produced the correct prefilled URL.
- Deleted the obsolete untracked `HANDOFF.md`. It described a branch-and-pull-request workflow Adam had already rejected and work that was already published, and its own header said it could be deleted.
- Rewrote the stale "Workflow decisions" section above, which still instructed future agents to use `codex/<slug>` branches and pull requests. That contradicted `AGENTS.md` and would have led a fresh session to reintroduce exactly the friction Adam removed.
- Open follow-ups for Adam: close the old 2026 form to responses, and decide whether to trash the throwaway `Untitled project` Apps Script project.

### 2026-08-14 — PUBLISHED: weeks became checkboxes, and the site now funnels every inquiry through the picker

- Adam's concern: a visitor arriving cold at the form could type anything into a free-text weeks box, giving him unusable data. He asked for checkboxes, or two forms, and wanted options.
- **Verified how Google Forms prefill actually behaves** before recommending anything, using a throwaway form rather than his. Findings are recorded under "Week-interest form" above; the decisive one is that an unmatched value is **silently discarded**. Also learned not to trust `aria-checked` when inspecting a rendered form — it reads `false` even for a box just clicked; the hidden `input[name="entry.<id>"]` elements are the real state.
- Adam rejected the sync-script option with sound reasoning: the site reads the CSV live and is always accurate, most visitors come through it, and a request for a sold week is still a lead. Alignment stays manual, procedure in `docs/when-a-week-sells.md`.
- Two design decisions that make the manual approach safe: option labels carry the **date range only** (so the editable `event` column can never break the match), and the runbook's **sheet-before-form ordering** (so every intermediate state fails safe).
- Switched the weeks question from Paragraph to Checkboxes with 21 options, in three stages so the form was valid at every moment: add the checkbox question and soften the old paragraph, then publish the site on the new entry id, then delete the paragraph. The script aborted if any response existed; there were none.
- Verified end to end **on the live domain**, not just locally: clicked weeks on `www.91teal.com`, followed the button, and confirmed exactly the selected boxes were ticked on the real form. Repeated after the paragraph was deleted.
- **Adam then restructured the funnel:** the hero button scrolls to the availability section instead of opening the form, and the booking section was deleted and merged into Availability with new copy he supplied. The form is now reachable only after weeks are chosen.
- Found and fixed a pre-existing defect while adding his deep link: no `scroll-margin-top` existed anywhere, so every nav anchor landed with its section heading behind the fixed header. Sections now stop ~27px clear, with a larger offset below 800px where the header grows.
- `behavior: 'smooth'` could not be verified in a real browser — `localhost` and `docs.google.com` are both blocked for the Chrome extension, and the in-app preview pane has no compositor so smooth scrolling is inert there. A fallback jump was added and *that* path was verified.
- Corrected an apparent typo in Adam's supplied copy, `Oh Hold` to `On Hold`, matching the legend; he was told.
- Published `c85e45f` and `87b0a85`, each confirmed live by fetching the real domain.
