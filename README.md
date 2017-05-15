Global Humanitarians Unite
==========================

This is the Global Humanitarians Unite website prototype.

Setup
-----

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

Running a Debug Server
----------------------

After activating the virtualenv:

    $ cd ghu_web
    $ ./manage.py runserver

[1]: https://stackoverflow.com/a/18797720/321301
