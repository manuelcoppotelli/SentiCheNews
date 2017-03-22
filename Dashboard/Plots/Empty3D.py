# -*- coding: utf-8 -*-

from __future__ import unicode_literals

class Empty3D(object):
	"""An empty 3D graph"""
	def plot(self):
		return {
			'figure': self.figure()
		}

	def figure(self):
		return {
			'data': [{
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
