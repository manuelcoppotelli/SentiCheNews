# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import os
from datetime import datetime

from config import *

class Saver(object):

	_file_path = None # PATH WHERE DATA IS STORED

	def __init__(self, prefix=None):
		if not os.path.exists(DATA_FOLDER):
			os.mkdir(DATA_FOLDER)

		if not os.path.exists(PATH_DOWNLOADING_FOLDER):
			os.mkdir(PATH_DOWNLOADING_FOLDER)

		self._file_path = self.path(prefix)
		self._file = io.open(self._file_path, 'a', encoding = 'utf-8')

	def save(self, element):
		self._file.write(element)
		self._file.write("\n")

	def path(self, prefix):
		date = datetime.now()
		hour = int(date.strftime("%H"))

		part = None
		if hour >= 0 and hour <= 6: part = "0"
		if hour >= 7 and hour <= 12: part = "1"
		if hour >= 13 and hour <= 18: part = "2"
		if hour >= 19 and hour <= 24: part = "3"

		filename = date.strftime("%Y%m%d") + '_' + part + '.txt'

		if prefix:
			filename = prefix + '_' + filename

		return PATH_DOWNLOADING_FOLDER + '/' + filename
