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
 * `ghu.service`: [systemd unit][4] for `uwsgi` which runs `run.sh`
 * `nginx.conf`: snippet of [nginx][5] configuration
 * `nginx-ssl.conf`: global [nginx][5] SSL configuration. The ansible script
   copies this to `/etc/nginx/conf.d/ssl.conf`
 * `nginx-sites/`: Configuration for each nginx site. Copied over initially by
   Ansible to `/etc/nginx/sites-available`
 * `README.md`: You're reading this!
 * `requirements.txt`: Deployment-specific python dependencies.
 * `run.sh`: Shell script that runs `uwsgi` will all the right configuration
   flags
 * `request_cert.sh`: Shell script that calls `certbot` with the name of all
   our domains. Run on remote server by Ansible script
 * `jenkins/`: Jenkins jobs run automatically by GitHub webhooks
 * `secrets.yml`: An ansible vault containing all kinds of credentials that
   future maintainers might need. You can view it with `ansible-vault view
   secrets.yml --ask-vault-pass`.
 * `ghu.yml`: The ansible script for initial setup. See the section below for
   details.

Ansible Initial Deployment Script
---------------------------------

The deployment scripts are great and all, but they still left me `ssh`ing in a
lot to tweak things. However, if I (the tweaker-in-chief) disappear,
administrators still need to make changes to the site, so I wrote this Ansible
script to take care of that.

Here's how you'd set up a new server running ghu:

 1. In the AWS console, create an Amazon EC2 medium instance with [Debian
    Stretch][6]. I gave it 32GiB of storage.
 2. Still in the AWS console, edit the security group to open up TCP ports 80
    and 443.
 3. Also in the AWS console, go into Route 53 and set the hostnames seen in
    `request_cert.sh` to point to the IP address of the instance you've created.
 4. Again in the AWS console, create an IAM user named `ghu-master` (or
    something like that) and give it full access to SES. Generate a access key
    and secret key for it.
 5. Save the ssh key for the instance to `~/.ssh/id_rsa_ghu` or whatever.
    `chmod` it to 600 or something decent, and then add the following to
    `~/.ssh/config`:

        Host ghu
            User admin
            HostName IP_ADDRESS_HERE
            Port 22
            IdentityFile ~/.ssh/id_rsa_ghu
            IdentitiesOnly yes

 6. Now you should be able to ssh into the machine with `ssh ghu`, so create a
    modest Ansible inventory file `hosts` with one line: `ghu`:

        $ printf 'ghu\n' >hosts

 7. Finally, you can run the playbook with:

        $ ansible-playbook --ask-vault-pass -i hosts ghu.yml

    If you don't have the vault password, you can generate a new vault by
    deleting `secrets.yml` and creating another by running `ansible-vault
    create secrets.yml`, and then adding the following contents to the vault:

        vault_postgresql_password: POSTGRES_PASSWORD_HERE
        vault_django_admin_password: DJANGO_ADMIN_PASSWORD_HERE
        # Amazon API creds for the IAM user for prod (found above)
        vault_aws_access_key: AWS_ACCESS_KEY_HERE
        vault_aws_secret_key: AWS_SECRET_KEY_HERE

 8. Now the website should be running, but you still need to set up Jenkins.
    See the following section for that.

You can re-run `ansible-playbook` with the command line shown above whenever
you want to update server configuration that lives outside `$deploy_dir`, such
as `config.ini` or overall nginx configuration. If you want to target only
develop or only master, pass `--extra-vars='{"branches":["develop"]}'` or
`--extra-vars='{"branches":["master"]}'` as an argument to `ansible-playbook`.

Jenkins Setup
-------------

We haven't ansible-ized the Jenkins setup process, so you'll have to go through
the Wizard, but it's not too bad. The ansible scripts automatically create the
jobs, and that's the tedious part.

 1. Get the admin password from the server with something like

        $ ssh ghu sudo cat /var/lib/jenkins/secrets/initialAdminPassword

    and use it to start the wizard at https://jenkins.globalhumanitariansunite.org/.
 2. Click the button for using the default set of plugins.
 3. Future versions of Jenkins might fix this, but right now, the wizard hangs
    if you don't enter an email addresson the next screen. So definitely do that.
 4. Follow the instructions on https://my.slack.com/services/new/jenkins-ci to
    install the Slack Notifications plugin and set it up.
 5. Now you need to configure GitHub webhooks. Use `ansible-vault view
    secrets.yml --ask-vault-pass` to see the personal access token for the
    [ghu-jenkins][7] account (or create a new personal access token in [the
    GitHub settings][8] for that account). Then under
    https://jenkins.globalhumanitariansunite.org/configure, add a GitHub server
    in the "GitHub Servers" section with that personal access token as a new
    secret key credential.
 6. The GitHub plugin will automatically create webhooks for each job as needed
    if you go to their Configure page and hit the Save button. (Realistically,
    since both the ghu-develop and ghu-master jobs share the same webhook since
    they are "hooked" by the same repository, you need to this for only one of
    them.)

[1]: https://en.wikipedia.org/wiki/Tmux
[2]: https://uwsgi-docs.readthedocs.io/en/latest/
[3]: https://en.wikipedia.org/wiki/Touch_(Unix)
[4]: https://www.freedesktop.org/software/systemd/man/systemd.service.html
[5]: https://en.wikipedia.org/wiki/Nginx
[6]: https://wiki.debian.org/Cloud/AmazonEC2Image
[7]: https://github.com/ghu-jenkins/
[8]: https://github.com/settings/tokens/new
