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

Because submodule for the [ghu\_toolkits][1] app [points to a particular
commit][2], which may be older than the head of the [ghu\_toolkits][1]
master branch, you should run

    $ git submodule update --remote

whenever new commits are made in the [ghu\_toolkits][1] repository.

Running a Debug Server
----------------------

After activating the virtualenv:

    $ cd ghu_web
    $ ./manage.py runserver

[1]: https://github.com/global-humanitarians-unite/ghu_toolkits
[2]: https://stackoverflow.com/a/18797720/321301
