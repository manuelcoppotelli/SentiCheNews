# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from dash.components import div, PlotlyGraph

import GlobalViewControls

def render(data):
	return [
		div(className="tab-pane active", id="global", role="tabpanel", content=[
			div(className="panel panel-default",
				content=GlobalViewControls.render(data)
			),
			div(className="row", content=[
				div(className="col-md-6", content=[
					div(className="panel panel-default", content=[
						div("Sentiment Trend", className="panel-heading"),
						div(className="panel-body", content=[
							PlotlyGraph(id='sentiment-trend')
						])
					])
				]),
				div(className="col-md-6", content=[
					div(className="panel panel-default", content=[
						div("Variance Trend", className="panel-heading"),
						div(className="panel-body", content=[
							PlotlyGraph(id='variance-trend')
						])
					])
				])
			])
		])
	]
