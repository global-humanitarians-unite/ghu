Deployment Documentation
========================

A brief, sad history of deployment
----------------------------------

Early in this project and in earlier classes, I deployed my code to production
as follows:

 1. Test my code locally
 2. Commit, push to master
 3. `ssh` into production server
 4. `git pull` on production
 5. Restart [`uwsgi`][2], which was running in a [`tmux`][1] session

This sucks for several reasons:

 1. I had to do it by hand whenever I want to update production, and only I
    could do it because no one else knows how. This got tedious fast
 2. The environment in which I test code locally, `manage.py runserver`,
    differs significantly from production, nginx with uwsgi and `DEBUG=False`,
    etc. So I was pushing undertested code to production
 3. I restarted `uwsgi` by `^C`ing and then restarting it, leaving a brief
    period during which the site was unavailable, which lengthened when I found
    an issue and had to fix it

Realizing the unsustainability of this process, I set out to make a process
that saves time, effort, and frustration by:

 1. Running automatically
 2. Allowing us to test code in a production-like environment before deploying
    it
 3. Do the update without major disruption (The site may serve an old page but
    then a new `style.css`, for example, if a user hits the site during an
    update, but we can't avoid that easily — just don't go down)

The new solution
----------------

We use the following deployment process now:

 1. When someone pushes (or merges a PR) to `develop` or `master`, a GitHub
    webhook hits an HTTP API provided by Jenkins on
    https://jenkins.globalhumanitariansunite.org/. This triggers the
    corresponding Jenkins build, which calls `deploy.sh` to deploy the new code
    to https://develop.globalhumanitariansunite.org/ (QA, for pushes to the
    `develop` branch) or https://globalhumanitarainsunite.org/ (production, for
    pushes to the `master` branch)
 2. https://develop.austinjadams.com/ matches the setup of production
    environment almost exactly, and gets rebuilt for any change to `develop`,
    so after merging a PR you can make sure your change works as expected
 3. `deploy.sh` reloads `uwsgi` by [`touch`][3]ing a file `uwsgi` watches for
    changes. While it restarts, `uwsgi` does not close the listen socket, so
    requests won't get lost

A rundown of `ls -1`: What each file does
-----------------------------------------

 * **Configuration**
     * `config.deploy-example.ini`: An example configuration file for
       deployment. Note that if you use Postgres, because `deploy.sh` will run
       `python manage.py migrate`, and `deploy.sh` runs as `jenkins` instead of
       `ghu` (or whatever user `uwsgi` runs as, which should match the database
       user), you need to configure a TCP connection to localhost with a user
       and password. Don't use unix sockets (aka don't leave out `host =`),
       because `pg_hba.conf` by default uses `peer` authentication, which means
       the system user you're running as _must_ match the database user you're
       trying to authenticate as. These are different users for the server and
       for Jenkins, so deployments will fail.
     * `deploy.config`: Contains the URL and branch to clone and other
       configuration specific to deployment scripts. Should be an HTTP URL
       unless you've got keys set up. If you change the clone URL or branch,
       you should delete `$deploy_root/repo`.
 * **Scripts**
     * `deploy.sh`: Called by Jenkins in response to a GitHub webhook. Does the
       following, roughly:

       1. Create virtualenv if it does not exist yet
       2. Pull/clone new changes from `$clone_url` and checks them out into a
          new directory 
       3. Backs up `deploy.sh` to `deploy.sh.old` (useful if a push breaks the
          deploy scripts)
       4. Copy `deploy.sh`, `fresh_checkout.sh`, `nginx.conf`, and the systemd
          unit to `$deploy_dir`
       5. Calls `fresh_checkout.sh` on the new checkout directory
       6. Touch `$deploy_dir/reload` to tell uwsgi to reload
     * `fresh_checkout.sh`: Does the tedious work of setting up a fresh
       checkout — basically the steps in the README. Roughly:
       1. Installs bower packages (`bower install`)
       2. Symlinks `ghu_web/config.ini` to `$deploy_root/config.ini` to use
          system configuration
       3. Activates Python virtual environment
       4. Uses pip to install Python dependencies from both `/requirements.txt`
          and `/deploy/requirements.txt`
       5. Performs database migrations (`manage.py migrate`)
       6. Collects static files (`manage.py collectstatic`)
     * `init_deploy.sh`: Helper script for bootstrapping a deployment
        environment. Will copy over necessary files to `$deploy_root/`. **Run
        this script as your `jenkins` user**.
 * `ghu.service`: [systemd unit][4] for `uwsgi` which runs `run.sh`
 * `nginx.conf`: snippet of [nginx][5] configuration
 * `README.md`: You're reading this!
 * `requirements.txt`: Deployment-specific python dependencies.
 * `fresh_checkout.sh` will install dependencies from `/requirements.txt`, then
   this
 * `run.sh`: Shell script that runs `uwsgi` will all the right configuration
   flags

[1]: https://en.wikipedia.org/wiki/Tmux
[2]: https://uwsgi-docs.readthedocs.io/en/latest/
[3]: https://en.wikipedia.org/wiki/Touch_(Unix)
[4]: https://www.freedesktop.org/software/systemd/man/systemd.service.html
[5]: https://en.wikipedia.org/wiki/Nginx
