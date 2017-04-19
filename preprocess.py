# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import os
import shutil

from config import *
from Collector.Scorer import Scorer

scorer = Scorer()

def preprocess_feed(input_file, output_file, ignored_file):
	for line in input_file:
		date, txt, source = line.rstrip("\n").split('\t')
		try:
			value = scorer.score(txt)
			output_file.write("{}\t{}\t{}\n".format(date, value, source))
		except Exception as e:
			ignored_file.write("{}\t{}".format(e, line))

def preprocess_tweet(input_file, output_file, ignored_file):
	for line in input_file:
		date, txt = line.split('\t')
		try:
			value = scorer.score(txt)
			output_file.write("{}\t{}\n".format(date, value))
		except Exception as e:
			ignored_file.write("{}\t{}".format(e, line))

def preprocess_file(file):
	input_file = io.open(PATH_UNPROCESSED_FOLDER + '/' + file, 'r', encoding='utf-8')
	output_file = io.open(PATH_PROCESSED_FOLDER + '/' + file, 'w', encoding='utf-8')
	ignored_file = io.open(PATH_IGNORED_FOLDER + '/' + file, 'w', encoding='utf-8')

	kind = file.split('_')[0]

	if kind == 'feed':
		preprocess_feed(input_file, output_file, ignored_file)

	if kind == 'tweet':
		preprocess_tweet(input_file, output_file, ignored_file)

	ignored_file.close()
	output_file.close()
	input_file.close()
	shutil.move(PATH_UNPROCESSED_FOLDER + '/' + file, PATH_ARCHIVED_FOLDER + '/' + file)

def preprocess_files():
	if not os.path.exists(PATH_UNPROCESSED_FOLDER):
		print 'No file to preprocess.'
		return

	if not os.path.exists(PATH_PROCESSED_FOLDER):
		os.mkdir(PATH_PROCESSED_FOLDER)

	if not os.path.exists(PATH_IGNORED_FOLDER):
		os.mkdir(PATH_IGNORED_FOLDER)

	if not os.path.exists(PATH_ARCHIVED_FOLDER):
		os.mkdir(PATH_ARCHIVED_FOLDER)

	for file in os.listdir(PATH_UNPROCESSED_FOLDER):
		if file in IGNORE_FILES: continue
		if os.path.isdir(DATA_FOLDER + '/' + file): continue
		preprocess_file(file)


# ------------------------------------[main]------------------------------------
if __name__ == "__main__":
	preprocess_files()
