# Availability Section Design Options

Status: concepts only; the live `index.html` availability section has not been changed.

Last reviewed: 2026-08-09

## Existing section and aesthetic

The existing 91 Teal design uses a warm off-white page, white content surfaces, a restrained terracotta accent, Georgia headings, system sans-serif body copy, thin warm-gray borders, and soft 16-pixel corners. The visual character is quiet, residential, and editorial rather than app-like.

The current availability section breaks that visual language because it embeds the complete Google Sheets interface. At the time of review it showed Google’s title bar, grid, sheet tab, horizontal and vertical scrollbars, and `#REF!` errors inside a 480-pixel-tall iframe.

## Public CSV finding

The existing published sheet can already be requested as CSV by replacing the `pubhtml` endpoint with:

```text
https://docs.google.com/spreadsheets/d/e/[PUBLISHED_SHEET_ID]/pub?gid=[TAB_GID]&single=true&output=csv
```

The CSV response returned `Access-Control-Allow-Origin: *`, so browser JavaScript on `www.91teal.com` can fetch it directly without a server or new hosting platform.

The current `gid=0` output is not ready to drive the site. On 2026-08-09 it contained the heading `91 Teal Walk`, the title `2026 Availability`, the columns `Holiday Week`, `Check In Date`, `Cost Before Tax`, `Cost as % "Base"`, and `Sold?`, but the first data row contained `#REF!` and there were no usable availability rows.

## Recommended sheet contract

Create a dedicated public tab named `Website Feed`. It should contain only display-safe fields and no tenant names, contact details, deposits, payment information, notes, or internal formulas.

Recommended columns:

| Column | Format | Purpose |
|---|---|---|
| `start_date` | `YYYY-MM-DD` | Rental check-in date |
| `end_date` | `YYYY-MM-DD` | Rental check-out date |
| `label` | Text | Optional holiday or seasonal label |
| `status` | `available`, `held`, or `booked` | Public availability state |
| `rate` | Number or blank | Optional tax-exclusive rate already approved for public display |
| `note` | Short text or blank | Optional public note such as `Two-week stay preferred` |
| `sort` | Number | Stable chronological ordering |

Publishing should be limited to this tab’s `gid`. The website should fetch it on page load, validate the allowed statuses and ISO dates, sort chronologically, and render only current/future rows. If the fetch or validation fails, it should show a calm fallback with the inquiry button rather than a blank section or raw spreadsheet errors.

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

Adam selected this direction for further development on 2026-08-09 and requested the separate holiday/event line. Holiday/event text must come from the public feed’s `label` field; the website must not infer labels from dates.

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

## Next implementation step

After Adam selects a direction:

1. Repair or create the `Website Feed` sheet tab and publish it as CSV.
2. Confirm the live column names, statuses, sample rows, and whether rates should be public.
3. Replace the iframe in `index.html` with the selected semantic markup.
4. Add a small dependency-free CSV parser/renderer and resilient fallback state.
5. Add responsive styles consistent with `styles.css`.
6. Test real data, empty data, malformed data, mobile layout, keyboard interaction, and fetch failure before publishing.
