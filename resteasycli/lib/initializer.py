import os

from resteasycli.config import Config
from resteasycli.logger import logger


SITES_TEMPLATE_CONTENT = '''\
description: My favourite sites
sites:    
  github_jobs:
    base_url: https://jobs.github.com
    endpoints:
      positions:
        route: positions.json
        timeout: 10
        methods:
          - GET
  testing:
    base_url: https://jsonplaceholder.typicode.com
    endpoints:
      todos:
        route: todos
      todo1:
        route: todos/1
'''

def initialize(force=False):
    if os.path.exists(Config.SITE_TEMPLATE_FILENAME) and not force:
          logger.debug('file exists: ' + Config.SITE_TEMPLATE_FILENAME)
          return
    with open(Config.SITE_TEMPLATE_FILENAME, 'w') as f:
        f.write(SITES_TEMPLATE_CONTENT)
    logger.debug('file written: ' + Config.SITE_TEMPLATE_FILENAME)
