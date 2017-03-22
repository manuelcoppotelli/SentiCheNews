# -*- coding: utf-8 -*-

from __future__ import unicode_literals

class DailySentiment(object):
	"""A daily sentiment graph"""
	def __init__(self, x, y, size, colors, ids, text):
		super(DailySentiment, self).__init__()
		self.x = x
		self.y = y
		self.size = size
		self.colors = colors
		self.ids = ids
		self.text = ['Variance: '+str(t)[:6] for t in text]

	def plot(self):
		return {
			'figure': self.figure()
		}

	def figure(self):
		return {
			'data': [{
				'name': 'Variance',
				'marker': {
					'sizemode': 'area',
					'sizeref': 0.00001,
					'size': self.size,
					'color': self.colors
				},
				'mode': 'markers',
				'hoverinfo': 'all',
				'text': self.text,
				'IDs': self.ids,
				'y': self.y,
				'x': self.x,
				'type': 'scatter'
			}],

			'layout': {
				'autosize': True,
				'breakpoints': [],
				'hovermode': 'closest',
				'xaxis': {
					'type': 'linear',
					'autorange': False,
					'range': [0, 1],
					'title': 'Positive score'
				},
				'yaxis': {
					'type': 'linear',
					'autorange': False,
					'range': [0, 1],
					'title': 'Negative score'
				},
				'images': [{
					'source': './static/triangle.png',
					'xref': 'x',
					'yref': 'y',
					'x': 0,
					'y': 0,
					'sizex': 1,
					'sizey': 1,
					'xanchor': 'left',
					'yanchor': 'bottom',
					'sizing': 'stretch',
					'opacity': 0.7,
					'layer': 'below'
				}]
			}
		}
