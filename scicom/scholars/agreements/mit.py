import copy

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors

from support import *


def mit_pageInfo (canvas, doc):
    canvas.saveState()

    # draw the header
    canvas.setFont('Times-Bold',12)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-50, 
                             'AMENDMENT TO PUBLICATION AGREEMENT')

    # draw the footer
    canvas.setFont('Times-Roman', 8)
    canvas.drawRightString(PAGE_WIDTH - 0.6 * inch, inch*.5, 
                       "MIT amendment to publication agreement rev. 1/27/06")

    # restore the previous canvas settings
    canvas.restoreState()

class MIT(object):
    """MIT addendum."""

    NAME = "MIT Amendment"
    VERSION = "1.0"

    def __call__(self, filename, manuscript="", journal="", author=[], 
                 publisher=""):
        """Generate the MIT agreement."""

        # check the parameters
        while len(author) < 4:
            author.append("")

        doc = getDocument(filename)

        Story = []

        # Section 1
        Story.append(
            Paragraph(
            """<seqreset id="main" /><seq id="main">. THIS Amendment hereby 
            modifies and supplements the attached Publication Agreement 
            concerning the following Article:""", styles['outer_style'])
            )

        journal_info_table = Table([
            [fillInRow(manuscript, "(manuscript title)", width=inch*5)],
            [fillInRow(journal, "(journal name)", width=inch*5)],
            ],
              )
        journal_info_table.hAlign = 'LEFT'
        Story.append(journal_info_table)

        # Section 2
        Story.append(
            Paragraph(
            """<seq id="main">. The parties to the Publication Agreement and
            to this Amendment are:""", styles['outer_style'])
            )

        journal_info_table = Table([
            [fillInRow(author[0], "(corresponding author)", width=inch*5)],
            [Paragraph("and", styles['outer_style'])],
            [fillInRow(journal, "(the Publisher)", width=inch*5)],
            ],
              )
        journal_info_table.hAlign = 'LEFT'
        Story.append(journal_info_table)

        # Section 3
        Story.append(
            Paragraph(
            """<seq id="main">. The parties agree that wherever there is any
            conflict between the Amendment and the Publication Agreement, 
            the provisions of this Amendment are paramount and the 
            Publication Agreement shall be construed accordingly.""",
            styles['outer_style'])
            )

        # Section 4
        Story.append(
            Paragraph(
            """<seq id="main">. Notwithstanding any terms in the Publication
Agreement to the contrary and in addition to the rights retained by Author 
or licensed by Published to Author in the Publication Agreement and any fair 
use rights of Author, Author and Publisher agree that the Author shall also 
retain the following rights:""",
            styles['outer_style'])
            )

        # 4a
        Story.append(
            Paragraph(
            """a.    The Author shall, without limitation, have the non-exclusive right to use, reproduce, distribute, create derivative works including update, perform, and display publicly, the Article in electronic, digital or print form in connection with the Author's teaching, conference presentations, lectures, other scholarly works, and for all of Author's academic and professional activities. """,
            styles['inner_style'])
            )

        # 4b
        Story.append(
            Paragraph(
                """b.   Once the Article has been published by Publisher, the Author shall also have all the non-exclusive rights necessary to make, or to authorize others to make, the final published version of the Article available in digital form over the Internet, including but not limited to a website under the control of the Author or the Author's employer or through any digital repository, such as MIT's DSpace or the National Library of Medicine's PubMed Central database.""",
            styles['inner_style'])
            )

        #4c
        Story.append(
            Paragraph(
                """c.    The Author further retains all non-exclusive rights necessary to grant to the Author's employing institution the non-exclusive right to use, reproduce, distribute, display, publicly perform, and make copies of the work in electronic, digital or in print form in connection with teaching, digital repositories, conference presentations, lectures, other scholarly works, and all academic and professional activities conducted at the Author's employing institution. """,
            styles['inner_style'])
            )

        # Section 5
        Story.append(
            Paragraph(
                """<seq id="main" />. <b>Final Agreement.</b> This Amendment and the Publication Agreement, taken together, constitute the final agreement between the Author and the Publisher with respect to the publication of the Article and allocation of rights under copyright in the Article. Any modification of or additions to the terms of this Amendment or to the Publication Agreement must be in writing and executed by both Publisher and Author in order to be effective.""",
            styles['outer_style'])
            )

        # Signature
        journal_info_table = Table([
            ["AUTHOR", " ", "PUBLISHER"],
            [fillInRow("", "(corresponding author on behalf of all authors)"),
             "", fillInRow("", "")],
            [fillInRow("", "Date"),
             "",
             fillInRow("", "Date")]
            ],
                                   colWidths=[inch*3, inch*.25, inch*3],
              )

        journal_info_table.hAlign = 'LEFT'
        Story.append(journal_info_table)

        # MIT Directive
        Story.append(
            Paragraph("<b>MIT Authors:</b>", styles['outer_style'])
            )
        Story.append(
            Paragraph("Please fax a copy of the agreement to 617-253-8894.  Direct any questions to amend-cip@mit.edu",
            styles['inner_style'])
            )


        agreement = "%s %s" % (self.NAME, self.VERSION)
        doc.build(Story, 
                  onFirstPage=mit_pageInfo, onLaterPages=mit_pageInfo)

if __name__ == '__main__':
    retaincc("test.pdf", "Extraordinary Measures",
               "Nature", ["B. Pants"], "The Publisher")
    
