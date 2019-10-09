import sys
sys.path.insert(0,'/mnt/d/_AAAEgyetem/Grafok/2018/bolozna-multilayer-networks-library')

from ArticleModule import Article, Articles
import matplotlib.pyplot as plot
# from GraphModule import GraphBuilder

import networkx as nx
# from pymnet import *

import pymnet as net
import numpy as np

from networkx.algorithms import community
import matplotlib.pyplot as plt

def getArticleById(articles, id):
	for article in articles:
		if article.id == id:
			return article
	return None

def buildLayer1(articles, year):
	G = nx.Graph()
	for article in articles:
		if int(article.Year) not in year:
			continue
		for author in article.Authors:
			G.add_node(author['name'])
		for author1 in article.Authors:
			for author2 in article.Authors:
				if author1['name'] != author2['name']:
					G.add_edge(author1['name'], author2['name'])
	return G

def buildLayer2(articles, year):
	G = nx.Graph()
	for article in articles:
		if int(article.Year) not in year:
			continue
		for author in article.Authors:
			G.add_node(author['name'])
		for author1 in article.Authors:
			for author2 in article.Authors:
				if author1['affiliation'] != author2['affiliation']:
					G.add_edge(author1['name'], author2['name'])
	return G

def buildMultiplex(G, layerName, g):
	G.add_layer(layerName, 1)
	for node in g.nodes:
		G.add_node(node, layerName)
	for edge in g.edges:
		b, e = edge
		G[b, e, layerName, layerName] = 1
	return G


if __name__ == "__main__":
	# articles, articleHeaders = Articles.load("scopus.csv", maxCount=None, groupBy=1)

	# year = list(range(2019, 2020))
	# network1 = buildLayer1(articles, year=year)
	# nx.write_gml(network1, "network1.gml")

	# network2 = buildLayer2(articles, year=year)
	# nx.write_gml(network2, "network2.gml")	


	# nx.draw_kamada_kawai(network2)
	# plot.show()

	g = nx.read_gml('network1.gml')
	h = nx.read_gml('network2.gml')

	G = net.MultilayerNetwork(aspects=1,fullyInterconnected=False)
	G = buildMultiplex(G, 'layer1', g)
	# G = buildMultiplex(G, 'layer2', h)
	G.add_layer('layer2', 1)
	for node in ['A','B','C','D']:
		G.add_node(node, 'layer2')
	G['A','B', 'layer2', 'layer2'] = 1
	G['A','D', 'layer2', 'layer2'] = 1
	G['D','B', 'layer2', 'layer2'] = 1

	# for node in g.nodes:
	# 	G[node, node, 'layer1', 'layer2'] = 1

	nodeLabelDict = {}
	i = 1
	for node in g.nodes:
		nodeLabelDict[node] = i
		i += 1
	for node in ['A','B','C','D']:
		nodeLabelDict[node] = node
	
	net.draw(G, show=True, nodeLabelDict=nodeLabelDict, alignedNodes=True, layergap=1.4)
