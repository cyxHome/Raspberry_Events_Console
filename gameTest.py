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
import textwrap
import newBallGame
import threading
import time

# http://pygame.org/wiki/TextWrapping?parent=
from itertools import chain

def truncline(text, font, maxwidth):
    real=len(text)
    stext=text
    l=font.size(text)[0]
    cut=0
    a=0
    done=1
    old = None
    while l > maxwidth:
        a=a+1
        n=text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext= n[:-cut]
        else:
            stext = n
        l=font.size(stext)[0]
        real=len(stext)
        done=0
    return real, done, stext

def wrapline(text, font, maxwidth):
    done=0
    wrapped=[]

    while not done:
        nl, done, stext=truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text=text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


########################     Constants     ########################
FIREBASE_ROOT_REF = 'https://event-finder-test.firebaseio.com'
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 800
IMG_WIDTH = 640
IMG_HEIGHT = 480
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 500
USEREVENT = 0
STEPY = 1
STEP_GAME = 1
STEPY_THRESHOLD = 10
STEP_THRESHOLD_GAME = 1
########################     Global Variables     ########################
screen = None
up = True
step_counter = 0
step_counter_game = 0
buffer_surface = None
cur_event_idx = 0
cur_img_idx = 0
events_arr = []
posX = 0
posY = 100
direction = -1
# need_update_display_count
need_update_display_count = 0
# whether we are playing game or viewing events now
is_game_mode = False
console = None

def addTextToSurfaceMiddleAlign(surface, text, starting_y, font_size):
    """ Adding title into the buffer surface.
    Return the ending y location of the text box.
    """
    font = pygame.font.SysFont("Arial", font_size)
    lines = wrap_multi_line(text, font, SCREEN_WIDTH)
    print lines
    print "split into %s lines" % str(len(lines))
    tmp = starting_y
    for line in lines:
        print tmp
        text = font.render(line, True, [0,255,255])
        text_width = text.get_rect().width
        surface.blit(text, [(SCREEN_WIDTH - text_width) / 2, tmp])
        tmp += text.get_rect().height
    return tmp

def addTitleToSurfaceMiddleAlign(surface, title, starting_y):
    """ Adding title into the buffer surface.
    Return the ending y location of the text box.
    """
    return addTextToSurfaceMiddleAlign(surface, title, starting_y, 25)

def addTimeAndLocationToSurfaceMiddleAlign(surface, time, location, starting_y):
    """ Adding time and location into the buffer surface.
    Return the ending y location of the text box.
    """
    tmp = addTextToSurfaceMiddleAlign(surface, location, starting_y, 18)
    return addTextToSurfaceMiddleAlign(surface, time, tmp, 18)

def addDescriptionToSurfaceMiddleAlign(surface, description, starting_y):
    """ Adding description into the buffer surface.
    Return the ending y location of the text box.
    """
    return addTextToSurfaceMiddleAlign(surface, description, starting_y, 20)

def addImageToSurfaceMiddleAlign(surface, starting_y):
    """ Adding time and location into the buffer surface.
    Return the ending y location of the text box.
    """
    global events_arr
    global cur_event_idx
    global cur_img_idx
    cur_events_images_arr = events_arr[cur_event_idx].getImageArray()
    img_str = cur_events_images_arr[cur_img_idx]
    print "img_str", img_str
    file = urllib2.urlopen(img_str).read()
    file = cStringIO.StringIO(file)
    img = pygame.image.load(file)
    img = pygame.transform.scale(img, (IMG_WIDTH, IMG_HEIGHT))
    surface.blit(img,((SCREEN_WIDTH - IMG_WIDTH) / 2, starting_y))
    return starting_y + IMG_HEIGHT

def updateDisplay():
    global buffer_surface
    global posX
    global posY
    screen.fill((0,0,0))
    if posY < 0:
        posY = 0
    if posY > SCREEN_HEIGHT - DISPLAY_HEIGHT:
        posY = SCREEN_HEIGHT - DISPLAY_HEIGHT
    screen.blit(buffer_surface.subsurface(posX,posY,DISPLAY_WIDTH,DISPLAY_HEIGHT),(0,0))
    pygame.display.flip() # update the display


def updateDisplayBuffer():
    global buffer_surface
    global events_arr
    global cur_event_idx
    print "cur_event_idx", cur_event_idx
    print "cur_img_idx", cur_img_idx
    buffer_surface.fill((0,0,0))
    next_y = addTitleToSurfaceMiddleAlign(buffer_surface, events_arr[cur_event_idx].getTitle(), 0)
    next_y = addTimeAndLocationToSurfaceMiddleAlign(buffer_surface, events_arr[cur_event_idx].getTime(),
                                                    events_arr[cur_event_idx].getLocation(), next_y)
    next_y = addImageToSurfaceMiddleAlign(buffer_surface, next_y)
    addDescriptionToSurfaceMiddleAlign(buffer_surface, events_arr[cur_event_idx].getDescription(), next_y)

