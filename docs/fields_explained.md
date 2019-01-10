# Fields Explained

Here you can find explaination of all the fields used in workspace files.

## ID fields

These fields can be anything that you can define or have defined in any file in your workspace except the configuration file. The value serves as identifier of workspace objects such as a site, an endpoint, an authentication method, a set of headers etc. It is recommended to keep the value as consise as possible without making it difficult to memorize. For e.g. the ID for the site *GitHub Jobs* can be defined as `ghjobs`.

Field            | Value
-----------------|--------------------
$site_id         | Value of this field is defined in *sites* file. You can find the available site IDs by executing `recli list-sites` command.
$endpoint_id     | Value of this field is defined in *sites* file. You can find the available site IDs by executing `recli list-endpoints` command.
$site_endpoint   | This is the conbination of `$site_id/$endpoint_id`. Available combinations can be listed by executing `recli list-endpoints` command
$headers_id      | Value of this field is defined in *headers* file. You can find the available site IDs by executing `recli list-headers` command.
$auth_id         | Value of this field is defined in *auth* file. You can find the available site IDs by executing `recli list-auth` command.
$request_id      | Value of this field is defined in *saved requests* file. You can find the available site IDs by executing `recli list-saved` command.

## Common fields

These fields are common for *sites*, *endpoints* and *saved requests*.

Field            | Value
-----------------|--------------------
verify           | How to verify ssl. It accepts either `False` or a valid certificate file path as argument. Default value is `False`
timeout          | How long to wait for a response before raising timeout error. Default is `None`.

## Fields specific to sites file

Field            | Value
-----------------|--------------------
base_url         | Base URL of a site such as `https://api.chucknorris.io`, `https://jsonplaceholder.typicode.com`, `https://jobs.github.com` etc.
methods          | Request methods allowed for a specific site or an endpoint. Default value is defined in `recli.cfg` file as `DEFAULT_ALLOWED_METHODS`

## Fields specific to headers file

Field            | Value
-----------------|--------------------
action           | Whether to update key-value pairs on top of existing headers or apply only given headers. It accepts `update` or `only` as value.
values           | Key-value pairs to apply as header. Example: `Content-Type: application/json`

## Fields specific to auth file

Field            | Value
-----------------|--------------------
type             | Type of authentication such as `basic` for basic auth, `token` for token auth.
credentials      | Based of the authentication type, credentials can be defined here.

## Fields specific to saved requests file

Field            | Value
-----------------|--------------------
method           | Request method to perform such as `GET`, `POST` etc. Given value must be allowed in *sites* file.
slug             | Path to append after the endpoint URL. It can be a single character such as `1` or a word such as `tasks` or a path such as `tasks/1`.
kwargs           | In case of GET requests, it is the key-value pairs to be sent as URL parameters. In case of other requests, it is the key-value pairs of the payload to be sent. In latter case, value will be automatically encoded as JSON string before it is sent.
