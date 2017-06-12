# -*- coding: utf-8 -*-"

import os
import time
import pickle
import webbrowser
from flask import Flask, request, g, render_template

from constants import *
from preprocessing.index_search import search

if not os.path.exists(RESOURCES_FOLDER):
	print ('Folder structure miscofinguration.')
	os._exit(1)

if not os.path.exists(DATA_FOLDER):
	print ('You must run setup first.')
	os._exit(1)

print (" _____ _            _                              _    _         _     ")
print ("|_   _| |__   ___  | |    ___  __ _  ___ _ __   __| |  / \   _ __(_)___ ")
print ("  | | | '_ \ / _ \ | |   / _ \/ _` |/ _ \ '_ \ / _` | / _ \ | '__| / __|")
print ("  | | | | | |  __/ | |__|  __/ (_| |  __/ | | | (_| |/ ___ \| |  | \__ \\")
print ("  |_| |_| |_|\___| |_____\___|\__, |\___|_| |_|\__,_/_/   \_\_|  |_|___/")
print ("                              |___/                                     ")

# Load indexes at startup
input = open(INVERTED_INDEX_FILE_NAME, 'rb')
inverted_index = pickle.load(input)
input.close()

input = open(LOOKUP_FILE_NAME, 'rb')
lookup = pickle.load(input)
input.close()

app = Flask(__name__, static_folder=RESOURCES_FOLDER, template_folder=RESOURCES_FOLDER+'/templates')

@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)

@app.route('/')
def index():
	query = request.args.get('query')

	if query is None or not query:
		return render_template('home.html')

	docs = search(query, inverted_index, lookup, TOPK)
	return render_template('results.html', query=query, docs=docs, num=len(docs))

if __name__ == '__main__':
	if not DEBUG:
		webbrowser.open_new('http://%s:%d' % (HOST, PORT))

	app.run(debug=DEBUG, host=HOST, port=PORT)
