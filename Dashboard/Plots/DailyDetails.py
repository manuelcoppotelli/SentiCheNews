# -*- coding: utf-8 -*-

from __future__ import unicode_literals

class DailyDetails(object):
	"""A daily details graph"""
	def __init__(self, x, y, z, color):
		super(DailyDetails, self).__init__()
		self.x = x
		self.y = y
		self.z = z
		self.color = color

	def plot(self):
		return {
			'figure': self.figure()
		}

	def figure(self):
		return {
			'data': [{
				'marker': {
					'sizemode': 'area',
					'color': self.color
				},
				'mode': 'markers',
				'x': self.x,
				'y': self.y,
				'z': self.z,
				'type': 'scatter3d'
			}],

			'layout': {
				'autosize': True,
				'scene': {
					'xaxis': {
						'title': 'Time',
						'showspikes': False,
						'type': 'date',
						'calendar': 'gregorian',
						'tickformat': '%H:%M',
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
