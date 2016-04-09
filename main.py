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

print "Welcome to use raspberry pi event visualizor"
print "-------------------------------------------------------"

########################     Constants     ########################

FIREBASE_ROOT_REF = 'https://event-finder-test.firebaseio.com'
IMG_WIDTH = 640
IMG_HEIGHT = 480
USEREVENT = 0


########################     Global Variables     ########################
screen = 0
cur_event_idx = 0
cur_img_idx = 0
events_arr = []
exit_count = 0

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

def JS_Left_callback(channel):
    print "falling edge detected on Joystick Left"
    global exit_count
    global cur_event_idx
    global events_arr
    exit_count = 0
    length = len(events_arr)
    cur_event_idx += length - 1
    cur_event_idx %= length
    updateDisplayWithUrl()
def JS_Top_callback(channel):
    print "falling edge detected on Joystick Top"
    global exit_count
    exit_count = 0
def JS_Bottom_callback(channel):
    print "falling edge detected on Joystick Bottom"
    global exit_count
    exit_count = 0
def JS_Right_callback(channel):
    print "falling edge detected on Joystick Right"
    global exit_count
    global cur_event_idx
    global events_arr
    exit_count = 0
    length = len(events_arr)
    cur_event_idx += 1
    cur_event_idx %= length
    updateDisplayWithUrl()
def BT_White_callback(channel):
    print "falling edge detected on Button White"
    global exit_count
    exit_count = 0
def BT_Red_callback(channel):
    print "falling edge detected on Button Red"
    global exit_count
    exit_count += 1


#def GPIO16_callback(channel):
#    cmd = 'echo "pause"'
#    subprocess.check_output(cmd, shell=True)


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

def updateDisplayWithUrl():
    global screen
    global events_arr
    global cur_event_idx
    global cur_img_idx
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
    #    GPIO.wait_for_edge(26, GPIO.FALLING)
        if exit_count >= 3:
            break

except KeyboardInterrupt:
    # do nothing
    print "Oops, exception!"

GPIO.cleanup() # clean up GPIO on normal exit













	# print img_str
	# f = open('workfile', 'w')
	# f.write(img_str)

	# print type(img_str)

#	img_str = "https://d3e1o4bcbhmj8g.cloudfront.net/photos/357497/big/0e2feb711243eca3cdbcb830029d6198f2b0212e.jpg"

#	img_str = "https://stackoverflow.com"
# img_str = "http://calligraphyalphabet.org/1234/wp-content/uploads/brush-calligraphy-alphabet-l.jpg"

# while True:

# 	if len(img_str) < 100:
# 		# r = requests.get("")
# 		# file = r.content  # Content of response
# 		file = urllib2.urlopen(img_str).read()
# 		print file
# 		file = cStringIO.StringIO(file)
# 		print file
# 		img = pygame.image.load(file)
# 		img = pygame.transform.scale(img, (w, h))

# 		screen.blit(img,(0,0))
# 		pygame.display.flip() # update the display
# 		c.tick(300)

	#everything below this line should be in your main loop
	# for event in pygame.event.get():
	# 	if event.type == USEREVENT+1:
	# 		cur_img_idx += 1
	# 		cur_img_idx %= len(cur_events_images_arr)
	# 	elif event.type == USEREVENT+2:
	# 		cur_event_idx += 1
	# 		cur_event_idx %= len(events_arr)

