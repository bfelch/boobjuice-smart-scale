#!/bin/bash
MYDIR="$(dirname $(realpath $0))"

echo "beginning boobjuice setup"
# install all dependencies for smartscale
apt-get install python3
apt-get install pip

python3 -m venv boobjuice-venv
source boobjuice-venv/bin/activate

python3 -m pip install -r "${MYDIR}/requirements.txt"

apt-get install i2c-tools
git clone https://github.com/tatobari/hx711py
git clone https://github.com/sterlingbeason/LCD-1602-I2C

# run smartscale at startup
cd $HOME

file=".bashrc"
if ! test -f $file; then
    touch $file
fi

if grep -q "boobjuice" "$file"; then
    echo "already running at startup"
else
    echo "bash ~/boobjuice-smart-scale/startup.sh" >> $file
    echo "set to run on startup"
fi

echo "setup complete!"
