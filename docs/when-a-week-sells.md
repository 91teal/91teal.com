# Runbook — when a week sells (or comes back)

Availability lives in **two** places that do not talk to each other:

1. **The availability Google Sheet**, published as CSV. The website reads this on every page load, so the site is always current.
2. **The `91 Teal Rental Interest` form**, which holds a fixed list of week checkboxes. Nothing updates this automatically.

Keeping them aligned is a deliberate manual step. Adam's decision on 2026-08-13: no sync script. Most visitors arrive through the website, which is always accurate, and a request for an already-sold week is still a lead worth having.

This runbook is written to be executed by the separate lease-signing workflow. It is self-contained — it assumes no knowledge of the conversation that produced it.

---

## The one rule that matters: sheet first, form second

**Always update the Google Sheet before touching the form.** The order is not cosmetic. It decides which failure you get.

| Order | What happens in between |
|---|---|
| **Sheet first** ✅ | The week vanishes from the website immediately, so nobody can select it. The form briefly still lists it — harmless. A cold visitor might tick a sold week, and you still get the lead. |
| Form first ❌ | The website still offers the week, but the form no longer recognises it. Google Forms **silently discards** a prefilled value that matches no option — no error to the visitor, nothing in your response. The inquiry arrives with a week missing and neither of you knows. |

Every intermediate state of "sheet first" is safe. "Form first" has a window where you lose data invisibly.

---

## A week sells

### Step 1 — Google Sheet

Find the row by `week_id` and set:

- `status` → `BOOKED`
- `requestable` → `FALSE`
- `last_updated` → today

Any status the site does not explicitly recognise is treated as unavailable, so a typo fails safe (the week disappears rather than being wrongly advertised).

### Step 2 — Confirm the website caught up

Load `https://www.91teal.com/` and check the week now reads **Booked** and cannot be clicked. Google's published CSV can lag a few minutes. **Wait for this to be true before step 3** — that is what makes the ordering work.

### Step 3 — Form

Open the form's edit URL (recorded in `SITE_CONTEXT.md`), find the **Weeks you selected** question, and **delete that week's checkbox option**.

Delete only. Do not retype, reorder, or "tidy" the other options.

---

## The rule that protects prefill: never hand-type an option

The website prefills checkboxes by sending the option text in the URL. The match must be **exact, character for character**. A single wrong character means that week is silently dropped from the inquiry.

The trap is the dash. These labels use an **en dash (–, U+2013)**, not a hyphen, and the spacing differs depending on whether the week crosses a month:

- Within one month → no spaces: `Jul 14–21, 2027`
- Across two months → spaces: `Jul 28 – Aug 4, 2027`

A hyphen typed on a normal keyboard (`-`) will not match and will fail silently.

**Deleting an option cannot break anything.** Adding or editing one can. So the safe shape of this job is: paste the whole season's list once, then only ever delete from it.

### Holiday text is deliberately not in the option labels

The checkbox options carry the date range only. Holiday and event names (`Memorial Day (Mon May 31)`, `Dance Festival (TBC)`) live in the sheet's `event` column and appear on the website ribbon, but **not** in the checkbox text.

This is on purpose. Event labels get edited mid-season — `Dance Festival (TBC)` was added in August 2026 — and if that text were part of the option, editing the sheet would silently break the form match for that week. Keeping options to the date range alone means the `event` column can be edited freely and forever.

---

## A week comes back available

Reverse the order: **form first, then sheet.** Same logic — never let the website offer a week the form does not know.

1. Add the option to the form, pasted from the season list below. Do not type it.
2. Then set the sheet row back to `AVAILABLE` / `TRUE`.

---

## Season list — 2027

Generated from the live site on 2026-08-13, so the characters are guaranteed correct. Google Forms accepts a pasted multi-line list and splits it into one option per line.

```text
May 5–12, 2027
May 19–26, 2027
May 26 – Jun 2, 2027
Jun 2–9, 2027
Jun 9–16, 2027
Jun 23–30, 2027
Jun 30 – Jul 7, 2027
Jul 14–21, 2027
Jul 21–28, 2027
Jul 28 – Aug 4, 2027
Aug 4–11, 2027
Aug 11–18, 2027
Aug 25 – Sep 1, 2027
Sep 1–8, 2027
Sep 8–15, 2027
Sep 15–22, 2027
Sep 22–29, 2027
Sep 29 – Oct 6, 2027
Oct 6–13, 2027
Oct 13–20, 2027
Oct 20–27, 2027
```

This is the 21 bookable weeks as of that date; the four already-booked weeks are excluded.

### Regenerating the list for a new season

Do not retype it. On `https://www.91teal.com/`, select every available week, then read the labels off the selection chips — that is the website's own formatter, so it cannot drift from what the site sends.

---

## How you would notice a mismatch

There is no alert, so check occasionally: if a response's checked weeks look thinner than you would expect from someone who clearly browsed the site, suspect a label mismatch rather than a picky guest. Compare the response against the current option list and the sheet.
