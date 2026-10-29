"""Drift Documentation Builder — High-Quality Professional DOCX Generator.

Provides standardized typography, colors, table formatting, callout blocks,
and structure for enterprise-grade technical and user documentation.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, List, Optional, Tuple

import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

# Color Palette Constants
COLOR_NAVY = RGBColor(27, 54, 93)        # #1B365D - Primary Headers
COLOR_SLATE = RGBColor(43, 91, 132)      # #2B5B84 - Secondary Headers
COLOR_CHARCOAL = RGBColor(44, 62, 80)    # #2C3E50 - Body Text
COLOR_MUTED = RGBColor(108, 117, 125)    # #6C757D - Captions & Subtitles
COLOR_GREEN = RGBColor(30, 126, 52)      # #1E7E34 - Success / Pass
COLOR_RED = RGBColor(189, 33, 48)        # #BD2130 - Alert / Fail
COLOR_AMBER = RGBColor(133, 100, 4)      # #856404 - Warning

HEX_NAVY = "1B365D"
HEX_SLATE = "2B5B84"
HEX_LIGHT_BG = "F4F6F9"
HEX_BORDER = "D0D7DE"
HEX_CODE_BG = "F8F9FA"
HEX_CALLOUT_INFO_BG = "EBF3FB"
HEX_CALLOUT_WARN_BG = "FFF8E6"
HEX_CALLOUT_SUCCESS_BG = "EAF7EE"


def create_document() -> docx.Document:
    """Initialize a document with standardized 1-inch margins and default styles."""
    doc = docx.Document()
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Set normal style
    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = COLOR_CHARCOAL
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(4)
    return doc


def add_cover_page(
    doc: docx.Document,
    title: str,
    subtitle: str,
    doc_type: str,
    metadata: list[tuple[str, str]],
) -> None:
    """Creates a clean executive title block at the top of the document."""
    # Top spacing
    p_top = doc.add_paragraph()
    p_top.paragraph_format.space_before = Pt(36)

    # Document Type Pill / Label
    p_badge = doc.add_paragraph()
    p_badge.paragraph_format.space_after = Pt(8)
    r_badge = p_badge.add_run(f"DRIFT • {doc_type.upper()}")
    r_badge.font.name = "Arial"
    r_badge.font.size = Pt(10)
    r_badge.font.bold = True
    r_badge.font.color.rgb = COLOR_SLATE

    # Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run(title)
    r_title.font.name = "Arial"
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run(subtitle)
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = COLOR_MUTED

    # Metadata Table
    table = doc.add_table(rows=len(metadata), cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    for idx, (label, val) in enumerate(metadata):
        c0 = table.cell(idx, 0)
        c1 = table.cell(idx, 1)

        c0.width = Inches(2.2)
        c1.width = Inches(4.3)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        p0.paragraph_format.space_before = Pt(2)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = COLOR_SLATE

        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.space_before = Pt(2)
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_CHARCOAL

        # Shading on label cell
        tcPr0 = c0._tc.get_or_add_tcPr()
        tcPr0.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{HEX_LIGHT_BG}"/>'))

    # Spacing and separator line
    p_sep = doc.add_paragraph()
    p_sep.paragraph_format.space_before = Pt(18)
    p_sep.paragraph_format.space_after = Pt(18)
    doc.add_page_break()


def add_heading_1(doc: docx.Document, text: str) -> None:
    """Numbered or primary section heading."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY


def add_heading_2(doc: docx.Document, text: str) -> None:
    """Subsection heading."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_SLATE


def add_heading_3(doc: docx.Document, text: str) -> None:
    """Sub-subsection heading."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_CHARCOAL


def add_paragraph(
    doc: docx.Document,
    text: str,
    bold_prefix: Optional[str] = None,
    italic: bool = False,
    space_after: int = 5,
) -> None:
    """Adds a standard body paragraph with optional bold lead-in."""
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_NAVY
    run = p.add_run(text)
    run.font.italic = italic
    run.font.size = Pt(10.5)
    run.font.color.rgb = COLOR_CHARCOAL


def add_bullet(
    doc: docx.Document,
    text: str,
    bold_prefix: Optional[str] = None,
    level: int = 0,
) -> None:
    """Adds a bullet point with clean spacing and optional prefix."""
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_NAVY
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_CHARCOAL


