import EventsCollector
from EventData import *


def packEventsToEventsData(events_arr, firebase_url):
	from firebase import firebase
	firebase = firebase.FirebaseApplication(firebase_url, None)
	events = firebase.get('/events', None)

	idx = 0

	if events is not None and len(events) > 0:
		for event in events.values():
			tmp = EventData(idx)
			idx += 1
			tmp.setArrayOfImages(event["imageOfEvent"])
			events_arr.append(tmp)
