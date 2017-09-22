#!/bin/bash
set -e 
set -o pipefail

[[ -z $GHU_DEPLOY_CONFIG_PATH ]] && {
    printf 'error: $GHU_DEPLOY_CONFIG_PATH is not set. Set it to the path to '`
          `'deploy.config and try again\n' >&2
    exit 1
}

. "$GHU_DEPLOY_CONFIG_PATH"

[[ -z $1 ]] && worktree=. \
            || worktree=$1

worktree=$(readlink -f "$worktree")

printf 'Setting up fresh worktree `%s'\''...\n' "$worktree"
cd "$worktree"
repo="$deploy_root/repo"
bower install
ln -sv "$deploy_root/config.ini" ghu_web/config.ini

. "$deploy_root/venv/bin/activate"
pip install -r requirements.txt
pip install -r deploy/requirements.txt
cd "$worktree/ghu_web"
# Pass --no-input since this might be running as a non-interactive Jenkins job
python manage.py migrate --no-input
python manage.py collectstatic
