import yaml
from cliff.command import Command

from resteasycli.lib.request import Request


class GenericRequest(Command):
    '''The generic request class for all requests'''

    def get_parser(self, prog_name):
        '''Overriding parent method'''

        parser = super(GenericRequest, self).get_parser(prog_name)
        parser.add_argument(
            '-m', '--method',
            choices=self.app.workspace.config.ALL_METHODS,
            help='override query method',
        )
        parser.add_argument(
            '-k', '--kwargs',
            type=lambda x: dict(yaml.safe_load(x)),
            help='payload/params to send. format is yaml',
        )
        parser.add_argument(
            '-u', '--update_kwargs',
            type=lambda x: dict(yaml.safe_load(x)),
            help='add/update key-value pairs in kwargs. format is yaml',
        )
        parser.add_argument(
            '-a', '--auth',
            choices=self.app.workspace.auth.keys(),
            help='use alternate authentication from file',
            default=self.app.workspace.config.DEFAULT_AUTH_ID,
        )
        parser.add_argument(
            '-H', '--headers',
            choices=self.app.workspace.headers.keys(),
            help='use alternate set of headers from file',
            default=self.app.workspace.config.DEFAULT_HEADERS_ID,
        )
        parser.add_argument(
            '-t', '--timeout',
            type=int, help='request timeout in seconds',
            default=self.app.workspace.config.DEFAULT_TIMEOUT,
        )
        parser.add_argument(
            '-C', '--certfile',
            help='ssl certificate file path',
            default=self.app.workspace.config.DEFAULT_CERTFILE,
        )
        parser.add_argument(
            '-I', '--insecure',
            action='store_true',
            help=(
                'do not verify ssl certificate. '
                '(overrides "-C", "--certfile" option)'
            ),
        )
        parser.add_argument(
            '-F', '--fake',
            help='print the request instead of actually doing it',
            action='store_true',
        )
        parser.add_argument(
            '-s', '--save_as',
            help=(
                'save the request for later use.'
                ' can be used with --fake option'
            ),
        )
        return parser

    def get_request(self, method, site_id, endpoint_id, args):
        '''Get the request object'''

        # Check if endpoint extsts
        site = self.app.workspace.get_site(site_id)
        endpoint = site.get_endpoint(endpoint_id)

        req = Request(
            workspace=self.app.workspace, method=method,
            site_id=site.site_id, endpoint_id=endpoint.endpoint_id,
        )
        self.update_request(req, args)
        return req

    def update_request(self, request, args):
        '''Update the request object based on given args'''

        if args.method is not None:
            request.set_method(args.method)
        if args.timeout is not None:
            request.set_timeout(args.timeout)
        if args.kwargs is not None:
            request.set_kwargs(args.kwargs)
        if args.update_kwargs is not None:
            request.update_kwargs(args.update_kwargs)
        if args.auth is not None:
            request.set_auth(args.auth)
        if args.headers is not None:
            request.set_headers(args.headers)
        if args.certfile is not None:
            request.set_verify(args.certfile)
        if args.insecure:
            request.set_verify(False)
        if args.fake:
            request.set_debug(True)

    def get_response(self, request, args):
        '''Get the response object'''

        if args.save_as is not None:
            request.save_as(request_id=args.save_as)
        resp = request.do()
        if args.fake and 'session' in resp:
            del resp['session']
            resp = {'params': request.dict(), 'request': resp}
        return resp
