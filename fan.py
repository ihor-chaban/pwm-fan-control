#!/usr/bin/env python3

import json
import os
import signal
import time
from config import *
from rpi_hardware_pwm import HardwarePWM

FAN_OFF = 0
FAN_MAX = 100

def getCpuTemperature():
    result = os.popen('cat /sys/class/thermal/thermal_zone0/temp').readline()
    return float(result) / 1000

def scale(value, in_min, in_max, out_min, out_max):
    if value < in_min:
        return FAN_OFF
    elif value > in_max:
        return FAN_MAX
    else:
        return (value - in_min) * (out_max - out_min) / (in_max- in_min) + out_min

def setFanSpeed(speed, temperature):
    speed = int(round(speed))
    pwm.change_duty_cycle(speed)
    if VERBOSE == True:
        print('Speed: ', speed, '\tTemperature: ', temperature)
    if JSON == True:
        data = {}
        data['fan_speed'] = speed;
        data['fan_temperature'] = temperature
        with open(os.path.dirname(os.path.realpath(__file__))+'/metrics.json', 'w') as outfile:
            json.dump(data, outfile)
    return()

pwm = HardwarePWM(0, hz=PWM_FREQ)
pwm.start(FAN_MAX)

while True:
    cpuTemperature = getCpuTemperature()
    setFanSpeed(scale(cpuTemperature, MIN_TEMP, MAX_TEMP, FAN_LOW, FAN_HIGH), cpuTemperature)
    time.sleep(WAIT_TIME)
