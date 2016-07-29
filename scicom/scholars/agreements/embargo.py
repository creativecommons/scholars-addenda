import copy

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.lib import colors

from support import *

class Embargo(object):

    NAME = "Delayed Access"
    VERSION = "1.0"

    def __call__(self, filename, manuscript="", journal="", author=[], 
                 publisher=""):
        """Generate the No Embargo agreement."""

        # check the parameters
        while len(author) < 4:
            author.append("")

        doc = getDocument(filename)

        Story = []

        # Section 1
        Story.append(
            Paragraph(
            """<seqreset id="main" /><seq id="main">. THIS ADDENDUM hereby modifies and supplements
            the attached Publication Agreement concerning the following
            Article:""", styles['outer_style'])
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
            """<seq id="main">. The parties to the Publication Agreement as
            modified and supplemented by this Addendum are:""", styles['outer_style'])
            )

        journal_info_table = Table([
            [fillInRow(author[0],"(corresponding author)",), "", ""],
            [fillInRow(author[1],""), "", ""],
            [fillInRow(author[2],""), "", ""],
            [fillInRow(author[3],
                       """(Individually or, if more than one author, collectively, Author)"""), "", fillInRow(publisher, "(Publisher")],
            ],
                                   colWidths=[inch*3, inch * 0.25, inch*3],
              )
        journal_info_table.hAlign = 'LEFT'
        Story.append(journal_info_table)

        # Section 3
        Story.append(
            Paragraph(
            """<seq id="main">. This Addendum and the Publication Agreement,
            taken together, allocate all rights under copyright with respect
            to all versions of the Article.  The parties agree that wherever
            there is any conflict between this Addendum and the Publication
            Agreement, the provisions of this Addendum are paramount and the
            Publication Agreement shall be construed accordingly.""",
            styles['outer_style'])
            )

        # Section 4
        Story.append(
            Paragraph(
            """<seq id="main">. Notwithstanding any terms in the Publication
            Agreement to the contrary, AUTHOR and PUBLISHER agree as follows:""",
            styles['outer_style'])
            )

        Story.append(
            Paragraph(
            """<seqreset id="Sec4" /><seq template="%(main)s.%(Sec4+)s"/>. <b>Professional Activities.</b>
            Author retains the non-exclusive right to create derivative works
            from the Article and to reproduce, to distribute, to publicly
            perform, and to publicly display the Article in connection with
            Author's teaching, conference presentations, lectures, other
            scholarly works, and professional activities. """,
            styles['inner_style'])
            )

        Story.append(
            Paragraph(
            """<seq template="%(main)s.%(Sec4+)s"/>. <b>Author's Final Version. </b>
            Author retains the non-exclusive right to distribute copies of
            Author's final version by means of any web server from which members
            of the general public can download copies without charge.
            "Author's final version" means the final version accepted for journal
            publication, and includes all modifications from the publishing peer
            review process. """,
            styles['inner_style'])
            )

        Story.append(
            Paragraph(
            """<seq template="%(main)s.%(Sec4+)s"/>. <b>Published Version. </b>
            Author has the non-exclusive right to distribute copies of the
            published version of the Article by means of any web server from
            which members of the general public can download copies without
            charge, provided that Author cites the journal in which the Article
            has been published as the source of first publication, and further,
            that Author shall not authorize public access to the published version
            any earlier than six months from the date that Publisher first makes
            the final, published version available to Publisher's subscribers.
            "Published version" means the version of the Article distributed by
            Publisher to subscribers or readers of the Journal.""",
            styles['inner_style'])
            )

        Story.append(
            Paragraph(
            """<seq template="%(main)s.%(Sec4+)s"/>.
            <b>Acknowledgment of Prior License Grants.</b>  Where applicable,
            Publisher acknowledges that Author's assignment of copyright or
            Author's grant of exclusive rights in the Publication Agreement is
            subject to Author's prior grant of a non-exclusive copyright license
            to Author's employing institution and/or to a funding entity that
            financially supported the research reflected in the Article as part
            of an agreement between Author or Author's employing institution
            and such funding entity, such as an agency of the United States
            government.""",
            styles['inner_style'])
            )

        # Section 5
        Story.append(
            Paragraph(
            """<seq id="main">. For record keeping purposes, Author requests
            that Publisher sign a copy of this Addendum and return it to Author.
            However, if Publisher publishes the Article in the journal or in any
            other form without signing a copy of this Addendum, such publication
            manifests Publisher's assent to the terms of this Addendum.""",
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


        # Disclaimer
        Story.append(
            Paragraph(Disclaimer, styles['disclaimer'])
            )

        agreement = "%s %s" % (self.NAME, self.VERSION)
        doc.build(Story, 
                  onFirstPage=lambda x,y: pageInfo(agreement, x, y), 
                  onLaterPages=lambda x,y: pageInfo(agreement, x, y))

if __name__ == '__main__':
    embargo("test.pdf", "Extraordinary Measures",
               "Nature", ["B. Pants"], "The Publisher")
    
