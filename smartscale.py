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

def setup_default_button_actions():
    GPIO.remove_event_detect(CONFIRM_PIN)
    GPIO.remove_event_detect(CANCEL_PIN)

    GPIO.add_event_detect(CONFIRM_PIN, GPIO.RISING, callback=record, bouncetime=300)
    GPIO.add_event_detect(CANCEL_PIN, GPIO.BOTH, callback=tare_shutdown, bouncetime=100)

    global confirming
    confirming = False

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
        'grams': grams,
        'minutes': elapsed
    }
    
    print(f'sending... {url}')
    print(f'data: {params}')
    #r = requests.put(url, json=params)
    #status = r.status_code
    #print(status)
    
    # TODO log status and message?

    setup_default_button_actions()

    #return status

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
    
    hx.power_down()
    hx.power_up()
    
    return val

def power_off():
    print('powering off...')
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

while True:
    try:
        if confirming:
            lcd.message('Submit pump Y/N?', 1)
            lcd.message(f'{grams: >7}g {elapsed: >4}min', 2)
        else:
            grams = weigh()
            mliters = round(grams / 1.03)
            elapsed = math.floor((time.time() - start) / 60)
            lcd.message(f'Pump time: {elapsed: >2}min', 1)
            lcd.message(f'{grams: >7}g {mliters: >5}ml', 2)
        
        time.sleep(0.1)

    except (KeyboardInterrupt, SystemExit):
        clean_and_exit()

