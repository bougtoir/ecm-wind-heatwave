# Word OMML Audit (DOCUMENT_LOCK)

## Finding
The manuscript defined all estimands only in prose — no display equations existed. A quantitative ECM paper's key metrics (WFI exposure, per-event WERR, country-day WERR_CD) justified genuine editable equations.

## Action (canonical source: scripts/build_manuscript.py)
Added OMML display equations via m:oMathPara (centered, Cambria Math):
1. Eq.1 §2.4: WFI(c,d) = Σ_{k=1} exp(−50k/100)·cap_d(u_k(c,d)) — n-ary sum, fraction, subscripts.
2. Eq.2 §2.7: WERR_e = ΔE_heat,e / E_wind,e — subscripts, fraction.
3. Eq.3 §2.7: WERR_CD = (Σ_{d∈D_c} ΔE_heat,d)/(Σ_{d∈D_c} E_wind,d) — two n-ary sums, fraction.
Plus a definition paragraph for ΔE_heat,d = ŝ_c·β̂_r·WFI_r(d)·24h·φ_d (inline symbols — intentionally kept inline per gate rule).

## Verification
- word/document.xml contains ≥3 m:oMath elements, 2 n-ary operators, 3+ fractions; no drawing/picture inside math regions.
- test_document_integrity.py::test_omml_equations_present_and_editable enforces this.
- Justified inline-text exceptions: β×WFI, ΔT, p/CI values, units, Table-2 β_WFI header — inline per convention.

Counts: 3 display equations added; 0 raw-LaTeX remnants; 0 image equations. PASS.
