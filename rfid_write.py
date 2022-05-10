#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
import sys
import datetime
import time

def write(text):
    try:
        GPIO.setwarnings(False)
        reader = SimpleMFRC522()
        reader.write_no_block(text)

    except KeyboardInterrupt:
        GPIO.cleanup()
        raise