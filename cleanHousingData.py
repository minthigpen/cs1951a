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
	# getMedianRentChange(zip_to_subborough)
	getAverageIncomeChange(zip_to_subborough)
	
def getMedianRentChange(zip_to_subborough):	
	medians_by_zip = {}
	with open("data/median rent/median_rent_2011.csv", "r") as median_11:
		median_2011 = csv.reader(median_11)
		next(median_2011, None)
		next(median_2011, None)
		for row in median_2011:
			if row[3] != "-":
				median_rent_temp = row[3].replace("+", "")
				median_rent = median_rent_temp.replace(",", "")
				medians_by_zip[row[1]] = {2011: int(median_rent)}

	with open("data/median rent/median_rent_2012.csv", "r") as median_12:
		median_2012 = csv.reader(median_12)
		next(median_2012, None)
		next(median_2012, None)
		for row in median_2012:
			if row[3] != "-":
				median_rent_temp = row[3].replace("+", "")
				median_rent = median_rent_temp.replace(",", "")
				if row[1] in medians_by_zip:
					medians_by_zip[row[1]][2012] = int(median_rent)

	with open("data/median rent/median_rent_2013.csv", "r") as median_13:
		median_2013 = csv.reader(median_13)
		next(median_2013, None)
		next(median_2013, None)
		for row in median_2013:
			if row[3] != "-":
				median_rent_temp = row[3].replace("+", "")
				median_rent = median_rent_temp.replace(",", "")
				if row[1] in medians_by_zip:
					medians_by_zip[row[1]][2013] = int(median_rent)

	with open("data/median rent/median_rent_2014.csv", "r") as median_14:
		median_2014 = csv.reader(median_14)
		next(median_2014, None)
		next(median_2014, None)
		for row in median_2014:
			if row[3] != "-":
				median_rent_temp = row[3].replace("+", "")
				median_rent = median_rent_temp.replace(",", "")
				if row[1] in medians_by_zip:
					medians_by_zip[row[1]][2014] = int(median_rent)

	with open("data/median rent/median_rent_2015.csv", "r") as median_15:
		median_2015 = csv.reader(median_15)
		next(median_2015, None)
		next(median_2015, None)
		for row in median_2015:
			if row[3] != "-":
				median_rent_temp = row[3].replace("+", "")
				median_rent = median_rent_temp.replace(",", "")
				if row[1] in medians_by_zip:
					medians_by_zip[row[1]][2015] = int(median_rent)

	

	avg_median_rent_by_subborough = {}
	for zipcode in zip_to_subborough:
 		avg_median_rent_by_subborough[zip_to_subborough[zipcode]] = {2011: [], 2012: [], 2013: [], 2014: [], 2015: []}

	for zipcode in medians_by_zip:
 		if zipcode in zip_to_subborough:
	 		subborough = zip_to_subborough[zipcode]
	 		for i in range(2011, 2016):
	 			if i in medians_by_zip[zipcode]:
		 			avg_median_rent_by_subborough[subborough][i].append(medians_by_zip[zipcode][i])

	for subborough in avg_median_rent_by_subborough:
		for i in range(2011, 2016):
			avg_median_rent_by_subborough[subborough][i] = sum(avg_median_rent_by_subborough[subborough][i]) / len(avg_median_rent_by_subborough[subborough][i]) 		

	with open("data/median rent/averageMedianRentChangeBySubborough.csv", "w") as output:
		writer = csv.writer(output)
		writer.writerow(["subborough", "2011", "2012", "2013", "2014", "2015"])
		for subborough in avg_median_rent_by_subborough:
			writer.writerow([subborough, avg_median_rent_by_subborough[subborough][2011], avg_median_rent_by_subborough[subborough][2012], avg_median_rent_by_subborough[subborough][2013], avg_median_rent_by_subborough[subborough][2014], avg_median_rent_by_subborough[subborough][2015]])


