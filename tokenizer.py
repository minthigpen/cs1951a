from porter_stemmer import PorterStemmer
import re
import string
from stop_words import get_stop_words

stop = get_stop_words('english')

class Tokenizer(object):
    def __init__(self):
        self.stemmer = PorterStemmer()

    # only admit non-number with length>2
    def qualify(self, word):
        return len(word)>2 and not word.isdigit()

    def process_desc(self, desc):

        ndesc = []

        for word in desc.split():

            # lowercase all characters
            word = word.lower()
            # replace words with hashtags with just the words
            if word[0] == "#":
                word = word[1:]
            # replace words with @ with "AT_USER"
            elif word[0] == "@":
                word = "AT_USER"
            # replace words with url beginnings with "URL"
            elif len(word) > 4:
                if word[:4] == "www." :
                    word = "URL"
            elif len(word) > 10:
                if word[:10] == "http(s)://":
                    word = "URL"        
            # strip punctuation using translate string method
            translator = str.maketrans('', '', string.punctuation)
            word = word.translate(translator)

            # use stop words list to filter out low value words
            if word not in stop:
                # ignore words that are one letter long
                if len(word) > 1:
                    # check to see if the first letter of the word is an alphabetic character
                    if word[0].isalpha() == True:
                        
                        # finally check for duplicates
                        if word not in ndesc:
                            ndesc.append(word)


        return ' '.join(ndesc)

    def __call__(self, desc):
        # This function takes in a single desc (just the text part)
        # then it will process/clean the desc and return a list of tokens (words).
        # For example, if desc was 'I eat', the function returns ['i', 'eat']

        # You will not need to call this function explictly.
        # Once you initialize your vectorizer with this tokenizer,
        # then 'vectorizer.fit_transform()' will implictly call this function to
        # extract features from the training set, which is a list of desc texts.
        # So once you call 'fit_transform()', the '__call__' function will be applied
        # on each desc text in the training set (a list of desc texts),
        features = []
        for word in self.process_desc(desc).split():
            if self.qualify(word):
                # Stem
                word = self.stemmer.stem(word, 0, len(word) - 1)

                features.append(word)

        return features
