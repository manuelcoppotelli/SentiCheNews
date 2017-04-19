# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
import requests

from config import *

class Scorer(object):

	def __init__(self):
		super(Scorer, self).__init__()
		self.session = requests.Session()  # I need Session() in order to keep alive the HTTP connection

	def score(self, stringa):

		payload = {
		'token': TOKEN_DANDELION,
		'text': stringa,
		'lang': LANGUAGE
		}

		response = self.session.get(SENTIMENT_URL, params=payload).json()
		sentiment = response["sentiment"]
		return json.dumps(sentiment["score"])
