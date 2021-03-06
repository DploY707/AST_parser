from pprint import pprint
import json
import gzip
import pickle
import copy

from androguard.decompiler.dad.decompile import DvMethod
from androguard.misc import AnalyzeAPK

from core.parser import ASTParser
from core.parser import ConstData

from core.parser import stmtList
from core.parser import actionList
from core.parser import dataList

from core.statements import Statement

from core.graph import ASTGraph
from core.graph import GraphConfig

from core.utils import save_pickle, load_pickle
from core.utils import get_filteredFileList_from_directory as get_targets

import networkx as nx

targetPath = 'data/'
target = 'data/okhttp-3.1.0_dex.jar'
resultPath = '/root/result/'

targetExts = ['.apk', '.jar']

# config = GraphConfig(10000,20000)

def create_ast(method):
    if method.is_external():
        return
    try:
        dv = DvMethod(method)
        dv.process(doAST=True)

        return dv.get_ast()

    except AttributeError as ae:
        print('ERROR : in creat_ast()')

if __name__ == '__main__' :
    targetList = get_targets(targetPath, targetExts)

    for target in targetList:
        a, d, dx = AnalyzeAPK(target)

        t_count = 0

        graphList = list()

        for method in dx.get_methods():
            m_ast = create_ast(method)

            ap = ASTParser()
            
            if m_ast is not None:
                ap.load_ast(m_ast)
                ap.parse_ast()

                # for node in ap.parsedNodes:
                #     if 'APIName' == node.nodeInfo.type:
                #         pprint(node.nodeInfo)

                # for edge in ap.parsedEdges:
                    # pprint(edge)

            # ag = ASTGraph(ap.parsedNodes, ap.parsedEdges, config)
            ag = ASTGraph(ap.parsedNodes, ap.parsedEdges)
            ag.graph_initialize()

            # encode_flag makes the index of edges meaningful
            # ag.graph_initialize(encode_flag = True)

            if ag.graph == None:
                pass
            else:
                graphList.append(ag.graph)

        save_pickle(resultPath + target.split('/')[1] + '.pickle', graphList)