def add_callout(
    doc: docx.Document,
    text: str,
    title: str = "NOTE",
    level: str = "info",
) -> None:
    """Render a highlighted callout box with custom background and left border."""
    bg_hex = HEX_CALLOUT_INFO_BG
    border_color = HEX_SLATE
    title_color = COLOR_SLATE

    if level == "warning":
        bg_hex = HEX_CALLOUT_WARN_BG
        border_color = "E0A800"
        title_color = COLOR_AMBER
    elif level == "success":
        bg_hex = HEX_CALLOUT_SUCCESS_BG
        border_color = "28A745"
        title_color = COLOR_GREEN
    elif level == "danger":
        bg_hex = "FCE8E6"
        border_color = "DC3545"
        title_color = COLOR_RED

    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)

    tcPr = cell._tc.get_or_add_tcPr()
    # Background fill
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{bg_hex}"/>'))
    # Left thick border, no other borders
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="none"/>'
        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>'
        f'  <w:bottom w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    # Padding inside cell
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="120" w:type="dxa"/>'
        f'  <w:left w:w="180" w:type="dxa"/>'
        f'  <w:bottom w:w="120" w:type="dxa"/>'
        f'  <w:right w:w="180" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15

    r_title = p.add_run(f"[{title}] ")
    r_title.font.bold = True
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = title_color

    r_text = p.add_run(text)
    r_text.font.size = Pt(9.5)
    r_text.font.color.rgb = COLOR_CHARCOAL

    # Spacer after callout
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_before = Pt(0)
    p_space.paragraph_format.space_after = Pt(4)


def add_code_block(doc: docx.Document, code_text: str) -> None:
    """Render a shaded monospaced code or configuration block."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)

    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{HEX_CODE_BG}"/>'))
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
        f'  <w:left w:val="single" w:sz="18" w:space="0" w:color="{HEX_NAVY}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
        f'  <w:right w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="100" w:type="dxa"/>'
        f'  <w:left w:w="160" w:type="dxa"/>'
        f'  <w:bottom w:w="100" w:type="dxa"/>'
        f'  <w:right w:w="160" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05

    r = p.add_run(code_text.strip())
    r.font.name = "Consolas"
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(33, 37, 41)

    # Spacer
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(4)


def add_table(
    doc: docx.Document,
    headers: list[str],
    data: list[list[str]],
    col_widths: Optional[list[float]] = None,
) -> None:
    """Render a fully styled table with navy headers, zebra stripes, and borders."""
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Format header row
    hdr_cells = table.rows[0].cells
    for idx, heading in enumerate(headers):
        cell = hdr_cells[idx]
        if col_widths and idx < len(col_widths):
            cell.width = Inches(col_widths[idx])

        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{HEX_NAVY}"/>'))
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:top w:val="single" w:sz="8" w:space="0" w:color="{HEX_NAVY}"/>'
            f'  <w:left w:val="none"/>'
            f'  <w:bottom w:val="single" w:sz="16" w:space="0" w:color="{HEX_SLATE}"/>'
            f'  <w:right w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'  <w:top w:w="120" w:type="dxa"/>'
            f'  <w:left w:w="120" w:type="dxa"/>'
            f'  <w:bottom w:w="120" w:type="dxa"/>'
            f'  <w:right w:w="120" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(heading)
        run.font.name = "Arial"
        run.font.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Format data rows
    for r_idx, row in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        is_even = (r_idx % 2 == 1)
        row_bg = HEX_LIGHT_BG if is_even else "FFFFFF"

        for c_idx, val in enumerate(row):
            cell = row_cells[c_idx]
            if col_widths and c_idx < len(col_widths):
                cell.width = Inches(col_widths[c_idx])

            tcPr = cell._tc.get_or_add_tcPr()
            if row_bg != "FFFFFF":
                tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{row_bg}"/>'))

            borders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
                f'  <w:left w:val="none"/>'
                f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
                f'  <w:right w:val="none"/>'
                f'</w:tcBorders>'
            )
            tcPr.append(borders)

            tcMar = parse_xml(
                f'<w:tcMar {nsdecls("w")}>'
                f'  <w:top w:w="80" w:type="dxa"/>'
                f'  <w:left w:w="120" w:type="dxa"/>'
                f'  <w:bottom w:w="80" w:type="dxa"/>'
                f'  <w:right w:w="120" w:type="dxa"/>'
                f'</w:tcMar>'
            )
            tcPr.append(tcMar)

            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.1
            run = p.add_run(val)
            run.font.size = Pt(9.0)
            run.font.color.rgb = COLOR_CHARCOAL

    # Spacer after table
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_after = Pt(6)
