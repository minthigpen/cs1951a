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
	getMedianRentChange(zip_to_subborough)
	getAverageIncomeChange(zip_to_subborough)
	
def getMedianRentChange(zip_to_subborough):	
	change_by_zip = {}
	with open("data/median rent/median_rent_2015.csv", "r") as median_15:
		median_2015 = csv.reader(median_15)
		next(median_2015, None)
		next(median_2015, None)
		for row in median_2015:
			if row[3] != "-":
				median_rent_temp = row[3].replace("+", "")
				median_rent = median_rent_temp.replace("+", "")
				change_by_zip[row[1]] = int(median_rent)

	with open("data/median rent/median_rent_2011.csv", "r") as median_11:
		median_2011 = csv.reader(median_11)
		next(median_2011, None)
		next(median_2011, None)
		for row in median_2011:
			if row[3] != "-":
				median_rent_temp = row[3].replace("+", "")
				median_rent = median_rent_temp.replace(",", "")
				if row[1] in change_by_zip:
					absolute_change = change_by_zip[row[1]] - int(median_rent)
					change_by_zip[row[1]] = absolute_change / int(median_rent) 

	median_rent_by_subborough = {}
	for zipcode in zip_to_subborough:
 		median_rent_by_subborough[zip_to_subborough[zipcode]] = [0, 0]

	for zipcode in change_by_zip:
 		if zipcode in zip_to_subborough:
	 		subborough = zip_to_subborough[zipcode]
	 		median_rent_by_subborough[subborough][0] += change_by_zip[zipcode]
	 		median_rent_by_subborough[subborough][1] += 1

	with open("data/median rent/averageMedianRentChangeBySubborough.csv", "w") as output:
		writer = csv.writer(output)
		writer.writerow(["subborough", "2011-2015 average change in median rent price"])
		for subborough in median_rent_by_subborough:
			writer.writerow([subborough, str(median_rent_by_subborough[subborough][0] / median_rent_by_subborough[subborough][1])])


def getAverageIncomeChange(zip_to_subborough):
	avg_income_by_subborough_2015 = {}
	for zipcode in zip_to_subborough:
 		avg_income_by_subborough_2015[zip_to_subborough[zipcode]] = [0, 0]

	to_exclude = []	
	with open("data/average income/income_2015.csv", "r") as units_2015:
		with open("data/average income/aggregate_income_2015.csv", "r") as avg_2015:
			housing_units_2015 = csv.reader(units_2015)
			avg_income_2015 = csv.reader(avg_2015)
			next(housing_units_2015, None)
			next(housing_units_2015, None)
			next(avg_income_2015, None)
			next(avg_income_2015, None)

			for row in avg_income_2015:
				if row[3] == "-":
					to_exclude.append(row[1])
			for row in housing_units_2015:
				if row[3] == "-":
					to_exclude.append(row[1])

	with open("data/average income/income_2015.csv", "r") as units_2015:
		with open("data/average income/aggregate_income_2015.csv", "r") as avg_2015:
			housing_units_2015 = csv.reader(units_2015)
			avg_income_2015 = csv.reader(avg_2015)
			next(housing_units_2015, None)
			next(housing_units_2015, None)
			next(avg_income_2015, None)
			next(avg_income_2015, None)

			for row in avg_income_2015:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough_2015[zip_to_subborough[row[1]]][0] += int(row[3])
						
			for row in housing_units_2015:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough_2015[zip_to_subborough[row[1]]][1] += int(row[3])
			

	for subborough in avg_income_by_subborough_2015:
		avg_income_by_subborough_2015[subborough] = avg_income_by_subborough_2015[subborough][0] / avg_income_by_subborough_2015[subborough][1]

	avg_income_by_subborough_2011 = {}
	for zipcode in zip_to_subborough:
 		avg_income_by_subborough_2011[zip_to_subborough[zipcode]] = [0, 0]

	to_exclude = []	
	with open("data/average income/income_2011.csv", "r") as units_2011:
		with open("data/average income/aggregate_income_2011.csv", "r") as avg_2011:
			housing_units_2011 = csv.reader(units_2011)
			avg_income_2011 = csv.reader(avg_2011)
			next(housing_units_2011, None)
			next(housing_units_2011, None)
			next(avg_income_2011, None)
			next(avg_income_2011, None)

			for row in avg_income_2011:
				if row[3] == "-":
					to_exclude.append(row[1])
			for row in housing_units_2011:
				if row[3] == "-":
					to_exclude.append(row[1])

	with open("data/average income/income_2011.csv", "r") as units_2011:
		with open("data/average income/aggregate_income_2011.csv", "r") as avg_2011:
			housing_units_2011 = csv.reader(units_2011)
			avg_income_2011 = csv.reader(avg_2011)
			next(housing_units_2011, None)
			next(housing_units_2011, None)
			next(avg_income_2011, None)
			next(avg_income_2011, None)

			for row in avg_income_2011:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough_2011[zip_to_subborough[row[1]]][0] += int(row[3])
						
			for row in housing_units_2011:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough_2011[zip_to_subborough[row[1]]][1] += int(row[3])
			

	for subborough in avg_income_by_subborough_2011:
		avg_income_by_subborough_2011[subborough] = avg_income_by_subborough_2011[subborough][0] / avg_income_by_subborough_2011[subborough][1]

	avg_income_change_by_subborough = {}
	for subborough in avg_income_by_subborough_2015:
		if subborough in avg_income_by_subborough_2011:
			avg_income_change_by_subborough[subborough] = (avg_income_by_subborough_2015[subborough] - avg_income_by_subborough_2011[subborough]) / avg_income_by_subborough_2011[subborough]

	with open("data/average income/averageIncomeChangeBySubborough.csv", "w") as avg_change:
		average_change = csv.writer(avg_change)
		average_change.writerow(["subborough", "2011-2015 change in average income"])
		for subborough in avg_income_change_by_subborough:
			average_change.writerow([subborough, avg_income_change_by_subborough[subborough]])

if __name__ == '__main__':
	main()