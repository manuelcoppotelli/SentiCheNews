# -*- coding: utf-8 -*-

from __future__ import unicode_literals

class SentimentTrend(object):
	"""A sentiment trend graph"""
	def __init__(self, data):
		super(SentimentTrend, self).__init__()
		self.data = data

	def plot(self):
		return {
			'figure': self.figure()
		}

	def figure(self):
		return {
				'data': [
					{
						'type': 'scatter3d',
						'mode': 'markers+lines',
						'name': info['name'],
						'x': info['xs'],
						'y': info['ys'],
						'z': info['zs'],
						'marker': {
							'color': info['color']
						}
					}

					for info in self.data
				],

				'layout': {
					'autosize': True,
					'showlegend': False,
					'scene': {
						'xaxis': {
							'title': 'Time',
							'showspikes': False,
							'type': 'date',
							'calendar': 'gregorian',
							'tickangle': 45
						},
						'yaxis': {
							'title': 'Positive score',
							'showspikes': False,
							'range': [0, 1]
						},
						'zaxis': {
							'title': 'Negative score',
							'showspikes': False,
							'range': [0, 1]
						}
					}
				}
			}
