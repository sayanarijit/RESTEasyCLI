# User Guide

## Quick start

For getting started as quickly as possible i.e. to get introduced to the most useful features it provides, we recommend you to try the interactive demo mentioned in the Introduction page.

## Initialize workspace

A workspace a directory is where you keep a group of files that contains information about your API queries such as API endpoints, request parameters, headers & authentication methods, configuration files etc.

The default format of these files is [YAML](https://en.wikipedia.org/wiki/YAML) for better readability. However [JSON](https://en.wikipedia.org/wiki/JSON) is also supported.

To initialize a workspace, create an empty directory and execute below command

### To initialize workspace with default YAML files

```bash
recli init
```

### To initialize workspace with JSON files

```bash
recli init -e json
```

NOTE: Normally it will skip a file it already exists. However, you may use `-f` or `--force` option to overwrite **all** the files.

## Workspace concept

### How does it work

When you initialize an workspace, you may notice a set of files are auto generated. These are just basic templates to help you understand the format. There should be atmost one file for each category of information.

For example, there should be one file that contains information about all the sites along with endpoints of each site, one file to contain set of request headers, one file to store the authentication methods and credentials, one file to save information about frequently made requests i.e. combination of payloads, parameters, headers and authentication methods used etc.

### Why have them

Simply to stay origanised. Having separate directories considered as workapaces enables us to categorize API sites, endpoints, headers, authentication methods etc into several groups. Whan we need to define something globally, we can always define in `~/.recli/` or even `/etc/recli`. This way we can have better control on our API requests.