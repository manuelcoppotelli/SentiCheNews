# -*- coding: utf-8 -*-"

import os
import time
import pickle
import webbrowser
import re, math
from collections import Counter
from flask import Flask, request, g, render_template

import scipy
from scipy.stats import pearsonr

from constants import *
from preprocessing.index_search import search

if not os.path.exists(RESOURCES_FOLDER):
	print ('Folder structure miscofinguration.')
	os._exit(1)

if not os.path.exists(DATA_FOLDER):
	print ('You must run setup first.')
	os._exit(1)

print (" _____ _            _                              _    _         _     ")
print ("|_   _| |__   ___  | |    ___  __ _  ___ _ __   __| |  / \   _ __(_)___ ")
print ("  | | | '_ \ / _ \ | |   / _ \/ _` |/ _ \ '_ \ / _` | / _ \ | '__| / __|")
print ("  | | | | | |  __/ | |__|  __/ (_| |  __/ | | | (_| |/ ___ \| |  | \__ \\")
print ("  |_| |_| |_|\___| |_____\___|\__, |\___|_| |_|\__,_/_/   \_\_|  |_|___/")
print ("                              |___/                                     ")

# Load indexes at startup
input = open(INVERTED_INDEX_FILE_NAME, 'rb')
inverted_index = pickle.load(input)
input.close()

input = open(LOOKUP_FILE_NAME, 'rb')
lookup = pickle.load(input)
input.close()

top_k_tweets = 5 # how many similar tweets do you want with respect to the news?

WORD = re.compile(r'\w+')


def load_news_values():

	news_values = {}

	with open('offline_data/news_values.tsv', 'r', encoding='utf-8') as news:

		for line in news: 

			date = line.split('\t')[0]
			value= line.split('\t')[1]

			news_values[date] = float(value)

	return news_values


def top_k_similar_tweets():

	global top_k_tweets

	top_k_with_date = {}
	top_k_with_query = {}

	with open('offline_data/news.tsv', 'r', encoding='utf-8') as news:

		for line in news:

			query = line.split('\t')[1]
			date = line.split('\t')[0]
			
			docs = search(query, inverted_index, lookup, TOPK)

			top_k_with_date[date] = [x.split('\t')[1] for x in docs[:top_k_tweets]]
			top_k_with_query[query] = [x.split('\t')[1] for x in docs[:top_k_tweets]]

	return top_k_with_date, top_k_with_query

def queries_values_array(news_values, top_k_tweets):

	results = []

	dict_keys = list(top_k_tweets.keys())

	for key in dict_keys:

		value = news_values.get(key)
		results.append(value)

	return results

def get_cosine(vec1, vec2):

	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])

	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)

	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator

def text_to_vector(text):

	global WORD

	words = WORD.findall(text)
	return Counter(words)

def compute_cosine_similarity(top_k_tweets_query):

	global top_k_tweets

	results = []

	for key in top_k_tweets_query:

		vector1 = text_to_vector(key)

		values = list(top_k_tweets_query.get(key))

		cosine_values_sum = 0.0

		for value in values:

			vector2 = text_to_vector(value)

			cosine = get_cosine(vector1, vector2)

			cosine_values_sum += cosine

		mean_cosine = cosine_values_sum / top_k_tweets

		results.append(mean_cosine)


	return results

if __name__ == '__main__':

	news_values = load_news_values()

	top_k_tweets_date, top_k_tweets_query = top_k_similar_tweets()

	pearson_correlation_news_array   = queries_values_array(news_values, top_k_tweets_date)

	pearson_correlation_tweets_array = compute_cosine_similarity(top_k_tweets_query)

	pearson_coefficient, p_value = pearsonr(pearson_correlation_news_array, pearson_correlation_tweets_array)

	print("Pearson coefficient: ", pearson_coefficient)
	print()
	print("p value: ", p_value)
	print()


	positive_values = []
	negative_values = []

	for x, y in zip(pearson_correlation_news_array, pearson_correlation_tweets_array):

		if float(x) >= 0:

			positive_values.append(float(y))

		else: 

			negative_values.append(float(y))

	print("Mean cosine similarity for news with positive values: ", sum(positive_values) / len(positive_values))
	print("Mean cosine similarity for news with negative values: ", sum(negative_values) / len(negative_values))

