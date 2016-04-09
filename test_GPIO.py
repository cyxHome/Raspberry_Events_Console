import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
# Joystick
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Buttons
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def GPIO_5_callback(channel):
    print "falling edge detected on 5"
def GPIO_6_callback(channel):
    print "falling edge detected on 6"
def GPIO_13_callback(channel):
    print "falling edge detected on 13"
def GPIO_19_callback(channel):
    print "falling edge detected on 19"
def GPIO_16_callback(channel):
    print "falling edge detected on 16"
def GPIO_26_callback(channel):
    print "falling edge detected on 26"

#def GPIO16_callback(channel):
#    cmd = 'echo "pause"'
#    subprocess.check_output(cmd, shell=True)

# "main" part of the program
# Joystick

GPIO.add_event_detect(5, GPIO.FALLING, callback=GPIO_5_callback, bouncetime=300)
GPIO.add_event_detect(6, GPIO.FALLING, callback=GPIO_6_callback, bouncetime=300)
GPIO.add_event_detect(13, GPIO.FALLING, callback=GPIO_13_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=GPIO_19_callback, bouncetime=300)
# Buttons
GPIO.add_event_detect(16, GPIO.FALLING, callback=GPIO_16_callback, bouncetime=300)
#GPIO.add_event_detect(26, GPIO.FALLING, callback=GPIO_26_callback, bouncetime=300)

try:
    print "Waiting for falling edge on port 26"
    GPIO.wait_for_edge(26, GPIO.FALLING)
    print "Falling edge detected on port 26"
except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit

GPIO.cleanup() # clean up GPIO on normal exit
