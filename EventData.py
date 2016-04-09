# wrapper of the events. 
class EventData:

	def __init__(self, idx):
		self.idx = idx
		self.images = []

	def setOneImage(self, image_data):
		self.images.append(image_data)

	def setArrayOfImages(self, image_array):
		for image in image_array:
			self.setOneImage(image)

	def getImageArray(self):
		return self.images