# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import time
import shutil
from datetime import datetime

from config import *
from Collector.Saver import Saver
from Collector.FeedParser import FeedParser

SOURCES = {
	'ILGI' : 'http://www.ilgiornale.it/feed.xml',
	'ANSA' : 'http://www.ansa.it/sito/notizie/topnews/topnews_rss.xml',
	'CORR' : 'http://xml.corriereobjects.it/rss/cronache.xml',
	'REPU' : 'http://www.repubblica.it/rss/cronaca/rss2.0.xml'
}

counter = 0

COLLECT_NEWS_CALLS = 12
BREAK = 1800

saver = Saver('feed')

def collect_news():
	for source, url in SOURCES.items():
		for news in FeedParser(url).items():
			try:
				news = ' '.join(news.split())
				saver.save("{}\t{}\t{}".format(datetime.now(), news, source))
			except Exception as e:
				print e, news

# ------------------------------------[main]------------------------------------
if __name__ == "__main__":
	# CALL 'collect_news' FUNCTION EVERY 30 MINUTES FOR 6 HOURS
	while counter < COLLECT_NEWS_CALLS:
		collect_news()
		counter +=1
		time.sleep(BREAK) # WAIT 30 MINUTES

	if not os.path.exists(PATH_UNPROCESSED_FOLDER):
		os.mkdir(PATH_UNPROCESSED_FOLDER)

	# FUNCTION THAT MOVES FILE/S FROM A SOURCE DIRECTORY TO A DESTINATION DIRECTORY
	shutil.move(saver._file_path, PATH_UNPROCESSED_FOLDER + '/')
