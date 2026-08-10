# Week Interest Form — build spec

Status: awaiting form creation. The website is already wired and will prefill as soon as the two values in "What to send back" are filled in.

Last reviewed: 2026-08-10

## Why a new form

The existing form (`91 Teal 2026 Rental Interest`) asks for weeks as a **multiple-choice grid** with one row per week (`MDW May 20, 2026`, `May 27, 2026`, …) and High/Medium/Low columns. That shape cannot work with the new availability ribbon:

- The rows are hardcoded 2026 dates and must be hand-edited every season, which reintroduces the duplicate source of truth the CSV feed was meant to remove.
- A grid needs one `entry.<id>` per row, so the website cannot pass an arbitrary set of selected weeks into it.
- The site now sends weeks read from the published CSV, so the form must accept whatever the feed contains.

The replacement moves week selection **out of the form** (the ribbon already does it) and keeps the form for identity, intent, and notes.

## Questions to create, in order

Keep the existing intro copy and the about-the-house blurb from the current form — only the questions change.

| # | Question | Type | Required | Notes |
|---|---|---|---|---|
| 1 | What is your name? | Short answer | Yes | Unchanged |
| 2 | What is your email? | Short answer | Yes | Unchanged. Offers are shared to this address |
| 3 | What is your phone #? | Short answer | Yes | Unchanged |
| 4 | Weeks you selected | **Paragraph** | Yes | **The website prefills this.** Must be Paragraph, not Short answer — several weeks will not fit on one line |
| 5 | How firm is your interest? | Multiple choice | Yes | Options: `Ready to book now`, `Strong interest`, `Just exploring`. Replaces the per-week High/Medium/Low grid |
| 6 | Anything else I should know (or, feel free to explain what exactly it is you're looking for)? | Paragraph | Yes | Unchanged |

Question 4 is the only one the site writes to. Leave its help text as something like "Prefilled from the website — edit if you want to add or remove weeks." Visitors can still correct it by hand, and anyone reaching the form directly can type into it.

### What the site sends into question 4

Selected weeks joined with `; `, in the order they were clicked, each as `<date range>, <year>` plus the feed's event label when present:

```text
May 26 – Jun 2, 2027 — Memorial Day (Mon May 31); Jun 30 – Jul 7, 2027 — July 4th (Sun Jul 4); Jul 14–21, 2027
```

## What to send back

Two values, both from the form itself — do not hand-write either one:

1. **The long form URL.** Open the form, click **Send**, choose the link tab, and untick "Shorten URL". It looks like `https://docs.google.com/forms/d/e/<LONG_ID>/viewform`. A `forms.gle` short link is not reliable here because prefill parameters can be dropped on redirect.
2. **The `entry` id for question 4.** In the form editor: **⋮ → Get pre-filled link**, type `PLACEHOLDER` into the Weeks field only, click **Get link**, then copy it. The result contains `entry.1234567890=PLACEHOLDER`; the `entry.1234567890` part is what is needed.

Paste both to Claude and they go into `index.html`:

```js
var availabilityFormUrl = "https://docs.google.com/forms/d/e/<LONG_ID>/viewform";
var availabilityFormWeeksEntry = "entry.<id from the pre-filled link>";
```

Until then `availabilityFormWeeksEntry` stays empty and the button opens the current form with nothing prefilled, so the section is never broken while the form is being built.

## Response handling

Responses land in the form's own sheet. Keep that sheet separate from the published availability sheet — the availability CSV is public, and inquiry responses contain names, emails, and phone numbers that must never be published.
