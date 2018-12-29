# RESTEasyCLI

Handy REST API client on your terminal

[![PyPI version](https://img.shields.io/pypi/v/RESTEasyCLI.svg)](https://pypi.org/project/RESTEasyCLI)
[![Build Status](https://travis-ci.org/rapidstack/RESTEasyCLI.svg?branch=master)](https://travis-ci.org/rapidstack/RESTEasyCLI)

- [RESTEasyCLI](#resteasycli)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Help menu](#help-menu)
    - [Initialize workspace](#initialize-workspace)
    - [Do CRUD requests](#do-crud-requests)
    - [Special formatting of data](#special-formatting-of-data)
      - [List](#list)
      - [Show](#show)

## Installation

```bash
pip install RESTEasyCLI

# OR

pipenv install RESTEasyCLI
```

## Usage

### Help menu
```bash
recli help
```

```bash
usage: recli [--version] [-v | -q] [--log-file LOG_FILE] [-h] [--debug]

Handy REST API client on your terminal

optional arguments:
  --version            show program's version number and exit
  -v, --verbose        Increase verbosity of output. Can be repeated.
  -q, --quiet          Suppress output except warnings and errors.
  --log-file LOG_FILE  Specify a file to log output. Disabled by default.
  -h, --help           Show help message and exit.
  --debug              Show tracebacks on errors.

Commands:
  complete       print bash completion command (cliff)
  delete         Do DELETE request
  get            Do GET request
  help           print detailed help for another command (cliff)
  init           Initialize template files in current directory
  list           Fetch a list of results
  patch          Do PATCH request
  post           Do POST request
  put            Do PUT request
  show           SHOW a particular result
```

### Initialize workspace
```bash
mkdir myworkspace
cd myworkspace
recli init

# A template file is generated
cat sites.yml
```

```yaml
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
```

### Do CRUD requests

```bash
recli get testing/todos
recli post testing/todos --kwargs title=abcd userId=10
recli put testing/todos/1 --kwargs title=abcd
recli patch testing/todo1 --kwargs title=xyz
recli delete testing/todos/1
```

### Special formatting of data

#### List

```bash
recli help list
```

```bash
usage: recli list [-h] [-f {csv,json,table,value,yaml}] [-c COLUMN]
                  [--quote {all,minimal,none,nonnumeric}]
                  [--max-width <integer>] [--fit-width] [--print-empty]
                  [--noindent] [--sort-column SORT_COLUMN]
                  [-k [KWARGS [KWARGS ...]]] [-t TIMEOUT]
                  endpoint

Fetch a list of results

positional arguments:
  endpoint

optional arguments:
  -h, --help            show this help message and exit
  -k [KWARGS [KWARGS ...]], --kwargs [KWARGS [KWARGS ...]]
  -t TIMEOUT, --timeout TIMEOUT

output formatters:
  output formatter options

  -f {csv,json,table,value,yaml}, --format {csv,json,table,value,yaml}
                        the output format, defaults to table
  -c COLUMN, --column COLUMN
                        specify the column(s) to include, can be repeated
  --sort-column SORT_COLUMN
                        specify the column(s) to sort the data (columns
                        specified first have a priority, non-existing columns
                        are ignored), can be repeated

CSV Formatter:
  --quote {all,minimal,none,nonnumeric}
                        when to include quotes, defaults to nonnumeric

table formatter:
  --max-width <integer>
                        Maximum display width, <1 to disable. You can also use
                        the CLIFF_MAX_TERM_WIDTH environment variable, but the
                        parameter takes precedence.
  --fit-width           Fit the table to the display width. Implied if --max-
                        width greater than 0. Set the environment variable
                        CLIFF_FIT_WIDTH=1 to always enable
  --print-empty         Print empty table if there is no data to show.

json formatter:
  --noindent            whether to disable indenting the JSON
```

#### Show

```bash
recli help show
```

```bash
usage: recli show [-h] [-f {json,shell,table,value,yaml}] [-c COLUMN]
                  [--max-width <integer>] [--fit-width] [--print-empty]
                  [--prefix PREFIX] [--noindent] [-k [KWARGS [KWARGS ...]]]
                  [-t TIMEOUT]
                  endpoint

SHOW a particular result

positional arguments:
  endpoint

optional arguments:
  -h, --help            show this help message and exit
  -k [KWARGS [KWARGS ...]], --kwargs [KWARGS [KWARGS ...]]
  -t TIMEOUT, --timeout TIMEOUT

output formatters:
  output formatter options

  -f {json,shell,table,value,yaml}, --format {json,shell,table,value,yaml}
                        the output format, defaults to table
  -c COLUMN, --column COLUMN
                        specify the column(s) to include, can be repeated

table formatter:
  --max-width <integer>
                        Maximum display width, <1 to disable. You can also use
                        the CLIFF_MAX_TERM_WIDTH environment variable, but the
                        parameter takes precedence.
  --fit-width           Fit the table to the display width. Implied if --max-
                        width greater than 0. Set the environment variable
                        CLIFF_FIT_WIDTH=1 to always enable
  --print-empty         Print empty table if there is no data to show.

shell formatter:
  a format a UNIX shell can parse (variable="value")

  --prefix PREFIX       add a prefix to all variable names

json formatter:
  --noindent            whether to disable indenting the JSON
```