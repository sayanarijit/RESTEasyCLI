import logging

from resteasycli.lib.workspace import Workspace


logger = logging.getLogger('test_logger')
workspace = Workspace(logger=logger)
