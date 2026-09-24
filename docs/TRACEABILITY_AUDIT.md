# R4 numerical traceability audit
- manuscript_values.csv maps every quantitative claim to source output + script.
- Placeholder scan of manuscript.docx: CLEAN (previously an unresolved
  `{np.abs(tf.iloc[:,1:].mean()).mean()/1e6:.0f}` literal rendered in §3.1 —
  fixed to a computed value ≈30×10⁶ kg/s).
- Event count: 3,017 WERR-analyzed events is canonical everywhere
  (results/werr_event_level.csv n=3017); pixel-event count 21,327 and
  sensitivity count 40,971 are separately labeled and consistent.
- β wording: narrative "0.5×10⁻⁴ °C/MW" refers to the NSDE coefficient
  (Table 2, 5.04×10⁻⁴ → text rounds to 0.5e-4? -> corrected: text now quotes
  the CSV value directly); domain β = -3.87×10⁻³ (Table 2 -38.68×10⁻⁴).
- WERR CI/count/slopes/turbine count/dates/B all traced; no stale values.
PASS: zero unresolved quantitative discrepancies.
