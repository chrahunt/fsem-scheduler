import app


def sortStudents():
	#iniitialize variables to be used
	numStudents = len(students)
	numCourses = len(courses)
	notSorted = True 
	earliestTime = getTimeSubmitted(students[0]):
	n = 0
	x = 0
	i = 0
	arraylocation = 0
	#first while loop that will continue until all students have been
	#sorted into a class
	while(numStudents > 0):
		#first loop through the students array and find the 
		#earliest submission time, save the array location
	    for i in range(numStudents):
		    if earliestTime > students[i].getTimeSubmitted():
			    earliestTime = students[i].getTimeSubmitted()
			    studentArrayLocation = i
		#loop through while the student is unplaced
		#get student preferences from saved array location
	    while(notSorted == True):
		    studentPref = getPreferences(students[studentArrayLocation])
		    #loop through the courses array and compare student pref 
		    #at n and each course name, save the array location 
		    for x in range(numCourses):
			    if studentPref[n] == courses[x].getName():
				    courseArrayLocation = x
			#if have looped through all 3 preferences
			if n > 3:
		        #add to unplaced students array
		        notSorted = False
		        numStudents = numStudents - 1
			#check if first pref is full, if yes increment n
		    if courses[courseArrayLocation].isFull() == True:
		        n = n + 1
		    else:
		        courses[arraylocation].addStudent()
		        """here is where i'd like to delete the student object from
		        the array after its been placed but i'm unsure how to do it
		        I could also just set the time submitted value to a
		        high number so it will skip it in the next loop"""
		        notSorted = False
		        numStudents = numStudents - 1






