# wrapper of the events. 
class EventData:

	def __init__(self, idx):
		self.idx = idx
		self.images = []

	## Setters ##
	def setOneImage(self, image_data):
		self.images.append(image_data)

	def setArrayOfImages(self, image_array):
		for image in image_array:
			self.setOneImage(image)

	def setTitle(self, title):
		self.title = title

	def setDescription(self, description):
		self.description = description

	def setTime(self, time):
		self.time = self.preprocessTime(time)

	def setLocation(self, location):
		self.location = location

	## Getters ##
	def getImageArray(self):
		return self.images

	def getTitle(self):
		return self.title

	def getDescription(self):
		return self.description

	def getTime(self):
		return self.time

	def getLocation(self):
		return self.location

	## Helpers ##
	def preprocessTime(self, time):
		""" From 201602021310 To 'Time: 02/02/2016 13:10' """
		str_time = str(time)
		return ("Time: %s/%s/%s %s:%s" % (str_time[4:6], str_time[6:8], 
			str_time[0:4], str_time[8:10], str_time[10:12]))












