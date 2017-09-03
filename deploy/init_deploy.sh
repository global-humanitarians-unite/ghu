#!/bin/bash
# This script sets up the deploy directory for you. Clone this repository
# somewhere temporary (like your homedir), run this AS THE USER USED BY THE
# DEPLOYMENT SCRIPTS (e.g., jenkins), then you can delete the repo (the scripts
# won't use it any more).

set -e
set -o pipefail

[[ $(id -u) == 0 ]] && {
    printf 'error: Do not run this script as root! Instead, run it as the '`
          `'user used in deployment. Try something like (if the deployment '`
          `'user is jenkins):\n\tsudo -u jenkins %s\n' "$0" >&2
    exit 1
}

# Calculate the absolute path to this repo
repo_path="$(readlink -f "$(dirname "${BASH_SOURCE[0]}")"/..)"
printf '(Temporary) repository path is `%s'\''\n' "$repo_path"

read -rep 'Where do you want the deploy root directory? '`
         `'[default: /var/www/ghu] ' deploy_root
[[ -z $deploy_root ]] && \
    deploy_root=/var/www/ghu || \
    deploy_root=$(readlink -f "$deploy_root")

# Cool, we know this now
GHU_DEPLOY_CONFIG_PATH=$deploy_root/deploy.config

printf 'Creating deploy root `%s'\'' if it does not already '`
      `'exist...\n' "$deploy_root"
mkdir -p "$deploy_root" || {
    printf 'error: This user probably lacks permission to create `%s'\''. '`
          `'Try:\n'`
          `'\tsudo mkdir /var/www/ghu\n'`
          `'\tsudo chown jenkins:jenkins /var/www/ghu\n' "$deploy_root" >&2
    exit 1
}

printf 'Copying over essentials to `%s'\''...\n' "$deploy_root"
cp -iv "$repo_path/deploy/config.deploy-example.ini" "$deploy_root/config.ini"
cp -iv "$repo_path/deploy/"{deploy.sh,deploy.config} "$deploy_root"
# TODO: Escape the path better here, both for sed and for the bash double
#       quotes "" in deploy.config
sed -ie "s/ABSOLUTE_PATH_TO_DEPLOY_ROOT/${GHU_DEPLOY_CONFIG_PATH//\//\\\/}/" \
        "$deploy_root/deploy.config"

# Generate a Django SECRET_KEY
"$repo_path/ghu_web/generate_key.py" "$deploy_root/config.ini"

printf 'Done!\n\n'`
      `'Now you can delete this repository, tweak application configuration '`
      `'in `%s'\'', and run your first deployment! Note you will need to run '`
      `'it as the deployment user (e.g., jenkins) like:\n'`
      `'\tsudo -u jenkins GHU_DEPLOY_CONFIG_PATH="%s" "%s"\n' \
      "$deploy_root/config.ini" "$deploy_root/deploy.config" \
      "$deploy_root/deploy.sh"

exit 0
