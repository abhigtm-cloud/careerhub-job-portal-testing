"""Builds the CareerHub academic report as a .pdf file using reportlab."""
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY

sys.path.insert(0, str(Path(__file__).parent))
from report_content import STUDENT, SECTIONS, TEST_CASE_TABLE
from report_results import ACTUAL_RESULTS, RESULTS_SUMMARY

OUT_PATH = Path(__file__).parent / "CareerHub_Academic_Report_Ritika_23BCA10289.pdf"
NAVY = colors.HexColor('#1A2E6E')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', fontSize=24, leading=30, alignment=TA_CENTER,
                           textColor=NAVY, spaceAfter=10, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle(name='CoverSub', fontSize=13, leading=18, alignment=TA_CENTER, spaceAfter=6))
styles.add(ParagraphStyle(name='CoverProject', fontSize=17, leading=22, alignment=TA_CENTER,
                           fontName='Helvetica-Bold', spaceBefore=20, spaceAfter=10))
styles.add(ParagraphStyle(name='CoverProjectTitle', fontSize=15, leading=20, alignment=TA_CENTER,
                           fontName='Helvetica-Bold', textColor=NAVY, spaceAfter=20))
styles.add(ParagraphStyle(name='CoverInfo', fontSize=12, leading=18, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='CoverNote', fontSize=8, leading=11, alignment=TA_CENTER,
                           textColor=colors.grey, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle(name='SectionHeading', fontSize=15, leading=19, textColor=NAVY,
                           fontName='Helvetica-Bold', spaceBefore=16, spaceAfter=8))
styles.add(ParagraphStyle(name='Body', fontSize=10.5, leading=15, alignment=TA_JUSTIFY, spaceAfter=8))
styles.add(ParagraphStyle(name='SummaryNote', fontSize=10, leading=14, fontName='Helvetica-Oblique', spaceAfter=8))


def build_cover(story):
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph('CHANDIGARH UNIVERSITY', styles['CoverTitle']))
    story.append(Paragraph('Department of Computer Applications', styles['CoverSub']))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph('Minor Project Report', styles['CoverProject']))
    story.append(Paragraph(f'"{STUDENT["title"]}"', styles['CoverProjectTitle']))
    story.append(Spacer(1, 0.6 * inch))

    info_lines = [
        f'Submitted By: {STUDENT["name"]}',
        f'UID: {STUDENT["uid"]}',
        f'Programme: {STUDENT["program"]}',
        f'Subject: {STUDENT["subject"]}',
        f'Submitted To: {STUDENT["submitted_to"]}',
        f'Academic Year: {STUDENT["academic_year"]}',
    ]
    for line in info_lines:
        story.append(Paragraph(line, styles['CoverInfo']))

    story.append(Spacer(1, 0.8 * inch))
    story.append(Paragraph(
        '[University logo and exact cover-page layout to be matched to the official Chandigarh '
        'University template before final submission; no reference image was available at '
        'generation time.]',
        styles['CoverNote']
    ))
    story.append(PageBreak())


def build_test_case_table():
    data = [['ID', 'Test Case', 'Expected Result', 'Category']] + list(TEST_CASE_TABLE)
    table = Table(data, colWidths=[0.5 * inch, 2.3 * inch, 2.6 * inch, 1.1 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F2F4FA')]),
    ]))
    return table


def build_results_table():
    data = [['Test Suite (pytest file / tool)', 'Passed', 'Failed/Error', 'Notes']] + list(ACTUAL_RESULTS)
    table = Table(data, colWidths=[2.3 * inch, 0.7 * inch, 0.9 * inch, 2.6 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F2F4FA')]),
    ]))
    return table


def build():
    doc = SimpleDocTemplate(str(OUT_PATH), pagesize=A4,
                             topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                             leftMargin=0.8 * inch, rightMargin=0.8 * inch)
    story = []
    build_cover(story)

    for heading, body in SECTIONS:
        story.append(Paragraph(heading, styles['SectionHeading']))
        if heading == 'Test Cases':
            story.append(Paragraph(
                'The table below lists the primary test cases implemented across the Selenium UI '
                'suite, the Requests-based API suite, and direct PyMongo database checks.',
                styles['Body']
            ))
            story.append(build_test_case_table())
            story.append(Spacer(1, 10))
            continue
        if heading == 'Actual Execution Results':
            story.append(Paragraph(
                'The table below reports genuine pass/fail counts captured from executing the suite '
                'against the running application on this machine.',
                styles['Body']
            ))
            story.append(build_results_table())
            story.append(Spacer(1, 6))
            story.append(Paragraph(RESULTS_SUMMARY, styles['SummaryNote']))
            continue
        if heading == 'Results':
            story.append(Paragraph(RESULTS_SUMMARY, styles['Body']))
            continue
        for para in body.split('\n'):
            story.append(Paragraph(para, styles['Body']))

    doc.build(story)
    print(f'PDF written to {OUT_PATH}')


if __name__ == '__main__':
    build()
