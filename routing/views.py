from django.conf import settings
from appmodels.models import *
from django.shortcuts import render_to_response
import marshal

from dijkstra import shortestPath

class ChangeOver:
	def __init__(self, start_stage, end_stage, routes):
		self.start_stage = start_stage
		self.end_stage = end_stage
		self.routes = routes

def direct_routes_between(start, end):
	return Route.objects.filter(stages__id=start.id).filter(stages__id=end.id)	

def show_shortest_path(request, start, end):
	G = marshal.load(open(settings.GRAPH_CACHE, 'rb'))
	path = shortestPath(G, int(start), int(end), weighted=False)
	stages = [Stage.objects.get(id=sid) for sid in path]
	changeovers = []
	for i in xrange(0,len(stages) - 1):
		startStage = stages[i]
		endStage = stages[i+1]
		rc = ChangeOver(
				start_stage = startStage,
				end_stage = endStage,
				routes=direct_routes_between(startStage, endStage))
		changeovers.append(rc)
	return render_to_response("show_shortest_path.html",
			{
				'changeovers':changeovers,
				'start_stage':Stage.objects.get(id=start),
				'end_stage':Stage.objects.get(id=end)
				})