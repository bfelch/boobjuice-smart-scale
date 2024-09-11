# BoobJuice Smart Scale
## 🛑 **THIS APPLICATION IS NOT YET COMPLETE, PLEASE CHECK BACK LATER** 🛑

Application is still undergoing changes and will not yet work as expected

## ⚠️ Requirements ⚠️

1. BoobJuice WebApp - check that out [here](https://github.com/bfelch/boobjuice-web-app).
2. Raspberry Pi - I used an RPi4. Any should work, but some config steps may vary.
3. Load Cell & HX711 AD Amplifier
4. 2x Push Buttons
5. Keyboard and Monitor - Only needed to complete setup, not part of final device.

## Setup
### Raspberry Pi Config

1. Use Raspberry Pi Imager to flash a microSD card with your OS of choice (I used Raspberry Pi OS Lite)
	- Leave user password blank as you won't have a way to enter it during normal use
	- Wifi SSID and password can be set during this step as well instead of the next step
2. Insert microSD card into Raspberry Pi and power it on
	- Once the Raspberry Pi has finished booting and you have access to the terminal, you can continue to the next steps
3. Type `sudo raspi-config` and hit enter
4. Select `system options > wireless LAN`
	- Skip this step if completed earlier
5. Enter your wifi SSID and password
6. Return to the Config main screen
7. Select `interface options > i2c`
8. Choose to enable i2c
9. Return to the Config main screen
10. Select `finish`

### Raspberry Pi Wiring

- TODO: Add wiring diagrams and written instructions

### Smart Scale Application

- TODO: apt-get install git
- TODO: clone repo
- TODO: set service host
- TODO: run setup.sh
- TODO: reboot

## Usage

There are two buttons that control all functions on the scale. One is the Send/OK button and the other is the Tare/Cancel button.

- Send/OK
	- Pressing this the first time will bring up a confirmation screen. This screen shows what data will be sent to the web app if confirmed.
 	- Pressing this while on the confirmation screen will initiate the send, print the response, then bring you back to the main display.
- Tare/Cancel
	- This button has multiple functions depending on the type of press (short/long) and the screen (main/confirmation).
	- Main Screen
		- Short pressing this will tare or zero the scale.
		- Long pressing this (>5 seconds, configurable in config.ini) will power off the device. Always do this instead of just unplugging.
	- Confirmation Screen
		- Pressing this (short/long press don't matter, only one function here) will cancel the send and bring you back to the main screen.
