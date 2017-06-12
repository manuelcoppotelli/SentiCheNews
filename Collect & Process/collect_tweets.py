# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import shutil
from tweepy import Stream
from tweepy import OAuthHandler

from config import *
from Collector.TwitterListener import TwitterListener


if __name__ == "__main__":
	listener = TwitterListener()
	auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	stream = Stream(auth, listener)
	stream.filter(languages=['it'], track=['di','a','da','in','con','su','per','tra','fra'])

	if not os.path.exists(PATH_UNPROCESSED_FOLDER):
		os.mkdir(PATH_UNPROCESSED_FOLDER)

	saver = listener._saver
	shutil.move(saver.file_path, PATH_UNPROCESSED_FOLDER + '/')
