#!/bin/bash
set -e
set -o pipefail

[[ -z $GHU_ADMIN_PASSWORD ]] && {
    printf 'error: $GHU_ADMIN_PASSWORD is not set. Set it to the Django admin '`
          `'password and try again\n' >&2
    exit 1
}

# This is sensitive, so don't want to pass this to subsequent commands
admin_pass=$GHU_ADMIN_PASSWORD
export GHU_ADMIN_PASSWORD=

[[ -z $GHU_DEPLOY_CONFIG_PATH ]] && {
    printf 'error: $GHU_DEPLOY_CONFIG_PATH is not set. Set it to the path to '`
          `'deploy.config and try again\n' >&2
    exit 1
}

. "$GHU_DEPLOY_CONFIG_PATH"

. "$deploy_root/venv/bin/activate"
cd "$deploy_root/worktrees/current/ghu_web"
python manage.py mkadmin <<<"$admin_pass"
python manage.py loaddata pages
