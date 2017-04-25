#!/usr/bin/env python

import csv
import argparse
import re

def main():
	zip_to_subborough = {}
	with open("data/districtLocationInfo2.csv", "r") as district_info:
		reader = csv.reader(district_info)
		next(reader, None)
		for row in reader:
			zipcodes = row[2].split(", ")
			for zipcode in zipcodes:
				zip_to_subborough[zipcode] = row[0]
	getProportionArtEvents(zip_to_subborough)

def getProportionArtEvents(zip_to_subborough):

	proportion_art_events_by_subborough = {}
	for subborough in zip_to_subborough.values():
		proportion_art_events_by_subborough[subborough] = {2011: [0, 0], 2012: [0, 0], 2013: [0, 0], 2014: [0, 0], 2015: [0, 0]}

	with open("data/fb_events/classifiedFacebookEvents.csv", "r") as events:
		reader = csv.reader(events)
		next(reader, None)
		for row in reader:
			year = int(row[1].split("-")[0])
			if row[0] in zip_to_subborough.values():
				if(2011 <= year <= 2015):
					proportion_art_events_by_subborough[row[0]][year][1] += 1
					if row[3] == "1":
						proportion_art_events_by_subborough[row[0]][year][0] += 1

	for subborough in proportion_art_events_by_subborough:
		for year in proportion_art_events_by_subborough[subborough]:
			if proportion_art_events_by_subborough[subborough][year][1] == 0:
				proportion_art_events_by_subborough[subborough][year] = 0
			else:
				proportion_art_events_by_subborough[subborough][year] = proportion_art_events_by_subborough[subborough][year][0] / proportion_art_events_by_subborough[subborough][year][1]

	print(proportion_art_events_by_subborough)

	with open("data/fb_events/changeInFacebookEvents.csv", "w") as events:
		writer = csv.writer(events)
		writer.writerow(["subborough", "2011", "2012", "2013", "2014", "2015"])
		for subborough in proportion_art_events_by_subborough:
			writer.writerow([subborough, proportion_art_events_by_subborough[subborough][2011], proportion_art_events_by_subborough[subborough][2012], proportion_art_events_by_subborough[subborough][2013], proportion_art_events_by_subborough[subborough][2014], proportion_art_events_by_subborough[subborough][2015]])


if __name__ == '__main__':
	main()