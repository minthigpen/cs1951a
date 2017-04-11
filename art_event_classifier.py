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



def load_file(file_path):
	art_ = []
	texts = []
	with open(file_path, 'r', encoding='latin1') as file_reader:
		reader = csv.reader(file_reader, delimiter=',', quotechar='"')
		for row in reader:
			sentiment = int(row[2])
			text = row[1]
			art_.append(sentiment)
			texts.append(text)
	return (art_, texts)

def main():
	##### DO NOT MODIFY THESE OPTIONS ##########################
	parser = argparse.ArgumentParser()
	parser.add_argument('-training', required=True, help='Path to training data')
	parser.add_argument('-test', help='Path to test data')
	parser.add_argument('-c', '--classifier', default='nb', help='nb | log | svm')
	parser.add_argument('-top', type=int, help='Number of top features to show')
	parser.add_argument('-p', type=bool, default='', help='If true, prints out information')
	opts = parser.parse_args()
	############################################################
	# Note: anytime the print flag is set to '', you should not print anything out! this includes the placeholder print statements - either remove those or include them only when the print flag is set to true.

	##### BUILD TRAINING SET ###################################
	# Initialize CountVectorizer
	# You will need to make a change in tokenizer.py
	tokenizer = Tokenizer()
	vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)

	# Load training text and training labels
	(training_labels, training_texts) = load_file(opts.training)

	# Get training features using vectorizer
	training_features = vectorizer.fit_transform(training_texts)

	# Transform training labels to numpy array (numpy.array)
	training_labels = numpy.array(training_labels)
	############################################################

	##### TRAIN THE MODEL ######################################
	# Initialize the corresponding type of the classifier
	# NOTE: Be sure to name the variable for your classifier "classifier" so that our stencil works for you!
	if opts.classifier == 'nb':
		# TODO: Initialize Naive Bayes
		classifier = BernoulliNB(binarize=None)
	elif opts.classifier == 'log':
		# TODO: Initialize Logistic Regression
		classifier = LogisticRegression()
	elif opts.classifier == 'svm':
		# TODO: Initialize SVM
		classifier = LinearSVC()
	else:
		raise Exception('Unrecognized classifier!')

	# TODO: Train your classifier using 'fit'
	classifier.fit(training_features, training_labels)

	############################################################


	###### VALIDATE THE MODEL ##################################
	# TODO: Print training mean accuracy using 'score'
	s = classifier.score(training_features,training_labels)
	if opts.p:
		print('training mean accuracy:')
		print(s)
	# TODO: Perform 10 fold cross validation (cross_val_score) with scoring='accuracy'
	cv = cross_val_score(classifier, training_features, training_labels, scoring='accuracy', cv=10)
	mean = numpy.mean(cv)
	std = numpy.std(cv)
	# TODO: Print the mean and std deviation of the cross validation score
	if opts.p:
		print('mean and std dev for cross validation scores:')
		print (mean)
		print (std)

	############################################################

	##### EXAMINE THE MODEL ####################################
	if opts.top is not None:
		# Print top n most informative features for positive and negative classes
		if opts.p:
			print('most informative features:')
			util.print_most_informative_features(opts.classifier, vectorizer, classifier, opts.top)
	############################################################


	##### TEST THE MODEL #######################################
	if opts.test is None:
		pass

	else:
		# Test the classifier on the given test set
		# TODO: Load test labels and texts using load_file()
		(test_labels, test_text) = load_file(opts.test)
		# TODO: Extract test features using vectorizer.transform()
		test_feat = vectorizer.transform(test_text)
		if opts.p:
			# TODO: Predict the labels for the test set
			print('predicted label for test tweets:')

		predicted_labels = classifier.predict(test_feat)
		actual_labels = test_labels
		score = classifier.score(test_feat,test_labels)

		if opts.p:
			print(predicted_labels)

			# TODO: Print mean test accuracy
			print('predicted mean accuracy:')
			print(score)

			# TODO: Print the confusion matrix using your implementation
			print('our confusion matrix:')

		# if actual class is 1 and pred class is 1
		TP = 0
		# if actual class is 0 and pred class is 0
		TN = 0
		# if actual class is 0 and pred class is 1
		FP = 0
		# if actual class is 1 and pred class is 0
		FN = 0

		for i in range(len(predicted_labels)):
			# True
			if predicted_labels[i] == actual_labels[i]:
				if predicted_labels[i] == 1 and actual_labels[i] == 1:
					TP += 1
				else:
					TN += 1
			# False
			elif predicted_labels[i] != actual_labels[i]:
				if predicted_labels[i] == 0:
					FN += 1
				else: 
					FP += 1

		conf_matrix = [[TN, FP],[FN,TP]]
		sk_matrix = confusion_matrix(actual_labels, predicted_labels)

		if opts.p:
			print (sk_matrix)



	############################################################


if __name__ == '__main__':
	main()
