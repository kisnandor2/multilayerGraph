import pymnet as net
import numpy as np
import warnings

from utilities import debug

class GraphBuilder:
	"""
	This class is used to create the multilayer graph. pymnet used as module
	"""

	def __init__(self, objects, baseLayerName):
		"""
		Construct new `GraphBuilder` object. The attribute of an object = layerName. Ex. objects[0].Author -> layerName must be "Author"

		:param objects: a list of any type that contains at least one object that has any number and kind of atributes
		:param baseLayerName: the layer which will contain the objects as nodes (with all attributes)

		:return: returns nothing
		"""

		if len(objects) == 0:
			raise IndexError("`articles` is empty")

		self.G = net.MultilayerNetwork(aspects=1,fullyInterconnected=False)
		self.objects = objects
		self.layers = np.array([])
		self.baseLayerName = baseLayerName

		# Create default layer for objects
		if self.baseLayerName not in objects[0].__dict__.keys():
			warnings.warn("GraphBuilder not used for {}! Initializing with no layers!".format(self.baseLayerName))
		else:
			self.createIntraConnections(self.baseLayerName)

	def addLayer(self, layerName, layerRenamed=None):
		"""
		Add a layer to the graph. If it was already added does nothing

		:param layerName: the name of the new layer to be added

		:return: returns True if the new layer was added, otherwise False
		"""

		
		if layerRenamed is None:
			self._checkLayerInAttributes(layerName)
		if layerName not in self.layers:
			self.G.add_layer(layerName, 1)
			self.layers = np.append(self.layers, layerName)
			return True
		# else:
		# 	self.G.add_layer(layerName+' layer 2', 1)
		# 	self.layers = np.append(self.layers, layerName + '2')
		# 	return True

		return False

	def createIntraConnections(self, layerName, layerRenamed=None):
		"""
		Adds the layer if needed, adds the nodes to the layer and creates the connections on that specific layer
		TODO: at the moment just the nodes are added, no intra connnections


		:param layerName: the name of the layer

		:return: returns nothing
		"""

		if layerRenamed is None:
			layerRenamed = layerName

		if not self.addLayer(layerName, layerRenamed):
			return

		attribType = type(getattr(self.objects[0], layerName))
		for obj in self.objects:
			attrib = getattr(obj, layerName)
			if attribType is np.ndarray or attribType is list:
				for att in attrib:
					self.G.add_node(att, layerRenamed)
			else:
				self.G.add_node(attrib, layerRenamed)
			
		setVerticesProcessed = set()
		for obj in self.objects:
			if attribType is np.ndarray or attribType is list:
				for vertex in getattr(obj, layerName):
					if vertex not in setVerticesProcessed:
						setVerticesProcessed.add(vertex)
						vertexNeighbors = self._getNeighbors(vertex, layerName)
						for neighbor in vertexNeighbors:
							self.G[vertex, neighbor, layerRenamed, layerRenamed] = 1

	def createInterConnections(self, layerName1, layerName2):
		"""
		It just creates the connections between the two layers. 
		No layer added. No nodes added.
		Use it when you want to connect two layers that were already added before.

		:param layerName1: name of the 1. layer
		:param layerName2: name of the 2. layer

		:return: returns nothing
		"""

		for obj in self.objects:
			attribVals1 = getattr(obj, layerName1)
			attribVals2 = getattr(obj, layerName2)

			if type(attribVals1) is np.ndarray:
				attribVals1 = list(attribVals1)
			if type(attribVals2) is np.ndarray:
				attribVals2 = list(attribVals2)

			if (type(attribVals1) is list) and (type(attribVals2) is list):				
				for attrib1 in attribVals1:
					for attrib2 in attribVals2:
						self.G[attrib1, attrib2, layerName1, layerName2] = 1
				return

			elif type(attribVals2) is list:
				helper = attribVals2
				attribVals2 = attribVals1
				attribVals1 = helper

				helper = layerName1
				layerName1 = layerName2
				layerName2 = helper

			# attribVals2 is not a list at this point
			if type(attribVals1) is list:
				if layerName2 == self.baseLayerName:
					for attrib1 in attribVals1:
						self.G[attrib1, obj, layerName1, layerName2] = 1
				else:
					for attrib1 in attribVals1:
						self.G[attrib1, attribVals2, layerName1, layerName2] = 1
			else:
				if layerName1 == self.baseLayerName:
					self.G[obj, attribVals2, layerName1, layerName2] = 1
				elif layerName2 == self.baseLayerName:
					self.G[attribVals1, obj, layerName1, layerName2] = 1
				else:
					self.G[attribVals1, attribVals2, layerName1, layerName2] = 1
		return

	def createOneToOneConnections(self, attribName, layerName1, layerName2):
		for obj in self.objects:
			attribVals1 = getattr(obj, attribName)
			attribVals2 = getattr(obj, attribName)

			if type(attribVals1) is np.ndarray:
				attribVals1 = list(attribVals1)
			if type(attribVals2) is np.ndarray:
				attribVals2 = list(attribVals2)

			if (type(attribVals1) is list) and (type(attribVals2) is list):
				for attrib1 in attribVals1:
					for attrib2 in attribVals2:
						self.G[attrib1, attrib2, layerName1, layerName2] = 1

	def createConnections(self, layerName1, layerName2):
		"""
		Creates both intra and inter connections. Layers added. Nodes added. 
		This should be used in most of the cases.

		:param layerName1: name of the 1. layer
		:param layerName2: name of the 2. layer

		:return: returns nothing
		"""

		self.createIntraConnections(layerName1)
		self.createIntraConnections(layerName2)
		self.createInterConnections(layerName1, layerName2)

	def getGraph(self):
		"""
		Get the graph that was built.

		:return: returns the graph that is ready to be used anywhere
		"""

		return self.G

	def _getNeighbors(self, attribute, layerName):
		"""
		Inner function to get the neighbors of a vertex

		:param attrib: who's neighbor are we searching for
		:param layerName: on which layer we want to find neighbors

		:return: list of neighbors
		"""
		debug("_getNeighbors", attribute, layerName)

		ret = []
		attribType = type(getattr(self.objects[0], layerName))
		if (attribType is np.ndarray) or (attribType is list):
			debug("attrib is a list")
			for obj in self.objects:
				attribs = getattr(obj, layerName)
				if attribute in attribs:
					for attrib in attribs:
						ret.append(attrib)
			ret = set(ret)
			ret.remove(attribute)

			debug(attribute, ret)

			debug("ret")
			return list(ret)
		debug("attrib is not a list")
		debug("ret")
		return ret

	def _checkLayerInAttributes(self, layerName):
		"""
		Inner function to check if the layer which is going to be added exists as an attribute of the object

		:raises IndexError: layerName not found as an attribute of the object

		:return: returns nothing
		"""

		if layerName not in self.objects[0].__dict__.keys():
			raise IndexError('Attribute `{}` not found in objects'.format(layerName))

	def draw(self):
		"""
		Function to disiplay the graph. Should be checked and modified manually, Just for testing purposes

		:return: returns nothing
		"""
		
		nodeLabelDict = {}
		for obj in self.objects:
			nodeLabelDict[obj] = obj.name
			nodeLabelDict[obj.Title] = "Title_{}".format(obj.id)
			nodeLabelDict[obj.Year] = obj.Year
			for author in obj.Authors:
				nodeLabelDict[author] = author
		net.draw(self.G, show=True, nodeLabelDict=nodeLabelDict, alignedNodes=True, layergap=1.1)
