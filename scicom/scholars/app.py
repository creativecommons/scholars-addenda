## Copyright (c) 2006-2007 Nathan R. Yergler, Creative Commons

## Permission is hereby granted, free of charge, to any person obtaining
## a copy of this software and associated documentation files (the "Software"),
## to deal in the Software without restriction, including without limitation
## the rights to use, copy, modify, merge, publish, distribute, sublicense,
## and/or sell copies of the Software, and to permit persons to whom the
## Software is furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
## DEALINGS IN THE SOFTWARE.

import os
import md5
import cherrypy
import genshi.template
from paste import httpserver

import scicom.scholars
from scicom.scholars import agreements

STATIC_DIR = os.path.abspath(
    os.path.dirname(scicom.scholars.static.__file__)
    )
TEMPLATE_DIR = os.path.abspath(
    os.path.dirname(scicom.scholars.templates.__file__)
    )

class MissingParameterException(Exception):
    pass

class ScholarsCopyright(object):

    def __init__(self):
        
        # create a persistent connection to our database
        self._stats = scicom.scholars.stats.StatsMapper()

        # create a template loader instance
        self._loader = genshi.template.TemplateLoader([TEMPLATE_DIR])

    @cherrypy.expose
    def index(self, default=None):
        """Return the index page."""

        template = self._loader.load('index.html')
        return template.generate(partner_id='direct',
                                 default=default,
                                 agreements=agreements.handlers).render('xhtml')

    @cherrypy.expose
    def stats(self):
        """Return the stats page."""

        template = self._loader.load('stats.html')
        return template.generate(total = self._stats.total(),
                                 counts = self._stats.counts()).render('xhtml')
    
    # serve up static files for HTML, CSS, Javascript, etc.
    _cp_config = {'tools.staticdir.on':True,
                  'tools.staticdir.root':STATIC_DIR,
                  'tools.staticdir.dir':''}

    @cherrypy.expose
    def generate(self, manuscript='', journal='', author=[],
                 publisher='', agreement='', partner_id='direct'):
        
        # make sure author is a list
        try:
            author.append(None)
            del author[-1]
        except AttributeError, e:
            # author must be a string
            author = [author]

        # validate input
        if "" in (manuscript, journal, publisher, agreement) or \
                len(author) == 0:
            raise MissingParameterException

        if len(journal) > 255: journal = journal[:255]

        # generate the agreement
        pdf_contents = scicom.scholars.generate.create_pdf(
            manuscript, journal, author, publisher, agreement)

        self._stats.session.add(
            scicom.scholars.stats.AgreementStatistic(
                partner_id, journal, agreement)
            )
        self._stats.session.flush()

        # set the appropriate headers
        cherrypy.response.headers['Expires'] = '0'
        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        cherrypy.response.headers['Cache-Control'] = \
            'must-revalidate, post-check=0, pre-check=0'
        cherrypy.response.headers['Content-Disposition'] = \
            'attachment; filename="agreement.pdf"'

        # read the response, unlink the temp file and return it
        return pdf_contents

    @cherrypy.expose
    def iframe(self, partner_id=None, stylesheet=None, default=None):

        # partner_id is required
        if partner_id is None:
            raise MissingParameterException()

        # render the template and return the value
        template = self._loader.load('iframe.html')
        stream = template.generate(partner_id=partner_id,
                                   default=default,
                                   stylesheet=stylesheet,
                                   agreements=agreements.handlers
                                   )

        return stream.render('xhtml')


def get_localconf():
    """Return a file-like object which can be read to load the local instance 
    configuration."""

    return file(os.path.join( os.path.dirname(__file__), 'local.conf' ))

def serve():

    # load the local configuration
    cherrypy.config.update( get_localconf() )
    stats_conf = {'/stats':
                  {'tools.basic_auth.on' : True,
                   'tools.basic_auth.realm': 'localhost',
                   'tools.basic_auth.users': {'stats':
                                              md5.new('stats').hexdigest()}
                   },
                  }
        
    # mount the application
    app = cherrypy.tree.mount(ScholarsCopyright(), config=stats_conf)
    httpserver.serve(app, '127.0.0.1', '8003')

if __name__ == '__main__':
    serve()
