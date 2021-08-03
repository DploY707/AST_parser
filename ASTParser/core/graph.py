import networkx as nx
import matplotlib.pyplot as plt

from core.parser import ConstValueNode

class ASTGraph():
	def __init__(self, nodeList, edgeList):
		self.nodeList = nodeList
		self.edgeList = edgeList
		self.graph = None

	def graph_initialize(self):
		self.graph = nx.Graph()

		# for node in self.nodeList:
			# self.graph.add_node(node)

		for edge in self.edgeList:
			if edge.pIndex == -1:
				self.graph.add_edge(
					str(edge.pIndex) + ':' + 'ROOT'
					, str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
			else:
				if type(self.nodeList[edge.cIndex]) != type(ConstValueNode(None, None)):
					self.graph.add_edge(
						str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
						, str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
				else:
					self.graph.add_edge(
						str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
						, str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo)

	def draw_graph(self):
		nx.draw(self.graph, pos=nx.drawing.nx_agraph.graphviz_layout(self.graph, prog='dot'),  with_labels=True)
		print(nx.info(self.graph))

	def save_graph_as_png(self, savePath):
		plt.figure()

		self.draw_graph()

		plt.axis('off')
		plt.savefig('/')
		plt.show()
		plt.savefig(savePath, format="PNG")