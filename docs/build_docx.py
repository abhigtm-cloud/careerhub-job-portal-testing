"""Builds the CareerHub academic report as a .docx file using python-docx."""
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

sys.path.insert(0, str(Path(__file__).parent))
from report_content import STUDENT, SECTIONS, TEST_CASE_TABLE
from report_results import ACTUAL_RESULTS, RESULTS_SUMMARY

OUT_PATH = Path(__file__).parent / f"CareerHub_Academic_Report_Ritika_23BCA10289.docx"
NAVY = RGBColor(0x1A, 0x2E, 0x6E)


def add_cover_page(doc):
    for _ in range(4):
        doc.add_paragraph()
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run('CHANDIGARH UNIVERSITY')
    run.bold = True
    run.font.size = Pt(26)
    run.font.color.rgb = NAVY

    sub = doc.add_paragraph()
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_run = sub.add_run('Department of Computer Applications')
    sub_run.font.size = Pt(14)

    doc.add_paragraph()
    doc.add_paragraph()

    proj = doc.add_paragraph()
    proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    proj_run = proj.add_run('Minor Project Report')
    proj_run.bold = True
    proj_run.font.size = Pt(18)

    doc.add_paragraph()

    titlep = doc.add_paragraph()
    titlep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    titlep_run = titlep.add_run(f'"{STUDENT["title"]}"')
    titlep_run.bold = True
    titlep_run.font.size = Pt(16)
    titlep_run.font.color.rgb = NAVY

    for _ in range(4):
        doc.add_paragraph()

    info_lines = [
        f'Submitted By: {STUDENT["name"]}',
        f'UID: {STUDENT["uid"]}',
        f'Programme: {STUDENT["program"]}',
        f'Subject: {STUDENT["subject"]}',
        f'Submitted To: {STUDENT["submitted_to"]}',
        f'Academic Year: {STUDENT["academic_year"]}',
    ]
    for line in info_lines:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(line)
        r.font.size = Pt(13)

    for _ in range(3):
        doc.add_paragraph()
    note = doc.add_paragraph()
    note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    note_run = note.add_run(
        '[University logo and exact cover-page layout to be matched to the official '
        'Chandigarh University template before final submission; no reference image was '
        'available at generation time.]'
    )
    note_run.italic = True
    note_run.font.size = Pt(9)
    note_run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)

    doc.add_page_break()


def set_cell_background(cell, color_hex):
    shd = cell._tc.get_or_add_tcPr()
    el = shd.makeelement(qn('w:shd'), {qn('w:fill'): color_hex})
    shd.append(el)


def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = NAVY
    return h


def add_test_case_table(doc):
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Light Grid Accent 1'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    headers = ['ID', 'Test Case', 'Expected Result', 'Category']
    for i, h in enumerate(headers):
        hdr[i].text = h
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.bold = True
    for row in TEST_CASE_TABLE:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
    doc.add_paragraph()


def add_results_table(doc):
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Light Grid Accent 1'
    hdr = table.rows[0].cells
    for i, h in enumerate(['Test Suite (pytest file / tool)', 'Passed', 'Failed/Error', 'Notes']):
        hdr[i].text = h
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.bold = True
    for row in ACTUAL_RESULTS:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = str(val)
    doc.add_paragraph()
    summary = doc.add_paragraph()
    summary.add_run(RESULTS_SUMMARY).italic = True


def build():
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    add_cover_page(doc)

    for heading, body in SECTIONS:
        add_heading(doc, heading, level=1)
        if heading == 'Test Cases':
            doc.add_paragraph(
                'The table below lists the primary test cases implemented across the Selenium UI suite, '
                'the Requests-based API suite, and direct PyMongo database checks.'
            )
            add_test_case_table(doc)
            continue
        if heading == 'Actual Execution Results':
            doc.add_paragraph(
                'The table below reports genuine pass/fail counts captured from executing the suite '
                'against the running application on this machine.'
            )
            add_results_table(doc)
            continue
        if heading == 'Results':
            doc.add_paragraph(RESULTS_SUMMARY)
            continue
        for para in body.split('\n'):
            doc.add_paragraph(para)

    doc.save(OUT_PATH)
    print(f'DOCX written to {OUT_PATH}')


if __name__ == '__main__':
    build()
