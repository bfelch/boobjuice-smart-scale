import configparser
import os
import sys
import math
import requests
import time

sys.path.append('./LCD-1602-I2C')
sys.path.append('./hx711py')

from RPi import GPIO
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

LONG_PRESS_DURATION = config['settings'].getint('long_press_duration')
TARGET_DENSITY = float(config['settings'].get('target_density'))

def setup_default_button_actions():
    GPIO.remove_event_detect(CONFIRM_PIN)
    GPIO.remove_event_detect(CANCEL_PIN)
    
    GPIO.add_event_detect(CONFIRM_PIN, GPIO.RISING, callback=record, bouncetime=300)
    GPIO.add_event_detect(CANCEL_PIN, GPIO.BOTH, callback=tare_shutdown, bouncetime=100)
    
    global confirming
    confirming = False
    global running
    running = True
    global sending
    sending = False
    global sendStatus
    sendStatus = ''

def record(channel):
    global confirming
    confirming = True
    
    GPIO.remove_event_detect(CONFIRM_PIN)
    GPIO.remove_event_detect(CANCEL_PIN)
    
    GPIO.add_event_detect(CONFIRM_PIN, GPIO.RISING, callback=confirm_record, bouncetime=300)
    GPIO.add_event_detect(CANCEL_PIN, GPIO.RISING, callback=cancel_record, bouncetime=300)

def confirm_record(channel):
    url = SERVER_HOST + SERVER_ROUTE
    params = {
        'mass': grams,
        'duration': elapsed
    }
    
    global sendStatus
    sendStatus = 'Sending...'
    
    global sending
    sending = True
    
    print(f'sending... {url}')
    print(f'data: {params}')
    
    r = requests.put(url, json=params)
    if r.status_code == 200:
        sendStatus = 'Success!'
    else:
        sendStatus = 'Error - ' + str(r.status_code)
    print(sendStatus)
    
    time.sleep(4)
    setup_default_button_actions()

def cancel_record(channel):
    print('canceling send...')
    setup_default_button_actions()

def tare_shutdown(channel):
    print('cancel pressed')
    if GPIO.input(channel) == GPIO.LOW:
        global cancel_pressed_start
        cancel_pressed_start = time.time()
    else:
        cancel_duration = time.time() - cancel_pressed_start
        if cancel_duration >= LONG_PRESS_DURATION:
            power_off()
        else:
            tare()

def tare():
    print('taring...')
    hx.reset()
    hx.tare()
    
    global start
    start = time.time()

def weigh():
    val = hx.get_weight(SCALE_PIN)
    val = int(val)
    print(val)
    
    return val

def power_off():
    global running
    running = False

def clean_and_exit(shutdown=False):
    message = 'Bye!'
    if shutdown:
        message = 'Shutting down...'
    
    lcd.clear()
    lcd.message(message, 1)
    time.sleep(1)
    
    print(message)
    lcd.LCD_BACKLIGHT = 0x00
    lcd.clear()
    
    GPIO.cleanup()
    
    if shutdown:
        os.system('sudo poweroff')
    else:
        sys.exit()

### Begin program ###
GPIO.cleanup()

hx = HX711(SCALE_PIN, 6)
hx.set_reading_format('MSB', 'MSB')
hx.set_reference_unit(CALIBRATION_FACTOR)

GPIO.setmode(GPIO.BCM)
# Confirm Button handles Send/OK
GPIO.setup(CONFIRM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Cancel Button handles Tare/Cancel/Power Off
GPIO.setup(CANCEL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

setup_default_button_actions()

tare()
print('Tare done! Add weight now...')

lcd = LCD(PI_REV, I2C_ADDR, BACKLIGHT)
lcd.message('Ready!', 1)
time.sleep(1)

while running:
    try:
        if sending:
            lcd.message('Status:', 1)
            lcd.message(sendStatus, 2)
        elif confirming:
            lcd.message('Submit pump Y/N?', 1)
            lcd.message(f'{grams: >7}g {elapsed: >4}min', 2)
        else:
            grams = weigh()
            mliters = round(grams / TARGET_DENSITY)
            elapsed = math.floor((time.time() - start) / 60)
            lcd.message(f'Pump time: {elapsed: >2}min', 1)
            lcd.message(f'{grams: >7}g {mliters: >5}ml', 2)
        
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

clean_and_exit(True)
