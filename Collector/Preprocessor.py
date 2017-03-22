# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import unicodedata
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

STOPWORDS = set(stopwords.words('italian'))
tokenizer = RegexpTokenizer(r'\w+')

'''
IDEA: We take one tweet at a time from the Twitter stream
(through the TwitterListener class)
	The class TwitterListener extract the text of the current tweet and calls a
	method of this class in order to preprocess the text
	This class has the goal to preprocess text and save it into a file (in order
	to analyze the work)
	In a second moment, this class will call a method of the sentiment analyzer
	class, which will give a value to the text (positive or negative)
'''

class Preprocessor:

	@staticmethod
	def preprocess(text):
		list_of_words = tokenizer.tokenize(text)
		to_write = []
		for word in list_of_words:
			word = word.lower()
			if(Preprocessor.is_not_stopword(word)):
				word = Preprocessor.normalization(word)
				to_write.append(word)

		return ' '.join(to_write)

	@staticmethod
	def is_not_stopword(word):
		'''return True if the word is NOT a stopword, false otherwise'''
		if word not in STOPWORDS:
			return True
		else:
			return False

	@staticmethod
	def remove_accents(input_str):
		nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
		return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

	@staticmethod
	def normalization(word):
		word = Preprocessor.remove_accents(word)
		word = re.sub(u'\w+/\w+', '', word)  # remove strange chars
		return word
