#!/usr/bin/python
import os
import glob
import time
import json
import requests
import sys
import I2C_LCD_driver

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
mylcd = I2C_LCD_driver.lcd()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    # Change to appropriate location
    # LOCATION = "shower"
    LOCATION = "cabin"
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        #  return {"location" : LOCATION, "celsius" : temp_c, "fahrenheit" : temp_f}
        return 'Temp: %.2f C' % (temp_c)
while True:
        mylcd.lcd_display_string(read_temp(),1)
        mylcd.lcd_display_string('45 Litres remain',2)
        time.sleep(1)
