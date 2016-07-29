
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors

import reportlab.lib.styles

import os.path
import scicom.scholars.static

PAGE_HEIGHT = inch * 11
PAGE_WIDTH = inch * 8.5
styles = getSampleStyleSheet()

styles.add(reportlab.lib.styles.ParagraphStyle(
    'outer_style', styles['Normal']))
styles['outer_style'].fontSize = 9
styles['outer_style'].leading = 10

styles['outer_style'].spaceAfter = 8
styles['outer_style'].spaceBefore = 6
styles['outer_style'].leftIndent = inch * 0.12
styles['outer_style'].firstLineIndent = -1 * styles['outer_style'].leftIndent

styles.add(reportlab.lib.styles.ParagraphStyle(
        'inner_style', styles['outer_style']))
styles['inner_style'].leftIndent = inch * 0.50
styles['inner_style'].firstLineIndent = -0.25 * inch

styles.add(reportlab.lib.styles.ParagraphStyle(
    'disclaimer', styles['outer_style']))
styles['disclaimer'].fontSize = 8
styles['disclaimer'].leading = 9
styles['disclaimer'].leftIndent = \
    styles['disclaimer'].firstLineIndent = 0

styles.add(reportlab.lib.styles.ParagraphStyle(
    'boxed_paragraph', styles['disclaimer']))
styles['boxed_paragraph'].fontName = 'Helvetica'
styles['disclaimer'].fontSize = 7
styles['disclaimer'].leading = 8

Title = "ADDENDUM TO PUBLICATION AGREEMENT"
Footer = "Model Author's Addendum to Publication Agreement 1.0"
Disclaimer = "<b>Neither Creative Commons nor Science Commons are parties to this agreement or provide legal advice.  Please visit www.sciencecommons.org for more information and specific disclaimers.</b>"

def getDocument(filename):
    """Returns a ReportLab Document with the appropriate margins set."""

    doc = SimpleDocTemplate(filename)
    doc.pagesize = (PAGE_WIDTH, PAGE_HEIGHT)
    doc.leftMargin = doc.rightMargin = \
        doc.bottomMargin = inch * 0.5

    doc.topMargin = inch

    return doc

def pageInfo (agreement_name, canvas, doc):
    canvas.saveState()

    # draw the header
    canvas.setFont('Times-Bold',12)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-50, Title)

    # draw the footer
    canvas.setFont('Times-Roman', 8)
    try:
        canvas.drawImage(os.path.abspath(os.path.join(
                    os.path.dirname(scicom.scholars.static.__file__), 'images',
                    'scicom.gif')), inch * 0.5, inch * 0.6,
                         width=inch, height=inch*.28)
    except:
        pass

    canvas.drawString(0.6 * inch, inch*.5, agreement_name)
    canvas.drawString(0.6 * inch, inch*.375, 'www.sciencecommons.org')

    canvas.restoreState()

def sparcPageInfo(agreement_name, canvas, doc):

    # draw the basics
    pageInfo(agreement_name, canvas, doc)

    # draw the SPARC logo and name
    canvas.saveState()

    canvas.setFont('Times-Roman', 8)
    try:
        canvas.drawImage(os.path.abspath(os.path.join(
                    os.path.dirname(scicom.scholars.static.__file__), 'images',
                    'sparc-wordmark.png')), PAGE_WIDTH - inch * 1.6, 
                         inch * 0.625,
                         width=inch, height=inch*.25)
    except:
        pass

    canvas.drawRightString(PAGE_WIDTH - 0.6 * inch, inch*.5, 'SPARC Author Addendum 3.0')
    canvas.drawRightString(PAGE_WIDTH - 0.6 * inch, inch*.375, 'www.ari.org/sparc/')
    
    # restore the starting state of the canvas
    canvas.restoreState()

def BoxedText(contents):
    """Returns a Table object wrapping the contents with a border around
    the entire table."""

    result = Table(contents)
    result.setStyle(
        TableStyle([
                ('BOX', (0,0), (-1,-1), 0.25, colors.black)
                ])
        )

    return result

def fillInRow(value, label, width=inch*3):

    result = Table([ [value],
                     [label]
                     ],
                   rowHeights=[inch*0.2, inch*0.1],
                   colWidths=[width])
    result.setStyle(
        TableStyle( [('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                     ('VALIGN', (0, 0), (0, 0), 'BOTTOM'),
                     ('VALIGN', (0, 1), (0, 1), 'TOP'),
                     ('FONTSIZE', (0, 1), (0, 1), 8),
                     ('LINEABOVE', (0, 1), (0, 1), 0.5, colors.black),
                     ('BOTTOMPADDING', (0,0), (0,0), 0),
                     ('TOPPADDING', (0, 1), (0, 1), 0),
                     ]
                    )
        )

    return result
