# Final Document Integrity Audit (one-shot gate)

Base: public main 4b414ab + verified submission set. Branch devin/document-integrity.

## Gate verdicts
- GATE 0 inventory/rules: PASS. Items: manuscript.docx (8 figs, 4 tables, 30 refs, 246-word abstract), cover_letter.md, highlights.txt, graphical_abstract.png, figs_editable.pptx, 7 zip files, no supplement. ECM rules: Fig.-style captions, Vancouver numbered order, separate figure files, ≤250-word abstract — checked against Elsevier guide conventions (accessed 2026-10-25).
- GATE 1 references: PASS. 30/30 cited, ordered, Crossref-verified; see REFERENCES_BIDIRECTIONAL_ORDER_AUDIT.md.
- GATE 2 figures/tables: PASS WITH FIX. Orphan "Fig. S1" citation removed; captions normalized to "Fig. N."; panel notation to "Fig. 1(a)"; order 1→8 / 1→4 verified.
- GATE 3 numeric consistency: PASS. All values regenerated from canonical CSVs; WERR_CD +0.0009 [−0.0048,+0.0098] and event-mean −0.036 kept as distinct estimands; manuscript_values.csv/NUMERIC_PROVENANCE refreshed; automated tests assert canonical equality.
- GATE 4 OMML: PASS WITH FIX. Added 3 genuine editable equations (WFI, WERR_e, WERR_CD); verified in OOXML.
- GATE 5 formatting: PASS. No asterisks, no char-grid, default proportional spacing.
- GATE 6 rebuild+regression: PASS. Fresh isolated clone rebuilt identical artifacts; 7 new regression tests; total pytest 11/11.
- GATE 7 hostile review: PASS WITH FIXES. Fixes listed under gates 2/4; no further justified corrections found (asterisk scan, equation editability, numbering, typography, numerical mismatches, compliance claims all re-verified).

## Defect register (fixed this gate)
1. "Fig. S1" orphan citation (no supplement) → removed.
2. Caption style "Figure N." → "Fig. N." (ECM).
3. "Fig. 1a" → "Fig. 1(a)" panel notation (×2).
4. Zero display equations → 3 OMML equations for WFI/WERR/WERR_CD.

No scientific content changed; no value edited by hand.
