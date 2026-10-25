# Figure/Table Reference Order Audit (DOCUMENT_LOCK)

## Inventory
- Main figures: 8 PNGs (fig1_deployment … fig8_werr) + graphical_abstract.png + figures_editable.pptx. Captions Fig. 1–8.
- Main tables: 4 (Table 1–4). No supplementary package exists.

## Checks
- Body first-mention order (before captions): Figs 1,1,2,2,3,4,5,6,7,8 — ascending. Tables 1,2,3,4 — ascending.
- Panel notation normalized to ECM style: "Fig. 1a" → "Fig. 1(a)" (2 sites: §2.1 transects, §2.3 capacity field).
- Captions normalized "Figure N." → "Fig. N." per Elsevier caption convention.
- DEFECT FIXED: §2.4 cited "Fig. S1" but no supplementary document exists — orphan citation removed, kernels now described inline (alternative kernels remain cited to the falsification battery).
- No duplicate numbers, skipped numbers, inversions, or main-vs-supplement confusion. All 8 figure files + GA correspond to cited items; no orphan files.
- Automated regression: tests/test_document_integrity.py asserts caption style/order, first-mention order, and absence of Fig. S/Table S references. PASS.
