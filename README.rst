
RESTEasyCLI
===========

Handy REST API client on your terminal


.. image:: https://img.shields.io/pypi/v/RESTEasyCLI.svg
   :target: https://pypi.org/project/RESTEasyCLI
   :alt: PyPI version


.. image:: https://travis-ci.org/rapidstack/RESTEasyCLI.svg?branch=master
   :target: https://travis-ci.org/rapidstack/RESTEasyCLI
   :alt: Build Status



.. image:: https://asciinema.org/a/219207.svg
   :target: https://asciinema.org/a/219207
   :alt: asciicast



* `RESTEasyCLI <#resteasycli>`_

  * `Get started with an interactive demo <#get-started-with-an-interactive-demo>`_
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

Get started with an interactive demo
------------------------------------

NOTE: This demo requires supported version of python and ``virtualenv`` to be installed

.. code-block:: bash

   curl -L https://raw.githubusercontent.com/rapidstack/RESTEasyCLI/master/tools/demo.sh -o demo.sh
   chmod +x demo.sh
   ./demo.sh

Installation
------------

.. code-block:: bash

   # Install it globally
   sudo pip install -U resteasycli

   # OR

   # Install it locally
   pip install -U --user resteasycli

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

   recli get testing/t
   recli post testing/t --kwargs title=abcd userId=10
   recli put testing/t/1 --kwargs title=abcd
   recli patch testing/t1 --kwargs title=xyz
   recli delete testing/t/1

Special formatting of data
^^^^^^^^^^^^^^^^^^^^^^^^^^

List
~~~~

.. code-block:: bash

   recli list testing/t

Show
~~~~

.. code-block:: bash

   recli show testing/t/1

Save a request for later use
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   recli get testing/t/1 -s my_request

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

`Check the great TODO list on project board <https://github.com/rapidstack/RESTEasyCLI/projects>`_

Contribution guide
------------------

This is a new born project and has lots of scope for improvements.

If you feel that you can help with any of above TODO list or if you have a totally unique idea, feel free to jump right in.

Here are some tips to start contributing to this project right away.


* Instead of directly creating pull requests, `create a issue <https://github.com/rapidstack/RESTEasyCLI/issues/new>`_ first to check it's relevence and save efforts. However,
* If you find a bug, feel free to directly create pull requests by forking master branch
* Awesome if commit messages and pull request description are clear and concise
* One of it's depedency `RESTEasy <https://github.com/rapidstack/RESTEasy>`_ has `a gitter channel <https://gitter.im/rapidstack/RESTEasy>`_ for any doubt or discussion related to this project or `RESTEasy <https://github.com/rapidstack/RESTEasy>`_
* Use `pipenv <https://github.com/pypa/pipenv>`_ to install/update dependencies
* Do not modify ``README.rst`` file. It's auto generated using `m2r <https://github.com/miyakogi/m2r>`_ (Installed as a dev dependency). While updating ``README.md`` file, use `plugin for auto TOC update <https://github.com/ekalinin/github-markdown-toc>`_.
* Run ``./tools/before_push.sh`` before pushing. It will take care of house keeping stuffs like generating ``README.rst``\ , checking if VERSOIN info is updated correctly in all files etc.
