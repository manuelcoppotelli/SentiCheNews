# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from dash.components import div, PlotlyGraph

import DailyViewControls

def render(data):
	return [
		div(className="tab-pane active", id="daily", role="tabpanel", content=[
			div(className="panel panel-default",
				content=DailyViewControls.render(data)
			),
			div(className='row', content=[
				div(className="col-md-6", content=[
					div(className="panel panel-default", content=[
						div("Sentiment", className="panel-heading"),
						div(className="panel-body", content=[
							PlotlyGraph(
								id='daily-sentiment',
								bindClick=True
							)
						])
					])
				]),
				div(className="col-md-6", content=[
					div(className="panel panel-default", content=[
						div("Details", className="panel-heading"),
						div(className="panel-body", content=[
							PlotlyGraph(id='daily-details')
						])
					])
				])
			])
		])
	]
