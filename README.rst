
RESTEasyCLI
===========

Handy REST API client on your terminal


.. image:: https://img.shields.io/pypi/v/RESTEasyCLI.svg
   :target: https://pypi.org/project/RESTEasyCLI
   :alt: PyPI version


.. image:: https://travis-ci.org/rapidstack/RESTEasyCLI.svg?branch=master
   :target: https://travis-ci.org/rapidstack/RESTEasyCLI
   :alt: Build Status



.. image:: https://asciinema.org/a/219065.svg
   :target: https://asciinema.org/a/219065
   :alt: asciicast



* `RESTEasyCLI <#resteasycli>`_

  * `Installation <#installation>`_
  * `Usage <#usage>`_

    * `Help menu <#help-menu>`_
    * `Initialize workspace <#initialize-workspace>`_
    * `Do CRUD requests <#do-crud-requests>`_
    * `Special formatting of data <#special-formatting-of-data>`_

      * `List <#list>`_
      * `Show <#show>`_

    * `Save a request for later use <#save-a-request-for-later-use>`_
    * `Do or redo a saved request <#do-or-redo-a-saved-request>`_
    * `Most importantly fake a request <#most-importantly-fake-a-request>`_

  * `TODO list <#todo-list>`_
  * `Contribution guide <#contribution-guide>`_

Installation
------------

.. code-block:: bash

   pip install resteasycli

   # OR

   pipenv install resteasycli

Usage
-----

Help menu
^^^^^^^^^

.. code-block:: bash

   recli help

Initialize workspace
^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   mkdir myworkspace
   cd myworkspace
   recli init
   # Few template files should be generated namely: auth.yml  headers.yml  saved.yml  sites.yml

Do CRUD requests
^^^^^^^^^^^^^^^^

.. code-block:: bash

   recli get testing/todos
   recli post testing/todos --kwargs title=abcd userId=10
   recli put testing/todos/1 --kwargs title=abcd
   recli patch testing/todo1 --kwargs title=xyz
   recli delete testing/todos/1

Special formatting of data
^^^^^^^^^^^^^^^^^^^^^^^^^^

List
~~~~

.. code-block:: bash

   recli list testing/todos

Show
~~~~

.. code-block:: bash

   recli show testing/todos/1

Save a request for later use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   recli get testing/todos/1 -s my_request

   # Request will be saved in saved.yml as "my_request"

Do or redo a saved request
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Without formatting
   recli do remind_shopping
   # Same as
   recli redo remind_shopping

   # With formatting
   recli dolst remind_shopping -m GET -k
   # Same as
   recli redo-list remind_shopping --method GET --kwargs

Most importantly fake a request
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   recli redo-show remind_shopping -m GET -k --fake

   # It can be used with -s to save the request for later use without doing it

   recli redo-show remind_shopping -m GET -k --fake -s get_todos

TODO list
---------


* [x] CRUD requests
* [x] Formatted outputs 
* [x] Save requests feature
* [x] Refactored sites, headers, authentication methods, saved requests
* [ ] Design a icon for it and it's dependency `RESTEasy <https://github.com/rapidstack/RESTEasy>`_
* [ ] Add full usage documentation with examples
* [ ] Add smart auto completions
* [ ] Fix interactive mode
* [ ] Code coverage > 90%
* [ ] Release version 1
* [ ] Test cases with different environment variables
* [ ] API server for full end to end test with custom headers, authentication
* [ ] Add more authentication methods
* [ ] Add proxy support
* [ ] Token detection for automatic authentication headers update
* [ ] Generate and publish API documentation feature
* [ ] Initialize workspace from generated API documentation
* [ ] Write a blog post, create a youtube video on it
* [ ] `Postman <https://www.getpostman.com>`_ compatibility

...[add more goals](https://github.com/rapidstack/RESTEasyCLI/issues/new)


Contribution guide
------------------

This is a new born project and has lots of scope for improvements.

If you feel that you can help with any of above TODO list or if you have a totally unique idea, feel free to jump right in.

Here are some tips to get started with contributing to this project right away.


* Instead of directly creating pull requests, `create a issue <https://github.com/rapidstack/RESTEasyCLI/issues/new>`_ first to check it's relevence and save efforts. However,
* If you find a bug, feel free to directly create pull requests by forking master branch
* Awesome if commit messages and pull request description are clear and concise
* One of it's depedency `RESTEasy <https://github.com/rapidstack/RESTEasy>`_ has a gitter channel for any doubt or discussion related to this project or `RESTEasy <https://github.com/rapidstack/RESTEasy>`_
