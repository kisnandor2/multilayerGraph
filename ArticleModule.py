# import pickle
import csv
import numpy as np

class Articles:
	"""
	Static class to build a list of article object
	"""
	@staticmethod
	def load(csvFileName, maxCount = None, groupBy=2):
		"""
		Load the data from csvFileName. All columns added as attributes from the csvFileName

		:param csvFileName: name of the csv file to be read

		:returns: list of articles, it's attributes
		"""
		articles = np.array([])
		articleHeaders = np.array([])
		reader = csv.reader(open(csvFileName, newline='\n'), delimiter=',', quotechar='"')
		i = -1
		for row in reader:
			if i < 0:
				for col in row:
					header = "".join(col.split())
					header = (header.encode('ascii', 'ignore')).decode("utf-8")
					articleHeaders = np.append(articleHeaders, header)
			else:
				article = Article(i)
				for j in range(0, len(row)):
					setattr(article, articleHeaders[j], row[j])
				article.formatAttributeValuesToList(attribute="Authors", groupBy=groupBy)
				articles = np.append(articles, article)
			i += 1
			if maxCount and i > maxCount:
				break
		return articles, articleHeaders


class Article:
	"""
	Class to describe an article. Attributes added dynamically in Articles static class.
	"""
	
	def __init__(self, id):
		"""
		Construct a new Article and add an id to it so it's easier to find it.
		
		:param id: id of the article (should be unique)

		:return: returns nothing
		"""

		self.id = id
		self.name = "Article_{}".format(id)
		self.Article = self.name

	def __repr__(self):
		"""
		Change it's representation to be it's name.
		"""

		return self.name

	def __str__(self):
		"""
		Printing all the attributes
		"""

		str = "Article_{}\n".format(self.id)
		for attribute in self.__dict__.keys():
			str += "{} : {}\n".format(attribute, getattr(self, attribute))
		return str

	def formatAttributeValuesToList(self, attribute, delimiter=',', groupBy=2):
		"""
		If the attribute should be represented as a list use this function.

		ex. article.Authors = "John, E., Julia, K."
				transfrom it into: 
			article.Authors = ["John E.", "Julia K."]

		:param attribute: which attribute should be represented as a list instead of a string
		:param delimiter: how to split the values
		:param groupBy: how many should be grouped in the created list

		:return: returns nothing
		"""

		# TODO: check if attribute is string!
		if attribute in self.__dict__.keys():
			oldValues = getattr(self, attribute)
			newValues = np.array([])
			oldValues = oldValues.split(delimiter)
			oldValues = list(map(str.strip, oldValues))
			for i in range(0, len(oldValues)//groupBy):
				newValue = " ".join(oldValues[i*groupBy:i*groupBy+groupBy])
				newValues = np.append(newValues, newValue)
			setattr(self, attribute, newValues)
		else:
			raise AttributeError("Attribute `{}` not found for `{}`".format(attribute, self.name))


	def save(self, fileName):
		# TODO:
		pass
	