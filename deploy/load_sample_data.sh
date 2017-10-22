#!/bin/bash
set -e
set -o pipefail

[[ -z $GHU_DEPLOY_CONFIG_PATH ]] && {
    printf 'error: $GHU_DEPLOY_CONFIG_PATH is not set. Set it to the path to '`
          `'deploy.config and try again\n' >&2
    exit 1
}

. "$GHU_DEPLOY_CONFIG_PATH"

. "$deploy_root/venv/bin/activate"
cd "$deploy_root/worktrees/current/ghu_web"
python manage.py loaddata pages