def JS_Left_callback(channel):
    global events_arr
    if len(events_arr) == 0:
        return
    print "falling edge detected on Joystick Left"
    global cur_event_idx
    global events_arr
    global need_update_display_count
    global step_counter_game
    global direction
    if is_game_mode:
        direction = 2
    else:
        length = len(events_arr)
        cur_event_idx += length - 1
        cur_event_idx %= length
        need_update_display_count += 1

def JS_Top_callback(channel):
    global events_arr
    if len(events_arr) == 0:
        return
    print "falling edge detected on Joystick Top"
    global posY
    global step_counter
    global up
    global step_counter_game
    global direction
    if is_game_mode:
        direction = 0
    else:
        up = True
        while GPIO.input(channel) == GPIO.LOW:
            print "Top is low..."
            step_counter += STEPY

def JS_Bottom_callback(channel):
    global events_arr
    if len(events_arr) == 0:
        return
    print "falling edge detected on Joystick Bottom"
    global posY
    global step_counter
    global up
    global step_counter_game
    global direction
    if is_game_mode:
        direction = 1
    else:
        up = False
        while GPIO.input(channel) == GPIO.LOW:
            print "Bottom is low..."
            step_counter += STEPY

def JS_Right_callback(channel):
    global events_arr
    if len(events_arr) == 0:
        return
    print "falling edge detected on Joystick Right"
    global cur_event_idx
    global events_arr
    global need_update_display_count
    global step_counter_game
    global direction
    if is_game_mode:
        direction = 3
    else:
        length = len(events_arr)
        cur_event_idx += 1
        cur_event_idx %= length
        need_update_display_count += 1

def BT_White_callback(channel):
    print "falling edge detected on Button White, Start playing game"
    global is_game_mode
    global console
    if not is_game_mode:
        is_game_mode = True
        console = newBallGame.Console(pygame, buffer_surface, screen)

def BT_Red_callback(channel):
    print "falling edge detected on Button Red, Game stop"
    global is_game_mode
    if is_game_mode:
        is_game_mode = False
        console = None

def keepRefreshingEventList():
    global events_arr
    print "refresh event"
    events_arr = []
    FirebaseConnector.packEventsToEventsData(events_arr, FIREBASE_ROOT_REF)
    print events_arr
    threading.Timer(31, keepRefreshingEventList).start()

def keepChangingEvents():
    global cur_event_idx
    global need_update_display_count
    if len(events_arr) == 0:
        return
    print "change event"
    length = len(events_arr)
    cur_event_idx += 1
    cur_event_idx %= length
    need_update_display_count += 1
    threading.Timer(10, keepChangingEvents).start()


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
        size=(SCREEN_WIDTH, SCREEN_HEIGHT)
        screen = pygame.display.set_mode(size)
        buffer_surface = pygame.Surface(size)
    	# c = pygame.time.Clock() # create a clock object for timing
    	# pygame.time.set_timer(USEREVENT+1, 1000)  #1 second
    	# pygame.time.set_timer(USEREVENT+2, 5000)  #5 seconds
        keepRefreshingEventList()
        keepChangingEvents()

        if len(events_arr) > 0:
            updateDisplayBuffer()
            updateDisplay()

    	# wait for 3 continuous red button pressed to exit the program.
        while True:
            if len(events_arr) == 0:
                buffer_surface.fill((0,0,0))
                updateDisplay()
                time.sleep(5)
            if is_game_mode and console is not None:
                print "move smile " + str(direction)    
                if direction == 0:
                    console.move_up_event(direction)
                elif direction == 1:
                    console.move_down_event(direction)
                elif direction == 2:
                    console.move_left_event(direction)
                elif direction == 3:
                    console.move_right_event(direction)
                if console.done:
                    is_game_mode = False
                    continue
                console.update_all()
            else:
                if step_counter >= STEPY_THRESHOLD:
                    step_counter = 0
                    if up:
                        posY -= STEPY_THRESHOLD
                    else:
                        posY += STEPY_THRESHOLD
                    print "posY now is %d" % posY
                    updateDisplay()
                #print "this is while loop"
                if need_update_display_count > 0:
                    posX = 0
                    posY = 100
                    updateDisplayBuffer()
                    updateDisplay()
                    need_update_display_count -= 1

    except KeyboardInterrupt:
        # do nothing
        print "Oops, exception!"

    GPIO.cleanup() # clean up GPIO on normal exit


