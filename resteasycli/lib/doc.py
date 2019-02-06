import re
import json
from docify import Document, components as c
from docify.formatters.html_bootstrap import HTMLBootstrap
from docify.formatters.markdown import Markdown

from resteasycli.exceptions import FileExtensionNotSupportedException


class APIDocument(object):
    '''Generate API documentation from workspace object'''

    FORMATS = {
        'md': Markdown,
        'html': HTMLBootstrap
    }

    def __init__(self, workspace, hide_cred=False):
        self.doc = self.create(workspace, hide_cred=hide_cred)

    @staticmethod
    def create(workspace, hide_cred=False):
        '''Create and return document object from workspace object'''

        doc = Document(c.H1(workspace.config.WORKSPACE_TITLE))
        if workspace.config.WORKSPACE_DESCRIPTION:
            doc.add(c.P(workspace.config.WORKSPACE_DESCRIPTION), c.Hr())
        else:
            doc.add(c.P(c.Nbsp()))

        for req_id in workspace.saved_requests:
            req = workspace.get_saved_request(req_id)
            api = req.endpoint.api
            headers = api.session.headers.copy()

            if hide_cred:
                if 'Authorization' in headers:
                    headers['Authorization'] = '*****'
                if 'Proxy-Authorization' in headers:
                    headers['Proxy-Authorization'] = '*****'

            lnk = re.sub('[^a-zA-Z0-9-]', '-', str(req_id))
            doc.add(c.Section(
                c.H2(
                    c.B(req.method), c.Nbsp(),
                    c.A(req_id, href='/#'+lnk), id=lnk),
                c.H3('Endpoint'),
                c.Pre(c.Code(api.endpoint)),
                c.H3('Headers'),
                c.Pre(c.Code('\n'.join(
                    ['{}: {}'.format(k, v) for k, v in headers.items()])))))

            if api.session.auth:
                if hide_cred:
                    username, password = ('*****', '*****')
                else:
                    username, password = api.session.auth

                doc.add(c.Section(
                    c.H3('Authentication'),
                    c.Section(
                        c.B('Username: ') + c.Nbsp() + c.Code(username),
                        c.Br(),
                        c.B('Password:') + c.Nbsp() + c.Code(password))))

            if req.method != 'GET':
                doc.add(c.Section(
                    c.H3('Body'),
                    c.Pre(c.Code(json.dumps(req.kwargs, indent=4)))))
            doc.add(c.P(c.Nbsp()))
        return doc

    def dump(self, filepath):
        '''Dump the document to given filename with proper format'''

        ext = filepath[::-1].split('.')[0][::-1].lower()
        if ext == filepath:
            ext = ''

        if ext not in self.FORMATS:
            raise FileExtensionNotSupportedException(
                'mention a file extension')

        with open(filepath, 'w') as f:
            f.write(str(self.FORMATS[ext](self.doc)))
