import sys
import json
import yaml
from cliff.show import ShowOne
from cliff.lister import Lister
from cliff.command import Command

from resteasycli.lib.request import Request
from resteasycli.cmd.common import SiteEndpoint
from resteasycli.cmd.generic_request import GenericRequest
from resteasycli.cmd.request_factory import RequestFactory
from resteasycli.exceptions import InvalidCommandException


class UnSavedRequest(GenericRequest):
    '''Parent for all unsaved requests for API requests'''

    def get_parser(self, prog_name):
        '''Overriding parent method'''

        parser = super(UnSavedRequest, self).get_parser(prog_name)
        choices = []
        ds = self.workspace.config.DEFAULT_SITE_ID
        dep = self.workspace.config.DEFAULT_ENDPOINT_ID

        if ds in self.workspace.sites:
            if dep in self.workspace.sites[ds]['endpoints']:
                choices.append(SiteEndpoint('/'))
            choices += list(map(
                lambda x: SiteEndpoint('/'+x),
                self.workspace.sites[ds]['endpoints'].keys()))

        for s, v in self.workspace.sites.items():
            if dep in v['endpoints']:
                choices.append(SiteEndpoint(s+'/'))
            for e in v['endpoints'].keys():
                choices.append(SiteEndpoint('{}/{}'.format(s, e)))

        parser.add_argument(
            'target',
            type=SiteEndpoint, choices=choices,
            help='format: $site_id/$endpoint_id or $site_id/$endpoint_id/$slug')
        return parser

    def get_request(self, method, args):
        '''Overriding parent method'''

        site_id, endpoint_id, slug = args.target.site_id, args.target.endpoint_id, args.target.slug

        if not site_id:
            if self.workspace.config.DEFAULT_SITE_ID:
                site_id = self.workspace.config.DEFAULT_SITE_ID
            else:
                raise InvalidCommandException('default site ID is not defined')

        if not endpoint_id:
            if self.workspace.config.DEFAULT_ENDPOINT_ID:
                endpoint_id = self.workspace.config.DEFAULT_ENDPOINT_ID
            else:
                raise InvalidCommandException('default endpoint ID is not defined')

        req = super(UnSavedRequest, self).get_request(
                method=method, site_id=site_id,
                endpoint_id=endpoint_id, args=args)

        if slug is not None:
            req.add_slug(slug)
        return req


class SavedRequest(GenericRequest):
    '''Generic saved request API'''

    def get_parser(self, prog_name):
        parser = super(SavedRequest, self).get_parser(prog_name)
        parser.add_argument(
            'request_id',
            choices=self.workspace.saved_requests.keys(),
            help='request ID from saved requests')
        parser.add_argument(
            '-S', '--slug',
            help='add slug at the end of the URL')
        return parser

    def update_request(self, request, args):
        '''Override parent class'''
        super(SavedRequest, self).update_request(request, args)
        if args.slug is not None:
            request.add_slug(args.slug)

    def get_request(self, method, args):
        '''Builds and returns the request object'''

        req = self.workspace.get_saved_request(args.request_id)
        if method is not None:
            req.set_method(method)
        self.update_request(req, args)
        return req


class GET(RequestFactory.unformatted(UnSavedRequest)):
    '''Do GET request'''

    def take_action(self, args):
        '''Override parent method'''
        super(GET, self).act(method='GET', args=args)


class POST(RequestFactory.unformatted(UnSavedRequest)):
    '''Do POST request'''

    def take_action(self, args):
        super(POST, self).act(method='POST', args=args)


class PUT(RequestFactory.unformatted(UnSavedRequest)):
    '''Do PUT request'''

    def take_action(self, args):
        super(PUT, self).act(method='PUT', args=args)


class PATCH(RequestFactory.unformatted(UnSavedRequest)):
    '''Do PATCH request'''

    def take_action(self, args):
        super(PATCH, self).act(method='PATCH', args=args)


class DELETE(RequestFactory.unformatted(UnSavedRequest)):
    '''Do DELETE request'''

    def take_action(self, args):
        super(DELETE, self).act(method='DELETE', args=args)


class UnSavedList(RequestFactory.listformatted(UnSavedRequest)):
    '''Fetch a list of resources'''

    def take_action(self, args):
        return super(UnSavedList, self).act(method='GET', args=args)


class UnSavedShow(RequestFactory.showoneformatted(UnSavedRequest)):
    '''Show a particular resource'''

    def take_action(self, args):
        return super(UnSavedShow, self).act(method='GET', args=args)


class SavedRedo(RequestFactory.unformatted(SavedRequest)):
    '''Re-do a saved request'''

    def take_action(self, args):
        super(SavedRedo, self).act(method=None, args=args)


class SavedList(RequestFactory.listformatted(SavedRequest)):
    '''Re-do a saved request with list format'''

    def take_action(self, args):
        return super(SavedList, self).act(method='GET', args=args)


class SavedShow(RequestFactory.showoneformatted(SavedRequest)):
    '''Re-do a saved request with show one format'''

    def take_action(self, args):
        return super(SavedShow, self).act(method='GET', args=args)
