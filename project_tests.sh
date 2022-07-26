#!/bin/bash
set -e
. install.sh
coverage run -m pytest
