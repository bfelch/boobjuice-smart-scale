import configparser
import os
import sys
import math
import requests
import time
import RPi.GPIO as GPIO

sys.path.append('./LCD-1602-I2C')
sys.path.append('./hx711py')

from LCD import LCD
from hx711 import HX711

config = configparser.ConfigParser()
configPath = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(configPath)

SERVER_HOST = config['server'].get('host')
SERVER_ROUTE = config['server'].get('route')

SCALE_PIN = config['scale'].getint('pin')
CALIBRATION_FACTOR = config['scale'].getint('calibration_factor')

CONFIRM_PIN = config['buttons'].getint('confirm')
CANCEL_PIN = config['buttons'].getint('cancel')

PI_REV = config['display'].getint('pi_rev')
I2C_ADDR = int(config['display'].get('i2c_addr'), 16)
BACKLIGHT = config['display'].getboolean('backlight')

def confirm_record(grams, minutes):
    # change to confirmation screen
    # 'Confirm? Y/N Xmin Yg Zml'
    # wait for confirm/cancel input
    # if cancel, return
    # if confirm, record(grams, minutes)
    pass

def record(grams, minutes):
    url = SERVER_HOST + SERVER_ROUTE
    params = {
        'grams': grams,
        'minutes': minutes
    }
    
    r = requests.put(url, json=params)
    status = r.status_code
    print(status)
    
    # TODO log status and message?
    return status

def tare():
    hx.reset()
    hx.tare()
    return time.time()

def weigh():
    val = hx.get_weight(SCALE_PIN)
    val = int(val)
    print(val)
    
    hx.power_down()
    hx.power_up()
    
    return val

def power_off():
    # clean_and_exit, then shutdown
    pass

def clean_and_exit():
    lcd.clear()
    lcd.message('Bye!', 1)
    time.sleep(1)
    
    print('Bye!')
    lcd.clear()
    GPIO.cleanup()
    sys.exit()

### Begin program ###
hx = HX711(SCALE_PIN, 6)
hx.set_reading_format('MSB', 'MSB')
hx.set_reference_unit(CALIBRATION_FACTOR)

GPIO.setmode(GPIO.BCM)
# Confirm Button handles Send/OK
GPIO.setup(CONFIRM_PIN, GPIO.IN)
# Cancel Button handles Tare/Cancel/Power Off
GPIO.setup(CANCEL_PIN, GPIO.IN)

start = tare()
print('Tare done! Add weight now...')

lcd = LCD(PI_REV, I2C_ADDR, BACKLIGHT)
lcd.message('Ready!', 1)
time.sleep(1)

cancel_pressed = False
cancel_pressed_start = 0

while True:
    try:
        grams = weigh()
        mliters = round(grams / 1.03)
        elapsed = time.time() - start
        elapsed = math.floor(elapsed / 60)
        lcd.message(f'Pump time: {elapsed: >2}min', 1)
        lcd.message(f'{grams: >7}g {mliters: >5}ml', 2)
        
        confirm_btn = GPIO.input(CONFIRM_PIN)
        cancel_btn = GPIO.input(CANCEL_PIN)
        #if confirm_btn == GPIO.LOW:
        #    confirm_record(grams, elapsed)
        #elif cancel_btn == GPIO.LOW:
        #    if not cancel_pressed:
        #        cancel_pressed_start = time.time()
        #    cancel_pressed = True
        #elif cancel_pressed:
        #    cancel_pressed = False
        #    if time.time() - cancel_pressed_start >= 3:
        #        power_off()
        #    else:
        #        start = tare()
        
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

