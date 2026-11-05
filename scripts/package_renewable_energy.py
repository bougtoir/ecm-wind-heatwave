#!/usr/bin/env python3
"""Build the Renewable Energy submission and reproducibility zips from the
current tree (run after build_manuscript.py, build_cover_letter.py,
make_graphical_abstract.py). Flat relative arcnames only."""
import hashlib, pathlib, re, subprocess, zipfile
from docx import Document
from docx.shared import Pt

ROOT = pathlib.Path(".")
SUB = ROOT / "submission"
VENUE = "RenewableEnergy"

# cover letter as editable docx (same text as cover_letter.md)
md = (SUB / "cover_letter.md").read_text().splitlines()
doc = Document(); st = doc.styles["Normal"]; st.font.name = "Times New Roman"; st.font.size = Pt(12)
para = []
for line in md[2:] + [""]:
    if line.strip():
        para.append(line.strip())
    elif para:
        doc.add_paragraph(" ".join(para)); para = []
doc.save(SUB / "cover_letter.docx")

FIGS = ["fig1_deployment", "fig2_moisture", "fig3_heatwaves", "fig4_panel",
        "fig5_analogs", "fig6_eventstudy", "fig7_falsification", "fig8_werr"]
items = [("manuscript.docx", SUB / "manuscript.docx"),
         ("cover_letter.docx", SUB / "cover_letter.docx"),
         ("cover_letter.md", SUB / "cover_letter.md"),
         ("highlights.txt", SUB / "highlights.txt"),
         ("graphical_abstract.pdf", ROOT / "figs" / "graphical_abstract.pdf"),
         ("graphical_abstract.png", SUB / "graphical_abstract.png"),
         ("figures/figures_editable.pptx", SUB / "figures_editable.pptx"),
         ("references_verified.csv", ROOT / "references" / "references_verified.csv")]
items += [(f"figures/Figure_{i}.png", ROOT / "figs" / f"{n}.png") for i, n in enumerate(FIGS, 1)]
readme = ("Renewable Energy submission set (single-anonymized review).\n"
          "manuscript.docx - title page (author placeholder), abstract, keywords, highlights,\n"
          "  main text, tables, figure captions/figures, declarations, references.\n"
          "cover_letter.docx/.md, highlights.txt, graphical_abstract.pdf/.png,\n"
          "figures/Figure_1..8.png (separate artwork files) + figures_editable.pptx,\n"
          "references_verified.csv (Crossref-verified bibliography).\n"
          "Author to complete in Editorial Manager: name/affiliation/ORCID, GenAI declaration.\n")
sub_zip = ROOT / f"{VENUE}_submission_DOCUMENT_LOCK.zip"
with zipfile.ZipFile(sub_zip, "w", zipfile.ZIP_DEFLATED) as z:
    for arc, src in items:
        z.write(src, arc)
    z.writestr("README.txt", readme)

tracked = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split()
new = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"], capture_output=True, text=True, check=True).stdout.split()
files = sorted(f for f in set(tracked + new) if not f.endswith(".zip") and pathlib.Path(f).is_file())
files += sorted(str(p) for p in (ROOT / "data" / "processed").glob("*") if p.is_file())
rep_zip = ROOT / f"{VENUE}_reproducibility_DOCUMENT_LOCK.zip"
with zipfile.ZipFile(rep_zip, "w", zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(f, f)

for zp in (sub_zip, rep_zip):
    with zipfile.ZipFile(zp) as z:
        bad = [n for n in z.namelist() if n.startswith(("/", "../")) or ".." in n.split("/")]
        assert not bad and z.testzip() is None, (zp, bad)
        n = len(z.namelist())
    print(zp.name, n, "files", zp.stat().st_size, "bytes", hashlib.sha256(zp.read_bytes()).hexdigest())
