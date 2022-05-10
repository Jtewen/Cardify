#!/usr/bin/env python
 
import webbrowser
import RPi.GPIO as GPIO
from time import sleep
from mfrc522 import SimpleMFRC522
import sys
 
GPIO.setwarnings(False)
 
reader = SimpleMFRC522()

 
try:
 while True:
 	print("Hold a tag near the reader")
 	id, text = reader.read()
 	webbrowser.open(text)
 	print()
 
 
except KeyboardInterrupt:
 GPIO.cleanup()
 raise