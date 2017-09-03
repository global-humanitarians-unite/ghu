Global Humanitarians Unite
==========================

This is the Global Humanitarians Unite website prototype.

Environment Setup
-----------------

    $ bower install
    $ virtualenv -p python3 venv
    $ . venv/bin/activate
    $ pip install -r requirements.txt

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
