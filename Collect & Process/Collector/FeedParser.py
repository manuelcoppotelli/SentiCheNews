# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import feedparser

class FeedParser(object):
	"""Pasre RSS feeds to obtain text"""
	def __init__(self, url):
		super(FeedParser, self).__init__()
		self.url = url
		self._feed = feedparser.parse(self.url)

	def items(self):
		for item in self._feed['items']:
			yield self.unescape(item['title'])

	@staticmethod
	def unescape(string):
		htmlCodes = (
			("&", '&amp;'),
			("'", '&#39;'),
			("\"", '&quot;'),
			(">", '&gt;'),
			("<", '&lt;'),
			("'", '&rsquo;'),
		)
		for code in htmlCodes:
			string = string.replace(code[1], code[0])
		return string
