#!/bin/bash
set -e
. mkvenv.sh
source venv/bin/activate
pip install pip wheel pytest coverage --upgrade
pip install -r requirements.txt
coverage run -m pytest
