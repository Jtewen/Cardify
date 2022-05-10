#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
import sys
GPIO.setwarnings(False)
reader = SimpleMFRC522()
def read():
    while True:
            id, text = reader.read_no_block()
            return text