# -*- coding: utf-8 -*-

import nltk

from preprocessing import preprocess, index_search

if __name__ == "__main__":
	print ('Checking libraries...')
	nltk.download(['stopwords', 'punkt'])
	print ('Libraries check done.')
	
	preprocess.process_tweets()
	preprocess.preprocess_data()
	index_search.compute_inverted_index()