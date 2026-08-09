# Availability Section Design Options

Status: Option 2 selected and implemented locally; the live site has not been published with the change.

Last reviewed: 2026-08-09

## Existing section and aesthetic

The existing 91 Teal design uses a warm off-white page, white content surfaces, a restrained terracotta accent, Georgia headings, system sans-serif body copy, thin warm-gray borders, and soft 16-pixel corners. The visual character is quiet, residential, and editorial rather than app-like.

The current availability section breaks that visual language because it embeds the complete Google Sheets interface. At the time of review it showed Google’s title bar, grid, sheet tab, horizontal and vertical scrollbars, and `#REF!` errors inside a 480-pixel-tall iframe.

## Public CSV implementation

The selected implementation reads Adam’s existing published Google Sheet directly as CSV. The exact public endpoint is stored in `index.html`.

```text
https://docs.google.com/spreadsheets/d/e/[PUBLISHED_SHEET_ID]/pub?output=csv
```

The CSV response returned `Access-Control-Allow-Origin: *`, so browser JavaScript on `www.91teal.com` can fetch it directly without a server or new hosting platform.

The earlier iframe pointed to a different legacy publication whose first data row contained `#REF!`. Adam supplied a clean publication from the existing availability sheet on 2026-08-09, so the implementation does not use or repair that legacy feed.

## Actual sheet contract

No new spreadsheet or tab is required. The supplied public CSV already contains only display-safe availability fields and no tenant names, contact details, deposits, payment information, or internal notes.

Recommended columns:

| Column | Format | Purpose |
|---|---|---|
| `week_id` | Stable text identifier | Identifies a rental week |
| `start_date` | Display date | Rental check-in date |
| `end_date` | Display date | Rental check-out date |
| `dates` | Display text | Sheet-provided compact date range |
| `event` | Text or blank | Holiday or seasonal label shown on its own line |
| `status` | `AVAILABLE`, `HELD`/`ON HOLD`, or `BOOKED` | Public availability state |
| `requestable` | Boolean | Public requestability flag retained in the feed |
| `last_updated` | Display date | Feed freshness value |

The website fetches the CSV on page load, finds columns by header name, validates and parses the dates, sorts chronologically, and renders only periods whose end date has not passed. If the fetch or validation fails, it shows a calm contact fallback rather than a blank section or raw spreadsheet errors.

## Option 1 — Editorial week list

An elegant vertical list of rental weeks. Each row gives the date range the most visual weight, with the seasonal label, status, optional rate, and a compact inquiry action. Booked weeks remain visible but subdued, which helps visitors understand the season without creating visual clutter.

Strengths:

- Best match for the existing editorial, design-led aesthetic.
- Extremely clear on phones and accessible with keyboard/screen readers.
- Handles labels, notes, rates, and Wednesday-to-Wednesday ranges naturally.
- Lowest implementation and maintenance risk.

Tradeoff: it is less calendar-like than a conventional month grid.

Recommendation: preferred direction.

## Option 2 — Season ribbon

A chronological ribbon grouped by month, with one compact block per rental week. Each block has a date line, a dedicated holiday/event line when relevant, and a status line. Weeks without a holiday keep that middle line visually quiet so dates and statuses remain aligned. Available weeks use a soft gold treatment, on-hold weeks use a restrained red treatment, and booked weeks remain neutral. Selecting a week reveals its date range, holiday/event label when present, and inquiry action below the ribbon.

Strengths:

- Makes the full season easy to scan at once.
- Visually distinctive without departing from the site palette.
- Well suited to fixed Wednesday-to-Wednesday inventory.
- Keeps holiday and Pines-event context visible without turning the section into a spreadsheet.

Tradeoffs:

- Requires careful mobile reflow and accessible non-color status labels.
- Notes and rates need a selected-week detail area rather than always being visible.

Adam selected this direction for development on 2026-08-09 and requested the separate holiday/event line. Holiday/event text comes from the public feed’s `event` field; the website does not infer labels from dates.

Status color mapping approved for the concept: gold means `available`, red means `held`/on hold, and neutral gray means `booked`. Every tile and the legend must continue to show the status in text so color is never the only signal.

## Option 3 — Monthly calendar

A familiar seven-column month view with rental periods marked as continuous bands and a month switcher. Selecting an available period opens its details and inquiry action below the calendar.

Strengths:

- Most immediately familiar to visitors.
- Shows how rental weeks relate to holidays and month boundaries.

Tradeoffs:

- Densest option on phones.
- Cross-month Wednesday-to-Wednesday periods are harder to display cleanly.
- More complex to implement and test correctly than the list or ribbon.

## Shared behavior for the final section

- Keep the existing heading style and white rounded section surface.
- Use text plus color for every status; never rely on color alone.
- Preserve the existing `Request dates and rates` Google Form as the action destination.
- Carry the selected week into the inquiry link only if the Google Form supports a reviewed prefilled parameter; otherwise name the week in the button’s analytics event and leave the form unchanged.
- Add loading, empty, stale-data, and fetch-error states.
- Display `Last updated` only if the public feed supplies a reliable update value.
- Do not render malformed rows or expose raw Google/CSV errors.
- Keep rates hidden when the published `rate` field is blank.

## Implementation status

The local branch now replaces the iframe with semantic markup, a small dependency-free CSV parser and renderer, responsive season-ribbon styles, selected-week inquiry detail, and a resilient fallback state. The real public feed, event labels, status controls, desktop layout, and 390-pixel mobile layout have been verified. Publishing remains a separate approval step.
