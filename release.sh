#!/bin/bash
# usage: `./release.sh [<live|...>]`
# calls `setup.py` to build distributables and uploads the result to `test.pypi.org` or `pypi.org`
# expected flow is `develop` -> `approved` -> `master` -> release
set -eu

index=${1:-"test"}

pypi_repository="testpypi"
pypi_url="https://test.pypi.org/pypi"
if [ "$index" = "live" ]; then
    pypi_repository="pypi"
    pypi_url="https://pypi.org/pypi"
fi

# avoid setting this on the command line, it will be visible in your history.
token="$TWINE_PASSWORD"
if [ -z "$token" ]; then
    echo "TWINE_PASSWORD is not set. This is the pypi.org or test.pypi.org API token"
    exit 1
fi

# check we are on the `master` branch.
# disabled: Jenkins checkouts out a revision and not a branch. we're not going to get a branch name.
# branch_name=$(git branch --show-current) # git 2.22+
#branch_name=$(git rev-parse --abbrev-ref HEAD)
#if [ "$branch_name" != "master" ]; then
#    echo "This is *not* the 'master' branch. Releases should happen from 'master' and not '$branch_name'."
#    echo "ctrl-c to quit, any key to continue."
#    # failure to read input within timeout causes script to exit with error code 142 rather than wait indefinitely
#    timeout=10 # seconds
#    read -t $timeout
#fi

echo "--- building"
rm -rf ./release-venv/ dist/ build/ *.egg-info
python3 -m venv release-venv
source release-venv/bin/activate
python3 -m pip install --upgrade pip setuptools wheel twine
python3 setup.py sdist bdist_wheel

echo "--- testing build"
python3 -m twine check \
    --strict \
    dist/*

echo "--- checking against remote release"
local_version=$(python3 setup.py --version)
local_version="($local_version)" # hack

package_name=$(python3 setup.py --name)
# "elife-dummy-python-release-project (0.0.1)                      - A small example package"  =>  "(0.0.1)"
remote_version=$(pip search "$package_name" --index "$pypi_url" --isolated | grep "$package_name" | awk '{ print $2 }')
if [ "$local_version" = "$remote_version" ]; then
    echo "Local version '$local_version' is the same as the remote version '$remote_version'. Not releasing."
    exit 0 # not a failure case
else
    echo "Local version '$local_version' not found remotely, releasing."
fi

echo "--- uploading"
python3 -m twine upload \
    --repository "$pypi_repository" \
    --username "__token__" \
    --password "$token" \
    dist/*
