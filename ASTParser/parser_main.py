from pprint import pprint
import json
import gzip
import pickle
import copy

from androguard.decompiler.dad.decompile import DvMethod
from androguard.misc import AnalyzeAPK

from core.parser import ASTParser
from core.statements import Statement

from core.parser import ConstData

from core.graph import ASTGraph

import networkx as nx

targetPath = 'data/okhttp-3.1.0_dex.jar'
resultPath = './out.pickle'

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
    a, d, dx = AnalyzeAPK(targetPath)

    t_count = 0

    for method in dx.get_methods():
        m_ast = create_ast(method)

        ap = ASTParser()
        
        if m_ast is not None:
            ap.load_ast(m_ast)
            ap.parse_ast()

            # for node in ap.parsedNodes:
                # pprint(node.nodeInfo)

            # for edge in ap.parsedEdges:
                # pprint(edge)

        ag = ASTGraph(ap.parsedNodes, ap.parsedEdges)
        ag.graph_initialize()

        ag.save_graph_png('./' + str(ap).split(' ')[-1] + '.png')

        break