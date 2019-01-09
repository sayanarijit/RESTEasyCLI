# User Guide

## Quick start

To get started as quickly as possible i.e. to get introduced to the most useful features it provides, we recommend you to try the interactive demo mentioned in the Introduction page.

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

***NOTE: Normally it will skip a file if it already exists. However, you may use `-f` or `--force` option to overwrite all the files.***

## Workspace concept

### How does it work

When you initialize an workspace, you may notice a set of files are auto generated. These are just basic templates to help you understand the format. There should be atmost one file for each category of information.

For example, there should be one file that contains information about all the sites along with endpoints of each site, one file to contain set of request headers, one file to store the authentication methods and credentials, one file to save information about frequently made requests i.e. combination of payloads, parameters, headers and authentication methods used, one configuration file etc.

### Why have workspaces

Simply to stay origanised. Having separate directories considered as workapaces enables us to categorize API sites, endpoints, headers, authentication methods etc into several groups. When we need to define something globally, we can always define in `~/.recli/` or even `/etc/recli`.

By default contents defined in current workspace will override `~/.recli`'s and contents defined in `~/.recli` will override `/etc/recli`'s. This priority based lookup path is also editable as the paths can be defined in `recli.cfg` file.

As we will eventually find out, this way of organising files will allow us to have better control on our API requests.


## Commands

### Help menu

To get the full list of available sub-commands enter any of the following commands:

```bash
recli help

# OR

recli -h

# OR

recli --help
```

### Help menu of a sub-command

To get the help menu of a sub-command enter any of the following commands

```bash
# Assuming "do" is the sub-command

recli help do

# OR

recli do -h

# OR

recli do --help
```

### Interactive mode

*recli* also supports interactive mode for more convenience. To get into the interactive mode, just enter:

```bash
recli
```

When in interactive mode, you don't need to type `recli` anymore. You can just enter the remaining parts of the command.
For example: `recli help` becomes `help`, `recli init` becomes `init`. There are some additional cool features that you can explore with `help` command.

For further information on interactive mode, please read [cliff documentation](https://docs.openstack.org/cliff/latest/user/interactive_mode.html).

### Workspace management commands

*recli* has a set of workspace management commands such as:

```bash
# List available sites
recli list-sites

# Show details of a particular site (e.g. ghjobs)
recli show-site ghjobs

# List available endpoints
recli list-endpoints

# Show details of an endpoint (e.g. ghjobs/p)
recli show-endpoint ghjobs/p

# Similarly

# List and show authentication method(s)
recli list-auth
recli show-auth $auth_id

# List and show headers
recli list-headers
recli show-headers $headers_id

# List and show saved requests
recli list-saved
recli show-saved $request_id
```

All these commands can be invoked with additional parameters such as `-f json` to display the output as JSON formatted text.


### Doing CRUD requests

*recli* supports full CRUD operation.

```bash
# GET request
recli get $site_id/$endpoint_id

# POST request
recli post $site_id/$endpoint_id -k "{$key1: $value1, $key2: $value2}"

# PUT request
recli put $site_id/$endpoint_id/1 -k "$key: $value"

# PATCH request
recli patch $site_id/$endpoint_id/1 -k "$key: $value"

# DELETE request
recli delete $site_id/$endpoint_id/1
```

***NOTE:*** *Although `$site_id/$endpoint_id/1` is not defined in any file, it will take "1" as a slug and format the URL accordingly*


### Formatting the output

To format the output of any CRUD request, use `-f` or `--format` option

```bash
recli get $site_id/$endpoint_id -f json

# Same as

recli get $site_id/$endpoint_id --format json
```

### Faking a request

Any API request can be faked using `-F` or `--fake` option. When faked, *recli* will print the information about that request instead of doing it.


### Saving a request

Requests can be saved with an ID using the `-s` or `--save_as` option with an ID.

If the ID already exists, *recli* will update the information overriding previous values.

This feature is best used with `-F` i.e. `--fake` option to save a request for later use without doing it.


### Invoking a saved request

Saved requests can be invoked any number of times using the `do` sub-command.

```bash
recli do $request_id
```

Saved requests can also be invoked with updated parameters by overriding the saved parameters using command-line arguments.

```bash
recli do $request_id -k "$key: $value" -a $updated_auth_id -H $updated_header_id
```

And it can be faked and saved by adding `-F -s $updated_request_id` arguments.

***NOTE:*** *`redo` is an alias to `do` command*


### Table formatted outputs

Response of GET requests can be displayed in table format by using below commands:

```bash
# Unsaved requests
recli list $site_id/$endpoint_id
recli show $site_id/$endpoint_id/1

# Saved requests
recli dolst $request_id
recli doshw $request_id -S 1
# Same as
recli redo-list $request_id
recli redo-show $request_id -S 1
```

This output can be further formatted to any supported representation using the `-f` or `--format` option.

***NOTE:*** *You can also use this feature for other CRUD operations by overriding the method using `-m` or `--method` option but doing so is not recommended as result's structure may vary and formatting may fail*


## Defining default command-line arguments

We can define frequently used command-line arguments such as site ID, endpoint ID, headers ID, auth ID etc in `recli.cfg` file. When defined in this file, these defaults will override all the other values as these will be passed as command-line arguments which has the highest priority.

For example, if we define `DEFAULT_SITE_ID = testing` and `DEFAULT_ENDPOINT_ID = t`, we can use below commands:

```bash
recli get /
# Same as: recli get testing/t

recli get //1
# Same as: recli get testing/t/1

recli get /another_endpoint
# Same as: recli get testing/another_endpoint

recli get /another_endpoint/1
# Same as: recli get testing/another_endpoint/1

recli get another_site/
# Same as: recli get another_site/t

recli get another_site//1
# Same as: recli get another_site/t/1
```
