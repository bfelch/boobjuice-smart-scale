#!/bin/bash
MYDIR="$(dirname $(realpath $0))"

source boobjuice-venv/bin/activate
python "${MYDIR}/smartscale.py"
