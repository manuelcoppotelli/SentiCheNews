# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime, timedelta
from tweepy.streaming import StreamListener

from Saver import Saver

class TwitterListener(StreamListener):

	_saver = Saver('tweet')

	def __init__(self):
		super(TwitterListener, self).__init__()
		self._expire = datetime.now() + timedelta(hours=6)
		self._lastdate = datetime.strptime("0001-01-01 00:00:00.000000", "%Y-%m-%d %H:%M:%S.%f")

	def on_status(self, status):
		current_date = datetime.now()

		if current_date >= self._expire:
			return False # break the stream

		if (current_date-self._lastdate) <= timedelta(minutes=1):
			return True

		self._lastdate = current_date

		try:
			txt = status.text
			txt = txt.replace("\n", " ").replace("\r", " ").replace("\n\n", " ")
			txt = ' '.join(txt.split())

			self._saver.save("{}\t{}".format(datetime.now(), txt))
		except Exception as e:
			print e, status.text

		return True # keep on streaming

	def on_error(self, status):
		print 'Error:', status
		return False # break the stream
