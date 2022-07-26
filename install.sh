#!/bin/bash
set -e
. mkvenv.sh
source venv/bin/activate
pip install pip wheel --upgrade
pip install -r requirements.txt
