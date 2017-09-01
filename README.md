Global Humanitarians Unite
==========================

This is the Global Humanitarians Unite website prototype.

Environment Setup
-----------------

    $ git submodule update --init
    $ git submodule update --remote
    $ bower install
    $ virtualenv -p python3 venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

Because the app submodules [each point to a particular commit][1], which may be
older than the head of the master branch of their respective repository, run

    $ git submodule update --remote

whenever new commits are made in submodule repositories.

Initializing the Application
----------------------------

With the environment set up, now you can configure the application:

    $ cd ghu_web
    $ python generate_key.py
    $ python manage.py migrate

Running a Debug Server
----------------------

After activating the virtualenv and `cd`ing to `ghu_web/`:

    $ python manage.py runserver

[1]: https://stackoverflow.com/a/18797720/321301
