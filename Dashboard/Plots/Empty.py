# -*- coding: utf-8 -*-

from __future__ import unicode_literals

class Empty(object):
	"""An empty graph"""
	def plot(self):
		return {
			'figure': self.figure()
		}

	def figure(self):
		return {
			'data': [{}],
			'layout': {}
		}
