# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from dash.components import div

import GlobalView, DailyView

def render(data):
	return div(
		className="tab-content",
		content= GlobalView.render(data) + DailyView.render(data)
	)
