from resteasycli.lib.request import Request

class SavedRequest(Request):
    '''Saved requests for reuse and lazyness'''

    def __init__(self, request_id, workspace):
        data = workspace.saved_requests[request_id]
        Request.__init__(self, workspace=workspace, site_id=data['site'],
                endpoint_id=data['endpoint'], **data)
        self.request_id = request_id

