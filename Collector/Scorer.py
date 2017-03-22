# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import io
import difflib

from config import *

class Scorer(object):
	VALUE_RATIO = 0.8
	ignoredWords = 0
	totalWords = 0

	def __init__(self):
		super(Scorer, self).__init__()
		self.dictionary, self.dictionary_keys = self.load_dictionary()
		self.dictionary_length = len(self.dictionary_keys)

	'''
	score() method computes the (positive,negative) values of a given string.
	The dictionary that it is used to compute the score contains also composite words
	separated by underscores: e.g. w_x_y_z.
	Therefore, the score() method tries, for each string,
	to see if there is a matching with a dictionary composite word, up to four terms.
	If the matching is positive, then the algorithm moves to the next four terms,
	otherwise it decreases the number of terms to three and so on.
	E.g. given string = "cat dog fish mouse"
	The algorithm searches first for the composite word "cat_dog_fish_mouse";
	if there is a matching then add the (positive, negative) value of this word
	to the list of values and move to the next four words of the string, if any;
	otherwise the algorithm searches for the composite word "cat_dog_fish" and so on..
	'''

	def score(self, stringa):
		values = []
		list_of_words = stringa.split()
		self.totalWords = self.totalWords + len(list_of_words)
		startIndex = 0
		endIndex = 4
		while(True):
			sublist = list_of_words[startIndex:endIndex]
			if not sublist:
				break
			else:
				for k in range(len(sublist),0,-1):
					word = "_".join(sublist[0:k])
					if word not in self.dictionary_keys:
						approx_word = self.searchApproxWord(word, 0, self.dictionary_length)
						if self.matchingPercentage(word, approx_word) < self.VALUE_RATIO:
							if k == 1:
								startIndex = startIndex + 1
								endIndex = startIndex + 4
								break # None of the words in the sublist had a positive matching --> Move to the next sublist of words
							else:
								continue
						values.append(self.dictionary[approx_word])
						startIndex = startIndex + k
						endIndex = startIndex + 4
						break # I found the word or the words so I have to move to the next sublist
					else:
						values.append(self.dictionary[word])
						startIndex = startIndex + k
						endIndex = startIndex + 4
						break # I found the word or the words so I have to move to the next sublist
		return self.computeCentroid(values)

	def computeCentroid(self, values):
		value_x = 0
		value_y = 0
		for x, y in values:
			value_x += float(x)
			value_y += float(y)

		if len(values) == 0:
			raise Exception("Unable to score the given string")

		value_x /= len(values)
		value_y /= len(values)
		return value_x, value_y

	def searchApproxWord(self, word, begin, end):
		position = (begin + end) // 2
		if self.matchingPercentage(word, self.dictionary_keys[position]) >= self.VALUE_RATIO:
			return self.dictionary_keys[position]
		if end - begin == 1:
			return self.dictionary_keys[position]
		if word > self.dictionary_keys[position]:
			begin = position
			return self.searchApproxWord(word, begin, end)
		else:
			end = position
			return self.searchApproxWord(word,begin,end)

	def matchingPercentage(self, s1, s2):
		return difflib.SequenceMatcher(None, s1, s2).ratio()

	@staticmethod
	def load_dictionary():
		dictionary = {}
		words = []
		with io.open(DATA_FOLDER + '/dictionary.txt', 'r', encoding='utf-8') as fo:
			for line in fo:
				list_of_words = line.split('\t')
				dictionary[list_of_words[0]] = (list_of_words[1], list_of_words[2])
				words.append(list_of_words[0])
		return dictionary, words
