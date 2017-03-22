# -*- coding: utf-8 -*-

from __future__ import unicode_literals

class VarianceTrend(object):
	"""A variance trend graph"""
	def __init__(self, data):
		super(VarianceTrend, self).__init__()
		self.data = data

	def plot(self):
		return {
			'figure': self.figure()
		}

	def figure(self):
		return {
			'data': [
				{
					'type': 'scatter',
					'mode': 'lines',
					'name': info['name'],
					'x': info['xs'],
					'y': info['ys'],
					'line': {
						'color': info['color']
					}
				}

				for info in self.data
			],

			'layout': {
				'autosize': True,
				'showlegend': False,
				'xaxis': {
					'title': 'Time',
					'type': 'date',
					'calendar': 'gregorian',
					'tickangle': 45
				},
				'yaxis': {
					'title': 'Variance',
					'range': [0, 1]
				}
			}
		}
