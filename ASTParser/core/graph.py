import networkx as nx
import matplotlib.pyplot as plt

from core.utils import Color
from core.utils import set_string_colored

from core.parser import ConstData

from core.parser import stmtList
from core.parser import actionList
from core.parser import dataList

class ASTGraph():
	def __init__(self, nodeList, edgeList, config):
		self.nodeList = nodeList
		self.edgeList = edgeList
		self.graph = None
		self.config = config

	def graph_initialize(self, encode_flag = False):
		if self.config.MAX_NODE_COUNT < len(self.nodeList):
			print(set_string_colored('Increase the graph configuration for MAX_NODE_COUNT', Color.RED.value))
			return

		self.graph = nx.Graph()

		if not encode_flag:
			# for node in self.nodeList:
			# 	self.graph.add_node(node)

			for edge in self.edgeList:
				if edge.pIndex == -1:
					self.graph.add_edge(
						str(edge.pIndex) + ':' + 'ROOT'
						, str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
				else:
					if type(self.nodeList[edge.cIndex].nodeInfo) != type(ConstData(None, None)):
						self.graph.add_edge(
							str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
							, str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
					else:
						self.graph.add_edge(
							str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
							, str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)

		else:
			for edge in self.edgeList:
				if edge.pIndex == -1:
					self.graph.add_edge(
						str(self.cal_labeled_index(edge.pIndex)) + ':' + 'ROOT'
						, str(self.cal_labeled_index(edge.cIndex)) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
				else:
					if type(self.nodeList[edge.cIndex].nodeInfo) != type(ConstData(None, None)):
						self.graph.add_edge(
							str(self.cal_labeled_index(edge.pIndex)) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
							, str(self.cal_labeled_index(edge.cIndex)) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
					else:
						self.graph.add_edge(
							str(self.cal_labeled_index(edge.pIndex)) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
							, str(self.cal_labeled_index(edge.cIndex)) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)

	def cal_labeled_index(self, index):
		nodeType = self.nodeList[index].nodeInfo.type

		if nodeType in stmtList:
			return stmtList.index(nodeType) * self.config.TYPE_WINDOW_SIZE + index
		elif nodeType in actionList:
			return (actionList.index(nodeType) + 20) * self.config.TYPE_WINDOW_SIZE + index
		elif nodeType in  dataList:
			return (dataList.index(nodeType) + 40) * self.config.TYPE_WINDOW_SIZE + index
		else:
			print(set_string_colored('UNKNOWN TYPE NODE...', Color.RED.value))

	def get_numeric_node_graph(self):
		if self.graph is None:
			print(set_string_colored('Graph Should be initialized first...', Color.RED.value))



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

class GraphConfig():
	def __init__(self, MAX_NODE_COUNT, TYPE_WINDOW_SIZE):
		self.MAX_NODE_COUNT = MAX_NODE_COUNT
		self.TYPE_WINDOW_SIZE = TYPE_WINDOW_SIZE