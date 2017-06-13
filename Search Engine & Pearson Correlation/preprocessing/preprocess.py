# -*- coding: utf-8 -*-

import io
import re
import os
import nltk
import urllib
import pickle
import unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

from constants import *

STOPWORDS = set(stopwords.words('italian')) 
tokenizer = RegexpTokenizer(r'\w+')
stemmer = SnowballStemmer("italian")

def process_tweets():
	print ('Processing started')

	lookup = []

	f = io.open(TWEET_BAG_INPUT_FILE, 'w', encoding = 'utf-8')
	g = io.open(TWEET_INPUT_FILE, 'r', encoding = 'utf-8')

	counter = 1
	
	for line in g:

			words = line.split('\t')

			f.write('\t'.join(words[1:]))

			lookup.append( line )

			counter += 1

	f.close()
	g.close()
	store(lookup, LOOKUP_FILE_NAME)
	print ('Processing done')

def store(data, filename):
	output = open(filename, 'wb')
	pickle.dump(data, output)
	output.close()

def preprocess_data():
	print ('Preprocessing started...')
	f = io.open(TWEET_BAG_INPUT_FILE, 'r', encoding = 'utf-8')
	g = io.open(TWEET_OUTPUT_FILE, 'w', encoding = 'utf-8')

	counter = 1
	for line in f:
		bag = sorted(bag_of_words(line))
		g.write(u' '.join(bag) + '\n')
		counter +=1

	g.close()
	f.close()
	print ('Preprocessing done')

def bag_of_words(line):
	processed = line
	processed = processed.lower()
	processed = tokenizer.tokenize(processed)
	processed = remove_stopwords(processed)
	processed = normalization(processed)
	processed = stemming(processed)

	return processed

def remove_stopwords(line):
	return [word for word in line if word not in STOPWORDS]

def normalization(line):
	bucket = []

	for word in line:
		word = remove_accents(word)
		word = re.sub(u'\w+⁄\w+', '', word) #remove stange chars
		if word == u'': continue
		bucket.append(word)

	return bucket

def stemming(line):
	stemmed = []

	for word in line:
		stemmed.append(stemmer.stem(word))

	return stemmed

def remove_accents(input_str):
	nkfd_form = unicodedata.normalize('NFKD', input_str)
	return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

if __name__ == "__main__":
	process_tweets()
	preprocess_data()
