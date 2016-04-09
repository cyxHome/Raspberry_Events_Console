import FirebaseConnector

firebase_url = 'https://event-finder-test.firebaseio.com'

robot_data = {}
robot_data['age'] = 100
robot_data['gender'] = 'female'
robot_data['interest'] = ['None'],
robot_data['myAttendanceNumber'] = 0
robot_data['myPostsNumber'] = 0
robot_data['nickname'] = 'robot'
robot_data['password'] = 'robot'
robot_data['username'] = 'python crawler'
robot_data['usrProfileImage'] = ''
robot_data['whatsup'] = 'nothing up'

if __name__ == '__main__':
	while True:
		print "Welcome to use this crawler to add events to CU Event Finder"
		print "-------------------------------------------------------"
		print "What would you like to do?"
		print "input 1 to add events"
		print "input 2 to delete events"
		print "input 3 to remove all the events"
		print "input 0 to exit"
		num = input("Your choice: ")
		if num == 0:
			quit()
		elif num == 1:
			FirebaseConnector.postEvents(robot_data, firebase_url, tags_list)
		elif num == 2:
			FirebaseConnector.removeRobotPostEvents(firebase_url, robot_data['username'])
		elif num == 3:
			FirebaseConnector.removeAllPostEvents()