import csv

art = ["LECTURE","FESTIVAL_EVENT","CONFERENCE_EVENT","MOVIE_EVENT","DANCE_EVENT","MUSIC_EVENT",
       "ART_EVENT","WORKSHOP","BOOK_EVENT","THEATER_EVENT","COMEDY_EVENT", "OTHER", "CLASS_EVENT", "FAMILY_EVENT", "FUNDRAISER"]

# notArt:["FUNDRAISER", "FITNESS","FAMILY_EVENT","SPORTS_EVENT","MEETUP",
# "DINING_EVENT","FOOD_TASTING","NIGHTLIFE","CLASS_EVENT","OTHER","RELIGIOUS_EVENT","NEIGHBORHOOD","VOLUNTEERING","SHOPPING"]


catIndex = 0
descIndex = 1

desc_set = set()


with open("./data/facebookEventNotNull.csv", "r") as inputF, open("facebookEventTest.csv", "w") as outFTest, open("facebookEventTrain.csv", "w") as outFTrain:
    reader = csv.reader(inputF)
        writerTest = csv.writer(outFTest)
        writerTrain = csv.writer(outFTrain)
        
        count = 0
        
        for row in reader:
            
            if str(row[descIndex]) not in desc_set:
                count += 1
                    desc_set.add(str(row[descIndex]))
                        
                        # if event is art related = 1, else = 0
                        if row[catIndex] in art:
                            if count > 386:
                                
                                writerTest.writerow([row[catIndex], row[descIndex], str(1), row[0]])
                                else:
                                    writerTrain.writerow([row[catIndex], row[descIndex], str(1), row[0]])
                        
                        else: 
                            if count > 386:
                                
                                
                                writerTest.writerow([row[catIndex], row[descIndex], str(0), row[0]])
                                else: 
                                    writerTrain.writerow([row[catIndex], row[descIndex], str(0), row[0]])

