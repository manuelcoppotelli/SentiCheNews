# -*- coding: utf-8 -*-

import io
import pickle
import math
from preprocessing.preprocess import bag_of_words

from constants import *

counter = 1

def compute_inverted_index():

	global counter 

	print ('Computing inverted index...')
	inverted_index = {}

	f = io.open(TWEET_PROCESSED_FILE, 'r', encoding = 'utf-8')

	for line in f:
		vector = compute_normalized_vector(line)
		index_merge(inverted_index, vector, counter)
		counter += 1

	f.close()
	store(inverted_index, INVERTED_INDEX_FILE_NAME)
	print ('Inverted index done.')

def compute_normalized_vector(line):
	frequencies = compute_vector(line)
	norm = compute_norm(frequencies)

	for (key, value) in frequencies.items():
		frequencies[key] = float(value)/norm

	return frequencies

def compute_vector(line):
	vector = {}

	for word in line.split():
		try:
			vector[word] += 1
		except:
			vector[word] = 1

	return vector

def compute_norm(dictionary):
	summation = 0
	for value in dictionary.values():
		summation += value**2

	return math.sqrt(summation)

def index_merge(index, frequencies, docid):
	for (key, value) in frequencies.items():
		try:
			index[key].append((docid, value))
		except:
			index[key] = [(docid, value)]

def store(data, filename):
	output = open(filename, 'wb')
	pickle.dump(data, output)
	output.close()

def search(query, index, lookup, top):
	terms = bag_of_words(query)
	docs = get_documents(terms, index)
	top = top_k(docs, top)
	results = prepare_results(top, lookup)
	return results

def prepare_results(docs, lookup):
	result = []

	for (docid, rank) in docs:
		result.append(lookup[docid-1])

	return result

def get_documents(terms, inverted_index):
	legth_limit = 10
	documents = {}
	results = []

	first = and_search(terms, inverted_index)
	merge(results, documents, first)

	if len(documents) < legth_limit:
		half = len(terms) / 2
		a = and_search(terms[0:int(half)], inverted_index)
		b = and_search(terms[int(half):], inverted_index)
		c = and_search(terms[0:len(terms):2], inverted_index)
		d = and_search(terms[1:len(terms):2], inverted_index)
		b.update(a)
		c.update(b)
		d.update(c)
		merge(results, documents, d)

	if len(documents) < legth_limit:
		d = or_search(terms, inverted_index)
		merge(results, documents, d)

	return results

def merge(results, dict1, dict2):
	dict2 = sorted(dict2.items(), key=lambda x: x[1], reverse=True)
	k = dict1.keys()
	for (key, value) in dict2:
		if key not in k:
			dict1[key] = value
			results.append((key, value))

def or_search(terms, inverted_index):

	global counter 

	scores = {}

	for term in terms:
		try:
			posting_list = inverted_index[term]
			denominator = len(posting_list)
			idf = math.log10(counter / denominator)

			for (doc, tf) in posting_list:
				try:
					scores[doc] += tf * idf
				except:
					scores[doc] = tf * idf
		except:
			pass

	return scores

def and_search(terms, inverted_index):

	global counter

	scores = {}

	first = True

	for term in terms:
		prod = {}
		try:
			posting_list = inverted_index[term]
			denominator = len(posting_list)
			idf = math.log10(counter / denominator)

			for (doc, tf) in posting_list:
				try:
					prod[doc] += tf * idf
				except:
					prod[doc] = tf * idf
		except:
			pass

		if first:
			first = False
			scores = prod
		else:
			scores = {x:prod[x] for x in prod if x in scores}

	return scores

def top_k(docs, k = None):
	if not k:
		return docs

	return docs[0:k]


def loading():
	print ('Loading...')

	input = open(INVERTED_INDEX_FILE_NAME, 'rb')
	inverted_index = pickle.load(input)
	input.close()

	input = open(LOOKUP_FILE_NAME, 'rb')
	lookup = pickle.load(input)
	input.close()

	print ('Loading done.')

	return inverted_index, lookup

def listen_for_queries(inverted_index, lookup):
	while True:
		query = raw_input()
		print (search(query, 'false', inverted_index, lookup, 10))

if __name__ == "__main__":
	compute_inverted_index()
	inverted_index, lookup = loading()
	listen_for_queries(inverted_index, lookup)
