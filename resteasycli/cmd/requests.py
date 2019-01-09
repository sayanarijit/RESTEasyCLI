import sys
import json
import yaml
from cliff.show import ShowOne
from cliff.lister import Lister
from cliff.command import Command

from resteasycli.objects import workspace
from resteasycli.lib.request import Request
from resteasycli.cmd.generic_request import GenericRequest
from resteasycli.cmd.request_factory import RequestFactory
from resteasycli.exceptions import InvalidCommandException


class UnSavedRequest(GenericRequest):
    '''Parent for all unsaved requests for API requests'''

    def get_parser(self, prog_name):
        '''Overriding parent method'''

        parser = super(UnSavedRequest, self).get_parser(prog_name)
        choices = []
        ds = workspace.config.DEFAULT_SITE_ID
        dep = workspace.config.DEFAULT_ENDPOINT_ID

        if ds in workspace.sites:
            if dep in workspace.sites[ds]['endpoints']:
                choices.append('/')
            choices += list(map(lambda x: '/'+x, workspace.sites[ds]['endpoints'].keys()))
        
        for s, v in workspace.sites.items():
            if dep in v['endpoints']:
                choices.append('{}/'.format(s))
            for e in v['endpoints'].keys():
                choices.append('{}/{}'.format(s,e))
        
        parser.add_argument(
            'site_endpoint',
            choices=choices, help='format: $site_id/$endpoint_id or $site_id/$endpoint_id')
        return parser

    def get_request(self, method, args):
        '''Overriding parent method'''

        if len(args.site_endpoint.split('/')) == 2:
            site_id, endpoint_id = args.site_endpoint.split('/')
        else:
            raise InvalidCommandException(
                ('{}: correct format is: $site_id/$endpoint_id').format(args.site_endpoint))

        if not site_id:
            if workspace.config.DEFAULT_SITE_ID:
                site_id = workspace.config.DEFAULT_SITE_ID
            else:
                raise InvalidCommandException('default site ID is not defined')

        if not endpoint_id:
            if workspace.config.DEFAULT_ENDPOINT_ID:
                endpoint_id = workspace.config.DEFAULT_ENDPOINT_ID
            else:
                raise InvalidCommandException('default endpoint ID is not defined')

        return super(UnSavedRequest, self).get_request(
                method=method, site_id=site_id,
                endpoint_id=endpoint_id, args=args)


class SavedRequest(GenericRequest):
    '''Generic saved request API'''

    def get_parser(self, prog_name):
        parser = super(SavedRequest, self).get_parser(prog_name)
        parser.add_argument(
            'request_id',
            choices=workspace.saved_requests.keys(),
            help='request ID from saved requests')
        return parser

    def get_request(self, args):
        '''Builds and returns the request object'''
        
        req = workspace.get_saved_request(args.request_id)
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


class UnSavedShow(RequestFactory.listformatted(UnSavedRequest)):
    '''Show a particular resource'''

    def take_action(self, args):
        return super(UnSavedShow, self).act(method='GET', args=args)


class SavedRedo(RequestFactory.unformatted(SavedRequest)):
    '''Re-do a saved request'''

    def take_action(self, args):
        req = self.get_request(args)
        super(SavedRedo, self).act(method=req.method, args=args)


class SavedList(RequestFactory.listformatted(SavedRequest)):
    '''Re-do a saved request with list format'''

    def take_action(self, args):
        super(SavedList, self).act(method='GET', args=args)


class SavedShow(RequestFactory.showoneformatted(SavedRequest)):
    '''Re-do a saved request with show one format'''

    def take_action(self, args):
        super(SavedShow, self).act(method='GET', args=args)
