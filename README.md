## ⚠️ Requirements ⚠️

1. BoobJuice WebApp - check that out [here](https://github.com/bfelch/boobjuice-web-app).
2. Raspberry Pi - I used an RPi4. Any should work, but some config steps may vary.
3. Load Cell & HX711 AD Amplifier
4. LCD1602 Display Module & LCD1602 I2C Serial Interface
5. 2x Push Buttons
6. Keyboard and Monitor - Only needed to complete setup, not part of final device.

## Setup
### Raspberry Pi Wiring

Refer to the images below to assist with wiring. Some of the pins can be changed in config.ini or swapped for preference, this is what worked for me.

1. Raspberry Pi -> HX711 Amplifier
	- 5V (4) > VCC
	- GND (9) > GND
	- GPIO5 (29) > DT
	- GPIO6 (31) > SCK
2. HX711 Amplifier -> Load Cell
	- E+ > Red
	- E- > Black
	- A- > White
	- A+ > Green
3. Raspberry Pi -> LCD1602 I2C Serial Interface
	- 5V (2) > VCC
	- GPIO2 (3) > SDA
	- GPIO3 (5) > SCL
	- GND (6) > GND
4. LCD1602 I2C Serial Interface -> LCD1602 Display Module
	- The pins on each should line up, just make sure the orientation is correct
	- I left the backlight pins in, the display was too hard to see without that
	- If the display doesn't seem to show anything while powered on, try adjusting the contrast
5. Raspberry Pi -> Buttons (I'm not sure how to label the button pins, check the images for clues)
	- GND (14) > Both Buttons
	- GPIO23 (16) -> Tare/Cancel/PowerOff Button
	- GPIO24 (18) -> Send/Ok Button

![wiring diagram](/.github/images/wiring%20diagram.png?raw=true "Wiring Diagram")
![pinout](/.github/images/pinout.png?raw=true "Pinout")

### Raspberry Pi Config

1. Use Raspberry Pi Imager to flash a microSD card with your OS of choice (I used Raspberry Pi OS Lite)
	- Username and password can be set during this step or during first boot, password will not be needed after completing setup
	- Wifi SSID and password can be set during this step
2. Insert microSD card into Raspberry Pi and power it on
	- Enter username and password when prompted
	- Once the Raspberry Pi has finished booting and you have access to the terminal, you can continue to the next steps
3. Type `sudo raspi-config` and hit enter
4. Connect to wifi
	1. Skip these steps if completed earlier
	2. Select `system options > wireless LAN`
	3. Enter your wifi SSID and password
	4. Return to the Config main screen
5. Enable I2C
	1. Select `interface options > i2c`
	2. Choose to enable i2c
	3. Return to the Config main screen
6. Enable autologin
	1. Select `system options > boot/auto login > console autologin`
	2. Return to the Config main screen
7. Select `finish`
8. Reboot if asked

### Smart Scale Application

1. Install git with `sudo apt-get install git`
	1. Enter `y` when asked to continue
2. Clone smart scale repo with `git clone https://github.com/bfelch/boobjuice-smart-scale`
3. Update config file
	1. Open config.ini with `sudo nano boobjuice-smart-scale/config.ini`
	2. Set `host` value to point at your web app container
	3. Save with `ctrl+x` and `y`
4. Run setup.sh with `bash boobjuice-smart-scale/setup.sh`
8. Calibrate the scale
	1. Start the program with `bash boobjuice-smart-scale/startup.sh`
	2. Place an item of known weight on the scale
	3. Calculate `new_factor = displayed_value / known_weight_in_grams`
	4. Stop smartscale.py with `ctrl+c`
 	5. Open config.ini with `sudo nano boobjuice-smart-scale/config.ini`
  	6. Set `calibration_factor = {new_factor}`
	7. Save with `ctrl+x` and `y`
9. Reboot with `shutdown -r now`
10. Your scale is all set! You can power down by long pressing the Tare/Cancel button

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
