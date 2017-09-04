#!/bin/bash
# Perform a deployment.

set -e
set -o pipefail

[[ -z $GHU_DEPLOY_CONFIG_PATH ]] && {
    printf 'error: $GHU_DEPLOY_CONFIG_PATH is not set. Set it to the path to '`
          `'deploy.config and try again\n' >&2
    exit 1
}

. "$GHU_DEPLOY_CONFIG_PATH"

# Create virtualenv
venv="$deploy_root/venv"
[[ ! -e $venv ]] && {
    printf 'Python virtualenv `%s'\'' does not exist yet, '`
          `'creating it...\n' "$venv"
    virtualenv -p python3 "$venv"
}

# Update repo
repo="$deploy_root/repo"
if [[ ! -e $repo ]]; then
    printf 'Bare mirror repository `%s'\'' does not exist yet, '`
          `'cloning it...\n' "$repo"
    git clone --mirror --branch "$clone_branch" "$clone_url" "$repo"
    cd "$repo"
else
    printf 'Bare repository `%s'\'' exists, attempting to update '`
          `'it...\n' "$repo"
    cd "$repo"
    git fetch
fi
worktrees="$deploy_root/worktrees"
mkdir -vp "$worktrees"
printf 'Looking up current commit SHA-1...\n'
commit=$(git rev-parse --short=8 HEAD)
worktree=$(mktemp -dp "$worktrees" "${BUILD_NUMBER:-NO_BUILD_NUMBER}-$commit-XXXXXXXX")
# mktemp creates directories with 700 permissions, so correct it
chmod 755 "$worktree"
printf 'Checking out commit `%s'\''...\n' "$commit"
GIT_WORK_TREE=$worktree git checkout -f

# Copy over useful lil scripts
printf 'Updating deployment scripts...\n'
cd "$worktree/deploy"
# In an emergency (if a push breaks the deploy script), we can copy the old
# deploy.sh back over and push again
mv -v "$deploy_root/deploy.sh"{,.old}
cp -v run.sh deploy.sh fresh_checkout.sh nginx.conf "$deploy_root"
cp -v ghu.service "$deploy_root/$systemd_unit_name"
sed -i -e "s/DEPLOY_CONFIG_PATH_HERE/${GHU_DEPLOY_CONFIG_PATH//\//\\\/}/g; "`
         `"s/SERVER_USER_HERE/$server_user/g; "`
         `"s/DEPLOY_ROOT_HERE/${deploy_root//\//\\\/}/g" \
    "$deploy_root/$systemd_unit_name"
sed -i -e "s/DEPLOY_ROOT_HERE/${deploy_root//\//\\\/}/g" \
    "$deploy_root/nginx.conf"

# Setup freshly-checked out repo
printf 'Initializing worktree...\n'
"$deploy_root/fresh_checkout.sh" "$worktree"

# Point to the new version of the site (atomically!)
printf 'Updating current worktree symlink...\n'
worktree_current=$worktrees/current
worktree_current_tmp=$worktrees/current.tmp
worktree_current_old=$worktrees/current.old
worktree_current_old_old=$(readlink -e "$worktree_current_old" || true)
ln -svnrf "$worktree" "$worktree_current_tmp"
[[ -e $worktree_current ]] && cp -PTv "$worktree_current" "$worktree_current_old"
# Use rename(2), which is atomic
mv -Tv "$worktree_current_tmp" "$worktree_current"
rm -rvf "$worktree_current_old_old"

printf 'Reloading uwsgi...\n'
touch "$deploy_root/reload"

printf 'Deployment done!\n'

exit 0
