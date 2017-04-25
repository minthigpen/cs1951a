#!/usr/bin/env python

from __future__ import division
import sys
import csv
import argparse
from collections import defaultdict

import util

import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from tokenizer import Tokenizer

def load_training_file(file_path):
	art_ = []
	texts = []
	with open(file_path, 'r', encoding='latin1') as file_reader:
		reader = csv.reader(file_reader, delimiter=',', quotechar='"')
		next(reader, None)
		for row in reader:
			sentiment = int(row[2])
			text = row[1]
			art_.append(sentiment)
			texts.append(text)
	return (art_, texts)

def load_input_file(file_path):
	features = []
	locations = []
	times = []
	with open(file_path, 'r', encoding='latin1') as file_reader:		
		reader = csv.reader(file_reader, delimiter=',', quotechar='"')
		next(reader, None)
		for row in reader:
			locations.append(row[0])
			features.append(row[6])
			times.append(row[5])
	return (locations, times, features)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-training', required=True, help='Path to training data')
	parser.add_argument('-input', required=True, help='Input file with features to classify')
	opts = parser.parse_args()

	tokenizer = Tokenizer()
	vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)

	# Load training text and training labels
	(training_labels, training_texts) = load_training_file(opts.training)

	# Get training features using vectorizer
	training_features = vectorizer.fit_transform(training_texts)

	# Transform training labels to numpy array (numpy.array)
	training_labels = numpy.array(training_labels)
	############################################################

	##### TRAIN THE MODEL ######################################
	# Initialize the type of the classifier

	classifier = LinearSVC()

	# Train classifier using 'fit'
	classifier.fit(training_features, training_labels)

	(input_locations, input_times, input_text) = load_input_file(opts.input)
	input_features = vectorizer.transform(input_text)
	predicted_labels = classifier.predict(input_features)

	with open("data/fb_events/ClassifiedNullFacebookEvents.csv", "w") as classified:
		writer = csv.writer(classified)
		writer.writerow(["neighborhood", "time of event", "event description", "art event indicator"])
		for i in range(0, len(predicted_labels)):
			writer.writerow([input_locations[i], input_times[i], input_text[i], predicted_labels[i]])

if __name__ == '__main__':
	main()
