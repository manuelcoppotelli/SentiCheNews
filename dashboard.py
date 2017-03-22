# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import webbrowser

from config import *
from Dashboard.app import dash


if __name__ == '__main__':
	if not DEBUG: webbrowser.open_new('http://{}:{}'.format(HOST, PORT))
	dash.server.run(port=PORT, debug=DEBUG, host=HOST)