def getAverageIncomeChange(zip_to_subborough):
	avg_income_by_subborough = {}
	for zipcode in zip_to_subborough:
 		avg_income_by_subborough[zip_to_subborough[zipcode]] = {2011: [0, 0], 2012: [0, 0], 2013: [0, 0], 2014: [0, 0], 2015: [0, 0]}

	to_exclude = set()
	with open("data/average_income/income_2015.csv", "r") as units_2015:
		with open("data/average_income/aggregate_income_2015.csv", "r") as avg_2015:
			housing_units_2015 = csv.reader(units_2015)
			avg_income_2015 = csv.reader(avg_2015)
			next(housing_units_2015, None)
			next(housing_units_2015, None)
			next(avg_income_2015, None)
			next(avg_income_2015, None)

			for row in avg_income_2015:
				if row[3] == "-":
					to_exclude.add(row[1])
			for row in housing_units_2015:
				if row[3] == "-":
					to_exclude.add(row[1])

	with open("data/average_income/income_2014.csv", "r") as units_2014:
		with open("data/average_income/aggregate_income_2014.csv", "r") as avg_2014:
			housing_units_2014 = csv.reader(units_2014)
			avg_income_2014 = csv.reader(avg_2014)
			next(housing_units_2014, None)
			next(housing_units_2014, None)
			next(avg_income_2014, None)
			next(avg_income_2014, None)

			for row in avg_income_2014:
				if row[3] == "-":
					to_exclude.add(row[1])
			for row in housing_units_2014:
				if row[3] == "-":
					to_exclude.add(row[1])

	with open("data/average_income/income_2013.csv", "r") as units_2013:
		with open("data/average_income/aggregate_income_2013.csv", "r") as avg_2013:
			housing_units_2013 = csv.reader(units_2013)
			avg_income_2013 = csv.reader(avg_2013)
			next(housing_units_2013, None)
			next(housing_units_2013, None)
			next(avg_income_2013, None)
			next(avg_income_2013, None)

			for row in avg_income_2013:
				if row[3] == "-":
					to_exclude.add(row[1])
			for row in housing_units_2013:
				if row[3] == "-":
					to_exclude.add(row[1])

	with open("data/average_income/income_2012.csv", "r") as units_2012:
		with open("data/average_income/aggregate_income_2012.csv", "r") as avg_2012:
			housing_units_2012 = csv.reader(units_2012)
			avg_income_2012 = csv.reader(avg_2012)
			next(housing_units_2012, None)
			next(housing_units_2012, None)
			next(avg_income_2012, None)
			next(avg_income_2012, None)

			for row in avg_income_2012:
				if row[3] == "-":
					to_exclude.add(row[1])
			for row in housing_units_2012:
				if row[3] == "-":
					to_exclude.add(row[1])

	with open("data/average_income/income_2011.csv", "r") as units_2011:
		with open("data/average_income/aggregate_income_2011.csv", "r") as avg_2011:
			housing_units_2011 = csv.reader(units_2011)
			avg_income_2011 = csv.reader(avg_2011)
			next(housing_units_2011, None)
			next(housing_units_2011, None)
			next(avg_income_2011, None)
			next(avg_income_2011, None)

			for row in avg_income_2011:
				if row[3] == "-":
					to_exclude.add(row[1])
			for row in housing_units_2011:
				if row[3] == "-":
					to_exclude.add(row[1])

	with open("data/average_income/income_2015.csv", "r") as units_2015:
		with open("data/average_income/aggregate_income_2015.csv", "r") as avg_2015:
			housing_units_2015 = csv.reader(units_2015)
			avg_income_2015 = csv.reader(avg_2015)
			next(housing_units_2015, None)
			next(housing_units_2015, None)
			next(avg_income_2015, None)
			next(avg_income_2015, None)

			for row in avg_income_2015:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2015][0] += int(row[3])
						
			for row in housing_units_2015:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2015][1] += int(row[3])

	with open("data/average_income/income_2014.csv", "r") as units_2014:
		with open("data/average_income/aggregate_income_2014.csv", "r") as avg_2014:
			housing_units_2014 = csv.reader(units_2014)
			avg_income_2014 = csv.reader(avg_2014)
			next(housing_units_2014, None)
			next(housing_units_2014, None)
			next(avg_income_2014, None)
			next(avg_income_2014, None)

			for row in avg_income_2014:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2014][0] += int(row[3])
						
			for row in housing_units_2014:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2014][1] += int(row[3])

	with open("data/average_income/income_2013.csv", "r") as units_2013:
		with open("data/average_income/aggregate_income_2013.csv", "r") as avg_2013:
			housing_units_2013 = csv.reader(units_2013)
			avg_income_2013 = csv.reader(avg_2013)
			next(housing_units_2013, None)
			next(housing_units_2013, None)
			next(avg_income_2013, None)
			next(avg_income_2013, None)

			for row in avg_income_2013:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2013][0] += int(row[3])
						
			for row in housing_units_2013:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2013][1] += int(row[3])

	with open("data/average_income/income_2012.csv", "r") as units_2012:
		with open("data/average_income/aggregate_income_2012.csv", "r") as avg_2012:
			housing_units_2012 = csv.reader(units_2012)
			avg_income_2012 = csv.reader(avg_2012)
			next(housing_units_2012, None)
			next(housing_units_2012, None)
			next(avg_income_2012, None)
			next(avg_income_2012, None)

			for row in avg_income_2012:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2012][0] += int(row[3])
						
			for row in housing_units_2012:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2012][1] += int(row[3])
			
	with open("data/average_income/income_2011.csv", "r") as units_2011:
		with open("data/average_income/aggregate_income_2011.csv", "r") as avg_2011:
			housing_units_2011 = csv.reader(units_2011)
			avg_income_2011 = csv.reader(avg_2011)
			next(housing_units_2011, None)
			next(housing_units_2011, None)
			next(avg_income_2011, None)
			next(avg_income_2011, None)

			for row in avg_income_2011:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2011][0] += int(row[3])
						
			for row in housing_units_2011:
				if row[1] in zip_to_subborough and row[1] not in to_exclude:
					avg_income_by_subborough[zip_to_subborough[row[1]]][2011][1] += int(row[3])

	for subborough in avg_income_by_subborough:
		for year in avg_income_by_subborough[subborough]:
			avg_income_by_subborough[subborough][year] = avg_income_by_subborough[subborough][year][0] / avg_income_by_subborough[subborough][year][1]

	# print(avg_income_by_subborough)

	with open("data/average_income/averageIncomeBySubborough.csv", "w") as avg_change:
		average_change = csv.writer(avg_change)
		average_change.writerow(["subborough", "2011", "2012", "2013", "2014", "2015"])
		for subborough in avg_income_by_subborough:
			average_change.writerow([subborough, avg_income_by_subborough[subborough][2011], avg_income_by_subborough[subborough][2012], avg_income_by_subborough[subborough][2013], avg_income_by_subborough[subborough][2014], avg_income_by_subborough[subborough][2015]])

if __name__ == '__main__':
	main()