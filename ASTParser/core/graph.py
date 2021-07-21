import networkx as nx
import matplotlib.pyplot as plt

class ASTGraph():
	def __init__(self, nodeList, edgeList):
		self.nodeList = nodeList
		self.edgeList = edgeList
		self.graph = None

	def graph_initialize(self):
		self.graph = nx.Graph()

		for node in self.nodeList:
			self.graph.add_node(node)

	def draw_graph(self):
		nx.draw(self.graph, with_labels = True)
		print(nx.info(self.graph))

	def save_graph_png(self, savePath):
		plt.figure()

		self.draw_graph

		plt.axis('off')
		plt.savefig('/')
		plt.show()
		plt.savefig(savePath, format="PNG")