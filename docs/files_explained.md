# Workspace Files Explained

All the files that may reside in a workspace or `~/.recli` or `/etc/recli` are metioned below.

## 1. Configuration file

This file has a fixed name `recli.cfg` and may reside in either current workspace, or `./recli`, or `/etc/recli`. *recli* will search for this file in specified order and read whatever comes first.

All the variable parameters of configuration used by *recli* such as default file extension, lookup path etc. may be defined in this file.

This file has it's own fixed format and a fixed search path as it is the first file *recli* reads when a command is invoked.

This file looks like this:

```ini
### Configuration file for RESTEasyCLI
### Values mentioned here are default values
### Uncomment lines and edit values as required

### Request methods to allow
DEFAULT_ALLOWED_METHODS = GET, POST, PUT, PATCH, DELETE

### Where to search for workspace files (priority highest -> lowest)
SEARCH_PATHS = ., ~/.recli, /etc/recli

### Which file format to use for initializing workspace files
DEFAULT_FILE_FORMAT = v1.0

### With file extension to use for initializing workspace files
DEFAULT_FILE_EXTENSION = yml

### Name of the sites template file
SITES_TEMPLATE_FILENAME = sites

### Name of the auth template file
AUTH_TEMPLATE_FILENAME = auth

### Name of the headers template file
HEADERS_TEMPLATE_FILENAME = headers

### Name of the saved requests template file
SAVED_REQUESTS_TEMPLATE_FILENAME = saved

### Title for current workspace
WORKSPACE_TITLE = myworkspace

### Description for current workspace
WORKSPACE_DESCRIPTION =
```

As shown above, this is a flat file with key-value pairs separated with `=`. Any of the characters `#` or `;` can be used to put comments.

***NOTE: Do not use single or double quotes to define values and use `#` or `;` only at the starting of a line***


## 2. Sites file

This file holds information about different sites, endpoints exposed by each site, default authentication used, default headers used etc. This file in YAML format will look like this:

### Minimal parameters

```yaml
version: v1.0
sites:
  $site_id:
    base_url: $base_url
    endpoints:
      $endpoint_id:
        route: $endpoint_path
```

### All available options

```yaml
version: v1.0
sites:
  $site_id:
    base_url: $base_url
    headers: $headers_id
    auth: $auth_id
    verify: $verify
    timeout: $timeout
    methods:
    - $allowed_method1
    - $allowed_method2
    endpoints:
      $endpoint_id:
        route: $endpoint_path
        headers: $headers_id
        auth: $auth_id
        verify: $verify
        timeout: $timeout
        methods:
        - $allowed_method1
        - $allowed_method2
```

Both versions of sites file defines an endpoint $base_url/$endpoint_path. One with minimal parameters, another with all available options.

All the undefined fields will inherit values from parent if available or take default values.

Name of this file can be changed by modifying `SITES_TEMPLATE_FILENAME` field in configuration file.


## 3. Headers file

This file holds key-value pairs to be sent as request headers.

Two actions are supported: `only` and `update`. `only` will remove previously applied headers by parents and apply new set of key-value pairs. `update` only adds new key-value pairs or updates existing ones without removing any. This file in YAML format will look like this:

```yaml
version: v1.0
headers:
  $header_id:
    action: $action
    values:
      $key1: $value1
      $key2: $value2
```

Name of this file can be changed by modifying `HEADERS_TEMPLATE_FILENAME` field in configuration file.


## 4. Auth file

This file stored authentication methods. Key-value pairs may vary based on authentication type. This file in YAML format will look like this:

### Basic auth

```yaml
version: v1.0
auth:
  $auth_id:
    type: basic
    credentials:
      username: $username
      password: $password
```

### Token auth

```yaml
version: v1.0
auth:
  $auth_id:
    type: token
    credentials:
      header: $key
      value: $value
```

Name of this file can be changed by modifying `AUTH_TEMPLATE_FILENAME` field in configuration file.


## 5. Saved requests file

This file stored information of all the requests saved for re-use purpose. Along with manual updates, this file also gets updated automatically by *recli* when we use `-s` or `--save` option to save a request. This file in YAML format looks like this:

### Minimal parameters

```yaml
version: v1.0
saved_requests:
  $request_id:
    method: $method
    site: $site_id
    endpoint: $endpoint_id
```

### All available options

```yaml
version: v1.0
saved_requests:
  $request_id:
    method: $method
    site: $site_id
    endpoint: $endpoint_id
    slug: $slug
    headers: $headers_id
    auth: $auth_id
    verify: $verify
    timeout: $timeout
    kwargs:
      $key1: $value1
      $key2: $value2
```

A requests inherits undefined values from it's endpoint which already inherited it's undefined values from it's site.

Name of this file can be changed by modifying `SAVED_REQUESTS_TEMPLATE_FILENAME` field in configuration file.


***NOTE: All workspace files except the configuration file contain a version information to allow extension of currently defined format tackling incompatibility***
