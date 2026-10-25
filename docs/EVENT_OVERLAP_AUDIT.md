# EVENT OVERLAP AUDIT (GATE 1, 2026-10-17)

## Question
Do the 3,017 event-level WERR rows overlap by country/date, and does each
event's denominator reuse the same actual wind generation?

## Finding — YES, structurally
`scripts/p9_werr.py` assigns each pixel-event the **whole country's**
actual wind generation over its days (`seg[cc_wind_gen]*24` summed over
ev.start:ev.end). Any second event in the same country covering the same
days therefore reuses the same denominator energy — and its own numerator
(dT is identical, since WFI is a region-level field, not pixel-level).

| country | n events | event-days | unique country-days | reused | multiplicity |
|---|---|---|---|---|---|
| AT | 83 | 408 | 100 | 308 | 4.1× |
| BE | 78 | 401 | 100 | 301 | 4.0× |
| CZ | 90 | 490 | 109 | 381 | 4.5× |
| DE | 409 | 2,368 | 240 | 2,128 | **9.9×** |
| DK | 59 | 479 | 134 | 345 | 3.6× |
| ES | 581 | 3,492 | 830 | 6280 | 4.2× |
| FR | 654 | 3,604 | 566 | 3,677 | 6.4× |
| GB | 355 | 1,954 | 272 | 1,682 | 7.2× |
| IE | 59 | 368 | 117 | 251 | 3.1× |
| IT | 294 | 1,845 | 444 | 1,614 | 4.2× |
| NL | 49 | 288 | 107 | 181 | 2.7× |
| PL | 297 | 1,625 | 179 | 1,446 | **9.1×** |
| PT | 9 | 34 | 15 | 19 | 2.3× |

Pooled: 3,017 events → 17,356 event-days but only **3,213 unique
country-days** (mean multiplicity 5.4×, max 50 concurrent pixel-events on
one country-day). Of the 3,213 days, only 731 are single-event days.

## Consequences
1. **Legitimate spatially distinct measurements** are mixed with
   **duplicate energy accounting**: each event row is a valid pixel-level
   exposure measurement, but summing dE_heat or E_wind across events
   multiplies the same country energy.
2. The **event-mean** pooled WERR (mean of per-event ratios) overweights
   (a) days with many concurrent pixel-events and (b) small wind
   generation denominators (IE, CZ) — a ratio-of-means vs mean-of-ratios
   issue.
3. The pooled −0.036 is therefore **not** an energy-accounting quantity;
   it is an average of spatial measurements.

Crosswalk: `results/event_country_day_crosswalk.csv` (21,826 event×day
rows, with per-country-day multiplicity).

## Resolution
GATE 2 introduces the country-day estimand WERR_CD — see
COUNTRY_DAY_WERR_AUDIT.md.
