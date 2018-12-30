# RESTEasyCLI

Handy REST API client on your terminal

[![PyPI version](https://img.shields.io/pypi/v/RESTEasyCLI.svg)](https://pypi.org/project/RESTEasyCLI)
[![Build Status](https://travis-ci.org/rapidstack/RESTEasyCLI.svg?branch=master)](https://travis-ci.org/rapidstack/RESTEasyCLI)

[![asciicast](https://asciinema.org/a/219065.svg)](https://asciinema.org/a/219065)

- [RESTEasyCLI](#resteasycli)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Help menu](#help-menu)
    - [Initialize workspace](#initialize-workspace)
    - [Do CRUD requests](#do-crud-requests)
    - [Special formatting of data](#special-formatting-of-data)
      - [List](#list)
      - [Show](#show)
    - [Re-do a saved request](#re-do-a-saved-request)
    - [Most importantly fake a retuest](#most-importantly-fake-a-retuest)
  - [External packages used](#external-packages-used)

## Installation

```bash
pip install resteasycli

# OR

pipenv install resteasycli
```

## Usage

### Help menu
```bash
recli help
```

### Initialize workspace
```bash
mkdir myworkspace
cd myworkspace
recli init
# Few template files should be generated namely: auth.yml  headers.yml  saved.yml  sites.yml
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
recli list testing/todos
```

#### Show

```bash
recli show testing/todos
```

### Re-do a saved request

```bash
recli redo remind_shopping
recli redo-list remind_shopping -m GET -k
```

### Most importantly fake a retuest

```bash
recli redo-show remind_shopping -m GET -k --fake
```

## External packages used

- [cliff](https://github.com/openstack/cliff)
- [RESTEasy](https://github.com/rapidstack/RESTEasy)
  - [requests](https://github.com/requests/requests)
