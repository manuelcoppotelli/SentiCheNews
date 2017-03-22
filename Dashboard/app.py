# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from dash import Dash

from config import *
from Layouts import MainLayout
from DataStore import DataStore
from Plots import SentimentTrend, VarianceTrend, DailySentiment, DailyDetails, Empty3D

dash = Dash(__name__)
dataStore = DataStore(PATH_PROCESSED_FOLDER)
dash.layout = MainLayout.render(dataStore.dataForLayout())

@dash.react('end-day-dropdown', ['start-day-dropdown'])
def dropdown_end_day(start_day):
	return dataStore.dataForGlobalDropdownEnd(start_day.selected)

@dash.react('sentiment-trend', ['start-day-dropdown', 'end-day-dropdown', 'global-sources-checklist'])
def graph_sentiment_trend(start_day, end_day, sources):
	data_sentiment = dataStore.dataForSentimentTrend(start_day.selected, end_day.selected, sources.options)
	return SentimentTrend(data_sentiment).plot()

@dash.react('variance-trend', ['start-day-dropdown', 'end-day-dropdown', 'global-sources-checklist'])
def graph_sentiment_trend(start_day, end_day, sources):
	data_variance = dataStore.dataForVarianceTrend(start_day.selected, end_day.selected, sources.options)
	return VarianceTrend(data_variance).plot()

@dash.react('daily-sentiment', ['day-dropdown', 'daily-sources-checklist'])
def graph_daily_sentiment(day, sources):
	data = dataStore.dataForDailySentiment(day.selected, sources.options)
	return DailySentiment(*data).plot()

@dash.react('daily-details', ['day-dropdown', 'daily-sentiment'])
def graph_daily_details(day, daily_sentiment):
	try:
		point = getattr(daily_sentiment, 'click')['points'][0]['pointNumber']
		sourceId = daily_sentiment.figure['data'][0]['IDs'][point]
		data = dataStore.dataForDailyDetails(day.selected, sourceId)
		return DailyDetails(*data).plot()
	except:
		return Empty3D().plot()
