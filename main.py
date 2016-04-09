#!/usr/bin/python
import sys
import pygame
import time
import re
import urllib2
import cStringIO
import base64
# import FirebaseConnector

firebase_url = 'https://event-finder-test.firebaseio.com'

import requests


if __name__ == '__main__':
	print "Welcome to use raspberry pi event visualizor"
	print "-------------------------------------------------------"


	pygame.init()



	USEREVENT = 0


	w = 640
	h = 480
	size=(w,h)
	screen = pygame.display.set_mode(size)
	c = pygame.time.Clock() # create a clock object for timing
	pygame.time.set_timer(USEREVENT+1, 1000)  #1 second
	pygame.time.set_timer(USEREVENT+2, 5000)  #5 seconds 

	events_arr = []
#	FirebaseConnector.packEventsToEventsData(events_arr, firebase_url)

#	cur_event_idx = 0
#	cur_img_idx = 0

#	cur_events_images_arr = events_arr[cur_event_idx].getImageArray()
#	img_str = cur_events_images_arr[cur_img_idx]
	# print img_str
	# f = open('workfile', 'w')
	# f.write(img_str)

	# print type(img_str)

#	img_str = "https://d3e1o4bcbhmj8g.cloudfront.net/photos/357497/big/0e2feb711243eca3cdbcb830029d6198f2b0212e.jpg"

#	img_str = "https://stackoverflow.com"
	img_str = "http://calligraphyalphabet.org/1234/wp-content/uploads/brush-calligraphy-alphabet-l.jpg"

	while True:

		if len(img_str) < 100:
			# r = requests.get("") 
			# file = r.content  # Content of response
			file = urllib2.urlopen(img_str).read()
			print file
			file = cStringIO.StringIO(file)
			print file
			img = pygame.image.load(file)
			img = pygame.transform.scale(img, (w, h))

			screen.blit(img,(0,0))
			pygame.display.flip() # update the display
			c.tick(300)
		
		#everything below this line should be in your main loop
		# for event in pygame.event.get():
		# 	if event.type == USEREVENT+1:
		# 		cur_img_idx += 1 
		# 		cur_img_idx %= len(cur_events_images_arr)
		# 	elif event.type == USEREVENT+2:
		# 		cur_event_idx += 1
		# 		cur_event_idx %= len(events_arr)
				
