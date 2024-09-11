#!/bin/bash
MYDIR="$(dirname $(realpath $0))"

echo "beginning boobjuice setup"
#echo "installing python3"
#apt-get install python3
#echo "installing pip"
#apt-get install pip
#echo "installing git"
#apt-get install git

#echo "setting up venv"
python3 -m venv boobjuice-venv
source boobjuice-venv/bin/activate

#echo "pip installing required packages"
#echo "${MYDIR}"
python3 -m pip install -r "${MYDIR}/requirements.txt"

#echo "installing i2c-tools"
apt-get install i2c-tools
#echo "cloning hx711py repo"
git clone https://github.com/tatobari/hx711py
#echo "cloning LCD-1602-I2C repo"
git clone https://github.com/sterlingbeason/LCD-1602-I2C

echo "setup complete!"
