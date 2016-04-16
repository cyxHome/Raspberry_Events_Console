#!/usr/bin/python
import sys
import pygame
import time
import re
import urllib2
import cStringIO
import base64
import FirebaseConnector
import RPi.GPIO as GPIO
import subprocess
import requests


########################     Constants     ########################
FIREBASE_ROOT_REF = 'https://event-finder-test.firebaseio.com'
IMG_WIDTH = 640
IMG_HEIGHT = 480
USEREVENT = 0

########################     Global Variables     ########################
screen = None
cur_event_idx = 0
cur_img_idx = 0
events_arr = []
# need_update_display_count
need_update_display_count = 0

def updateDisplayWithUrl():
    global screen
    global events_arr
    global cur_event_idx
    global cur_img_idx
    global events_arr
    print "cur_event_idx", cur_event_idx
    print "cur_img_idx", cur_img_idx
    cur_events_images_arr = events_arr[cur_event_idx].getImageArray()
    img_str = cur_events_images_arr[cur_img_idx]
    print "img_str", img_str
    file = urllib2.urlopen(img_str).read()
    file = cStringIO.StringIO(file)
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, (IMG_WIDTH, IMG_HEIGHT))
    screen.blit(img,(0,0))
    pygame.display.flip() # update the display

def JS_Left_callback(channel):
    print "falling edge detected on Joystick Left"
    global cur_event_idx
    global events_arr
    global events_arr
    global need_update_display_count
    length = len(events_arr)
    cur_event_idx += length - 1
    cur_event_idx %= length
    need_update_display_count += 1

def JS_Top_callback(channel):
    print "falling edge detected on Joystick Top"

def JS_Bottom_callback(channel):
    print "falling edge detected on Joystick Bottom"

def JS_Right_callback(channel):
    print "falling edge detected on Joystick Right"
    global cur_event_idx
    global events_arr
    global need_update_display_count
    length = len(events_arr)
    cur_event_idx += 1
    cur_event_idx %= length
    need_update_display_count += 1

def BT_White_callback(channel):
    print "falling edge detected on Button White"

def BT_Red_callback(channel):
    print "falling edge detected on Button Red"

if __name__ == '__main__':

    print "Welcome to use raspberry pi event visualizor"
    print "-------------------------------------------------------"

    ########################     GPIO Setup     ########################

    GPIO.setmode(GPIO.BCM)
    # Joystick
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Buttons
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Joystick Left
    GPIO.add_event_detect(5, GPIO.FALLING, callback=JS_Left_callback, bouncetime=300)
    # Joystick Top
    GPIO.add_event_detect(6, GPIO.FALLING, callback=JS_Top_callback, bouncetime=300)
    # Joystick Bottom
    GPIO.add_event_detect(13, GPIO.FALLING, callback=JS_Bottom_callback, bouncetime=300)
    # Joystick Right
    GPIO.add_event_detect(19, GPIO.FALLING, callback=JS_Right_callback, bouncetime=300)
    # White
    GPIO.add_event_detect(16, GPIO.FALLING, callback=BT_White_callback, bouncetime=300)
    # Red
    GPIO.add_event_detect(26, GPIO.FALLING, callback=BT_Red_callback, bouncetime=300)

    try:
        print "Press Red Button Continuously For Three Times To Exit"
        pygame.init()
        size=(IMG_WIDTH, IMG_HEIGHT)
        screen = pygame.display.set_mode(size)
    	# c = pygame.time.Clock() # create a clock object for timing
    	# pygame.time.set_timer(USEREVENT+1, 1000)  #1 second
    	# pygame.time.set_timer(USEREVENT+2, 5000)  #5 seconds
        FirebaseConnector.packEventsToEventsData(events_arr, FIREBASE_ROOT_REF)
        print events_arr

        updateDisplayWithUrl()
        
    	# wait for 3 continuous red button pressed to exit the program.
        while True:
            if need_update_display_count > 0:
                print "update with cur_event_idx = %s" % cur_event_idx
                updateDisplayWithUrl()
                need_update_display_count -= 1


    except KeyboardInterrupt:
        # do nothing
        print "Oops, exception!"

    GPIO.cleanup() # clean up GPIO on normal exit


