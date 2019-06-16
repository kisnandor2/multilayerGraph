import sys
sys.path.insert(0,'/mnt/d/_AAAEgyetem/Grafok/2018/bolozna-multilayer-networks-library')

from ArticleModule import Article, Articles
from GraphModule import GraphBuilder

import networkx as nx
from pymnet import *

from networkx.algorithms import community
import matplotlib.pyplot as plt

def getArticleById(articles, id):
	for article in articles:
		if article.id == id:
			return article
	return None

if __name__ == "__main__":
	articles, articleHeaders = Articles.load("scopus.csv", maxCount=3, groupBy=1)

	# print(getArticleById(articles, 2))

	print(articles)
	graphBuilder = GraphBuilder(articles, "Authors")

	# graphBuilder.createIntraConnections("Authors")
	# graphBuilder.createIntraConnections("Title")
	# graphBuilder.createOneToOneConnections("Authors", "Authors layer 1", "Authors layer 2")

	graphBuilder.createConnections(layerName1="Authors", layerName2="Title")
	# graphBuilder.createConnections(layerName1="Authors", layerName2="Authors")
	# graphBuilder.createConnections(layerName1="Authors", layerName2="Authors")

	graphBuilder.draw()
