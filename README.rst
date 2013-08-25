Django Octocat
==============

A Django app for handling github users and repos.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-octocat

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/Celc/django-octocat.git#egg=github

Add ``github`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'github',
    )

Add the ``github`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^github/', include('github.urls', namespace='github')),
    )

Add ``github.middlewares.GithubAuthorizationMiddleware`` to your
``MIDDLEWARE_CLASSES``

.. code-block:: python

    MIDDLEWARE_CLASSES = (
        ...
        'github.middlewares.GithubAuthorizationMiddleware',
    )

Add ``github.backends.GithubBackend`` to your ``AUTHENTICATION_BACKENDS``

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        ...
        'github.backends.GithubBackend',
    )

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate github

If you are planning on cloning the repos set the target directory

.. code-block:: python

    import tempfile
    GITHUB_ROOT = tempfile.gettempdir()


Finally add the Github settings under ``/admin``.

Usage
-----

To authenticate users send them to `{% url 'github:authorize' pk=1 %}` where
pk is the id of the Github app.

Contribute
----------

.. code-block:: bash

    mkvirtualenv django-octocat
    make develop

Add code, write test, send pull request.
