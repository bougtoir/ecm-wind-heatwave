# Next target: Renewable Energy (Elsevier, ISSN 0960-1481)

Sources (accessed 2026-11-05 UTC via rendered Chrome; text snapshots + SHA-256 in
`docs/journal_guides/LEDGER.csv`):
- Guide for Authors: https://www.sciencedirect.com/journal/renewable-energy/publish/guide-for-authors
- Aims and scope: https://www.sciencedirect.com/journal/renewable-energy/about/aims-and-scope
- Open-access options: https://www.sciencedirect.com/journal/renewable-energy/publish/open-access-options
- Fully-OA status of alternatives: DOAJ API (`docs/journal_guides/doaj_*.json`)

## Candidate evaluation

| Candidate | Scope fit for this paper | Charges (live check) | Length rule | Verdict |
|---|---|---|---|---|
| **Renewable Energy** | Explicit areas "Wind Energy Technology" and "Climatology and Meteorology"; in scope when concerned with renewable power generation — net delivered wind energy is the estimand | Hybrid: subscription route, no publication fee; optional OA APC USD 4,150 | Guide 4,000–6,000 words; ≤50 refs; word count must be stated | **Selected** |
| Applied Energy | Applied energy systems; atmospheric-observational paper with null aggregate result is a weaker fit; same desk-reject risk profile as ECM | Hybrid (subscription route free) | No fixed range found | Not chosen (fit) |
| Energy | Energy engineering; Full Length Article 5,000–7,000 words incl. tables/figures, "manuscripts exceeding word limits may be rejected" | Hybrid | 5,000–7,000 | Not chosen (fit + length) |
| Energy Policy | Policy-analysis venue; paper has no policy design content | Hybrid | 4,500–8,000 | Not chosen (fit) |
| Environmental Research Letters | Good fit | Fully OA with APC (DOAJ: has_apc = true) | — | Excluded (mandatory APC) |
| Weather and Climate Extremes | Good meteorology fit | Fully OA with APC (DOAJ: has_apc = true) | — | Excluded (mandatory APC) |
| Wind Energy (Wiley) | Good fit | Fully OA with APC (DOAJ: has_apc = true) | — | Excluded (mandatory APC) |
| J. Renewable and Sustainable Energy (AIP) | Fit | Not in DOAJ (hybrid) | — | Not chosen (lower standing than RE) |

Reasons for Renewable Energy: the two named scope areas cover exactly the paper's
energy (wind generation, demand offset) and meteorology (ERA5, heatwaves) halves; no
mandatory author charge; single-anonymized review matches the existing title page;
numbered references in order of first appearance match the existing citation machinery.

## Rules (Guide for Authors) and how the package meets them

| Rule | Requirement | Package |
|---|---|---|
| Review model | Single anonymized | Author line kept as placeholder for the author to fill at submission |
| Paper length | Guide 4,000–6,000 words excl. captions/refs; **state word count at submission** | 3,094 words (title page + cover letter, computed at build). Below the advisory range — flagged risk |
| References | ≤50; numbers in square brackets, numbered in order of appearance; any consistent style | 30 refs, `[n]` brackets with ranges, Elsevier numbered layout, all Crossref-verified |
| Abstract | ≤250 words, no references | 250 words, no citations |
| Keywords | 1–6, English | 6 |
| Highlights | Required, 3–5 bullets, ≤85 chars incl. spaces, separate editable file with "highlights" in the name | 5 bullets, max 72 chars, `highlights.txt` |
| Graphical abstract | Encouraged; separate file; TIFF/EPS/PDF/MS Office preferred | `graphical_abstract.pdf` + PNG |
| Figures | Separate files, cited, numbered by order of appearance, logical names (Figure_1 …) | `figures/Figure_1.png … Figure_8.png` + editable PPTX; also embedded in the single-file manuscript |
| Declarations | Competing interest, CRediT, funding, data, GenAI declaration | Present; GenAI declaration left for the author (policy wording requires author decision) |

## Rules diff vs ECM

| Item | ECM (as packaged) | Renewable Energy |
|---|---|---|
| Citation display | Superscript numbers | `[n]` square brackets (changed) |
| Reference entries | Title. Journal (year). DOI | Authors, title, journal volume (year) pages. DOI (changed; authors/volume/pages from Crossref) |
| Word count statement | Not required | Required (added to title page and cover letter) |
| Length | No cap used (≤9,000 QC) | 4,000–6,000 advisory (QC reports, does not fail) |
| Reference cap | none | ≤50 (QC + test) |
| Keywords | EM field only | 1–6 in manuscript (added) |
| Highlights / GA | Same rules | Same rules |
