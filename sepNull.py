import csv

with open("./data/FullFacebookEvents.csv", "r") as inputF,  open("data/facebookEventNull.csv", "w") as outputF1, open("data/facebookEventNotNull.csv", "w") as outputF2:

	catIndex = 4

	reader = csv.reader(inputF)
	writerNull = csv.writer(outputF1)
	writerNNull = csv.writer(outputF2)

	for row in reader:

		# format of rows in FullFacebokEvents is 
		# Neighborhood	Borough		Event_ID	Event_Name	Event_Category	Event_Start	Event_Description

		if row[catIndex] == 'null':

			# this will be the file to be used with ML to classify
			writerNull.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])


		else:
			# have the not null event categories be in this format
			# neighborhood	time of event	event description	art event indicator

			art = ["LECTURE","FESTIVAL_EVENT","CONFERENCE_EVENT","MOVIE_EVENT","DANCE_EVENT","MUSIC_EVENT",
			"ART_EVENT","WORKSHOP","BOOK_EVENT","THEATER_EVENT","COMEDY_EVENT"]

			if str(row [catIndex]) in art:
				# if the category is not null, we either categorize as 0 (not art related) or 1 (art-related)
				writerNNull.writerow([row[0], row[5], row[6], str(1),row[4]])

			else:
				writerNNull.writerow([row[0], row[5], row[6], str(0),row[4]])




