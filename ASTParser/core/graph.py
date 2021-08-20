import networkx as nx
import os
import sys
import matplotlib.pyplot as plt
import re

from core.utils import Color
from core.utils import set_string_colored

from core.parser import ConstData

from core.parser import stmtList
from core.parser import actionList
from core.parser import dataList

frameFilter = ['android/', 'com/google/android/', 'java/', 'javax/', 'junit/', 'org/apache/', 'org/json/', 'org/w3c/dom/', 'org/xml/', 'dalvik/', 'com/google/firebase/', 'org/xmlpull/']

class ASTGraph():
    
    def __init__(self, nodeList, edgeList, config = None):
        self.nodeList = nodeList
        self.edgeList = edgeList
        self.graph = None
        self.config = config

    def graph_initialize(self, method_name, encode_flag = False):
        if encode_flag and self.config.MAX_NODE_COUNT < len(self.nodeList):
            print(set_string_colored('Increase the graph configuration for MAX_NODE_COUNT', Color.RED.value))
            return

        self.graph = nx.DiGraph()
        
        # #with open('/root/workDir/ASTParser/core/frame_cls.txt','r') as f:
        # with open('../../AST_parser/ASTParser/core/frame_cls.txt','r') as f:
        #     frame = f.read().split()
        # frame = list(frame)

# origin
#         if not encode_flag:
#             # for node in self.nodeList:
#             # 	self.graph.add_node(node)

#             for edge in self.edgeList:
#                 if edge.pIndex == -1: # 
#                     self.graph.add_edge(
#                         str(edge.pIndex) + ':' + method_name#'ROOT'
#                         , str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
#                 else: 
#                     if type(self.nodeList[edge.cIndex].nodeInfo) != type(ConstData(None, None)): # action, statement
#                         self.graph.add_edge(
#                             str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
#                             , str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
#                     else:
#                         #요기다가 조건걸고 검색하고 뭉게기  if self.nodeList[edge.pIndex].nodeInfo.type 로 타입 체크하고 self.nodeList[edge.cIndex].nodeInfo.type이 parser.py에 정의된 뭐시기일때 뭉게기
#                         self.graph.add_edge(
#                             str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
#                             , str(edge.cIndex) + ':' + str(self.nodeList[edge.cIndex].nodeInfo.value))

