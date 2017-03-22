# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from dash.components import div, label, Dropdown, CheckList

def render(data):
	return [
		div(className="panel-heading", content=[
			div(className="form-inline", content=[
				div(className="form-group", content=[
					label("From:"),
					Dropdown(
						id='start-day-dropdown',
						options=data['day_dropdown']['options']
					)
				]),
				div(className="form-group", content=[
					label("To:"),
					Dropdown(
						id='end-day-dropdown',
						options=[{'val':'', 'label': ''}]
					)
				]),
				div(className="form-group", content=[
					CheckList(
						id='global-sources-checklist',
						options=data['sources-checklist']['options']
					)
				])
			])
		])
	]
