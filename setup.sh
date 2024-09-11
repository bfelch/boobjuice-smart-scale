#!/bin/bash
MYDIR="$(dirname $(realpath $0))"

echo "beginning boobjuice setup"
apt-get install python3
apt-get install pip
apt-get install git

python3 -m venv boobjuice-venv
source boobjuice-venv/bin/activate

python3 -m pip install -r "${MYDIR}/requirements.txt"

apt-get install i2c-tools
git clone https://github.com/tatobari/hx711py
git clone https://github.com/sterlingbeason/LCD-1602-I2C

echo "setup complete!"