# custom
        if not encode_flag:
            # for node in self.nodeList:
            # 	self.graph.add_node(node)

            for edge in self.edgeList:
                if edge.pIndex == -1: # 
                    self.graph.add_edge(
                        str(edge.pIndex) + ':' + method_name#'ROOT'
                        , str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
                else: 
                    if type(self.nodeList[edge.cIndex].nodeInfo) != type(ConstData(None, None)): # action, statement
                        self.graph.add_edge(
                            str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                            , str(edge.cIndex) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
                    else:
                        #요기다가 조건걸고 검색하고 뭉게기  if self.nodeList[edge.pIndex].nodeInfo.type 로 타입 체크하고 self.nodeList[edge.cIndex].nodeInfo.type이 parser.py에 정의된 뭐시기일때 뭉게기

                        if self.nodeList[edge.cIndex].nodeInfo.type == 'Triple':
                            triple = str(self.nodeList[edge.cIndex].nodeInfo.value[0])
                            # print(triple)
                    
                            if  self.nodeList[edge.pIndex].nodeInfo.type == 'ClassInstanceCreation':
                                for frame in frameFilter:
                                    if triple.startswith(frame):
                                        self.graph.add_edge(
                                            str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                            , str(edge.cIndex) + ': '+ 'Framework_API')
                                    
                                else:
                                    self.graph.add_edge(
                                        str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                        , str(edge.cIndex) + ':' + str(self.nodeList[edge.cIndex].nodeInfo.value[1]))
                                
                            elif self.nodeList[edge.pIndex].nodeInfo.type == 'MethodInvocation':
                                for frame in frameFilter:
                                    if triple.startswith(frame):
                                        self.graph.add_edge(
                                            str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                            , str(edge.cIndex) + ': '+ 'Framework_API')                    
           
                                else:
                                    self.graph.add_edge(
                                        str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                        , str(edge.cIndex) + ':' + str(self.nodeList[edge.cIndex].nodeInfo.value[1]))
                     
                                param_type = str(self.nodeList[edge.cIndex].nodeInfo.value[-1]).split(')')[0]
                                param_type = param_type.replace('(','')

                                if not param_type:
                                    param_type = 'void'

                                self.graph.add_edge(
                                    str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                    , str(edge.cIndex) + ':' + param_type)

                                ret_type = str(self.nodeList[edge.cIndex].nodeInfo.value[-1]).split(')')[-1]
                                    
                                if not ret_type:
                                        ret_type = 'void'

                                self.graph.add_edge(
                                    str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                    , str(edge.cIndex) + ':' + ret_type)                                                       
                                
                            elif self.nodeList[edge.pIndex].nodeInfo.type == 'FieldAccess':
                                for frame in frameFilter:
                                    if triple.startswith(frame):
                                        self.graph.add_edge(
                                            str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                            , str(edge.cIndex) + ': '+ 'Framework_API')

                                else:
                                    #api = str(self.nodeList[edge.cIndex].nodeInfo.value[1])+str(self.nodeList[edge.cIndex].nodeInfo.value[-1])
                                    if '(' in str(self.nodeList[edge.cIndex].nodeInfo.value[-1]):
                                        api = str(self.nodeList[edge.cIndex].nodeInfo.value[0])+'/'+str(self.nodeList[edge.cIndex].nodeInfo.value[1])+str(self.nodeList[edge.cIndex].nodeInfo.value[-1])
                                    else:
                                        api = str(self.nodeList[edge.cIndex].nodeInfo.value[0])+'/'+str(self.nodeList[edge.cIndex].nodeInfo.value[1])+':'+str(self.nodeList[edge.cIndex].nodeInfo.value[-1])

                                    self.graph.add_edge(
                                        str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                        , str(edge.cIndex) + ':' + api)
                                
                        elif self.nodeList[edge.pIndex].nodeInfo.type == 'FieldAccess' and self.nodeList[edge.cIndex].nodeInfo.type == 'TypeName':
                            type_name = str(self.nodeList[edge.cIndex].nodeInfo.value)
                            # print(type_name)
                            
                            for frame in frameFilter:
                                    if type_name.startswith(frame):
                                        self.graph.add_edge(
                                            str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                            , str(edge.cIndex) + ': '+ 'Framework_API')
                            else:
                                self.graph.add_edge(
                                    str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                    , str(edge.cIndex) + ': '+ str(self.nodeList[edge.cIndex].nodeInfo.value))
                            
                        elif self.nodeList[edge.pIndex].nodeInfo.type == 'MethodInvocation' and self.nodeList[edge.cIndex].nodeInfo.type == 'APIName':
                            pass
                            
                        else:
                            self.graph.add_edge(
                                str(edge.pIndex) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                                , str(edge.cIndex) + ':' + str(self.nodeList[edge.cIndex].nodeInfo.value))
                        

        else: # index숫자질
            for edge in self.edgeList:
                if edge.pIndex == -1:
                    self.graph.add_edge(
                        str(self.cal_labeled_index(edge.pIndex)) + ':' + method_name#'ROOT'
                        , str(self.cal_labeled_index(edge.cIndex)) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
                else:
                    if type(self.nodeList[edge.cIndex].nodeInfo) != type(ConstData(None, None)):  # action, statement
                        self.graph.add_edge(
                            str(self.cal_labeled_index(edge.pIndex)) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                            , str(self.cal_labeled_index(edge.cIndex)) + ':' + self.nodeList[edge.cIndex].nodeInfo.type)
                    else:
                        self.graph.add_edge(
                            str(self.cal_labeled_index(edge.pIndex)) + ':' + self.nodeList[edge.pIndex].nodeInfo.type
                            , str(self.cal_labeled_index(edge.cIndex)) + ':' + str(self.nodeList[edge.cIndex].nodeInfo.value))

    def cal_labeled_index(self, index):
        nodeType = self.nodeList[index].nodeInfo.type

        if nodeType in stmtList:
            return stmtList.index(nodeType) * self.config.TYPE_WINDOW_SIZE + index
        elif nodeType in actionList:
            return (actionList.index(nodeType) + 20) * self.config.TYPE_WINDOW_SIZE + index
        elif nodeType in dataList:
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