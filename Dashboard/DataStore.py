# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

import os
import io
import numpy

from config import *

class DataStore(object):
	"""Access the data collected"""
	def __init__(self, path):
		super(DataStore, self).__init__()
		self._path = path

	def sources(self):
		return {
			'TWEE': {'name': 'Twitter', 'color': '#1F77B4'},
			'ILGI': {'name': 'Il Giornale', 'color': '#FF7F0E'},
			'ANSA': {'name': 'ANSA', 'color': '#2CA02C'},
			'CORR': {'name': 'Corriere della Sera', 'color': '#D62728'},
			'REPU': {'name': 'La Repubblica', 'color': '#ECE832'}
		}

	def parts(self):
		return [
			{'name': 'Night', 'hour': '00:00'},
			{'name': 'Day', 'hour': '07:00'},
			{'name': 'Afternoon', 'hour': '13:00'},
			{'name': 'Evening', 'hour': '19:00'},
		]

	def days(self):
		days = []
		for file in os.listdir(self._path):
			if file in IGNORE_FILES: continue
			day = file.rstrip('.txt').split('_')[1]
			if day not in days: days.append(day)
		return sorted(days)

	def dataForLayout(self):
		return {
			'day_dropdown': {
				'options' : [
					{'val': day, 'label': DataStore.presentDay(day)}
					for day in self.days()
				]
			},
			'sources-checklist': {
				'options': [
					{
						'id': id,
						'label': source['name'],
						'char': '◉',
						'color': source['color'],
						'checked': True
					}
					for id, source in self.sources().iteritems()
				]
			}
		}

	def dataForDailySentiment(self, day, sources):
		xs = []
		ys = []
		vars = []
		colors = []
		ids = []

		for source in sources:
			if not source['checked']: continue
			points = self._collectPointsForDay(day, source['id'])
			meanx, meany = self._computeMean(points)
			var = self._computeVar(points)
			xs.append(meanx)
			ys.append(meany)
			vars.append(var)
			colors.append(source['color'])
			ids.append(source['id'])

		return xs, ys, vars, colors, ids, vars

	def dataForDailyDetails(self, day, sourceId):
		points = self._collectPointsForDay(day, sourceId)
		xs = [time for time, positive, negative in points]
		ys = [positive for time, positive, negative in points]
		zs = [negative for time, positive, negative in points]
		color = self.sources()[sourceId]['color']
		return xs, ys, zs, color

	def dataForGlobalDropdownEnd(self, start_date):
		options = [
			{'val': day, 'label': DataStore.presentDay(day)}
			for day in self.days()
			if day >= start_date
		]

		return {
			'options': options,
			'selected': options[-1]['val']
		}

	def dataForSentimentTrend(self, start_date, end_date, sources):
		days = self._daysWithinRange(start_date, end_date)

		for source in sources:
			if not source['checked']: continue
			xs, ys, zs = self._sentimentTrendForSource(source['id'], days)
			yield {
				'name': source['label'],
				'color': source['color'],
				'xs': xs,
				'ys': ys,
				'zs': zs
			}

	def dataForVarianceTrend(self, start_date, end_date, sources):
		days = self._daysWithinRange(start_date, end_date)

		for source in sources:
			if not source['checked']: continue
			xs, ys = self._varianceTrendForSource(source['id'], days)
			yield {
				'name': source['label'],
				'color': source['color'],
				'xs': xs,
				'ys': ys
			}

	def _collectPointsForDay(self, day, sourceId):
		points = []

		for part in range(0, 5):
			points += self._collectPointsForPart(day, sourceId, part)

		return points

	def _collectPointsForPart(self, day, sourceId, part):
		points = []
		prefix = 'feed'
		if sourceId == 'TWEE': prefix = 'tweet'
		filename = '{}_{}_{}.txt'.format(prefix, day, part)
		filepath = PATH_PROCESSED_FOLDER+'/'+filename

		try:
			file = io.open(filepath, 'r', encoding='UTF-8')
			for line in file:
				infos = line.strip().split('\t')
				if (sourceId == 'TWEE') or (sourceId == infos[3]):
					points.append((infos[0], float(infos[1]), float(infos[2])))
			file.close()
		except IOError as e:
			pass

		return points

	def _computeMean(self, points):
		if len(points) == 0: return None, None

		mean_positive = sum([pos for time, pos, neg in points])/len(points)
		mean_negative = sum([neg for time, pos, neg in points])/len(points)
		return mean_positive, mean_negative

	def _computeVar(self, points):
		if len(points) == 0: return None

		return numpy.var(
			numpy.array(
				[(x, y) for t, x, y in points]
			).astype(numpy.float64)
		)

	def _daysWithinRange(self, start_date, end_date):
		return [
			day
			for day in self.days()
			if day >= start_date and day <= end_date
		]

	def _sentimentTrendForSource(self, sourceId, days):
		xs = []
		ys = []
		zs = []

		for day in days:
			for partId in range(0, 4):
				points = self._collectPointsForPart(day, sourceId, partId)
				mean_pos, mean_neg = self._computeMean(points)
				xs.append(DataStore.presentDay(day) + ' ' + self.parts()[partId]['hour'])
				ys.append(mean_pos)
				zs.append(mean_neg)

		return xs, ys, zs

	def _varianceTrendForSource(self, sourceId, days):
		xs = []
		ys = []

		for day in days:
			for partId in range(0, 4):
				points = self._collectPointsForPart(day, sourceId, partId)
				variance = self._computeVar(points)
				xs.append(DataStore.presentDay(day) + ' ' + self.parts()[partId]['hour'])
				ys.append(variance)

		return xs, ys

	@staticmethod
	def presentDay(date):
		return date[0:4]+'-'+date[4:6]+'-'+date[6:8]
