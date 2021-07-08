from pprint import pprint
import json
import gzip
import pickle
import copy

from androguard.decompiler.dad.decompile import DvMethod
from androguard.misc import AnalyzeAPK

import networkx as nx

targetPath = '/root/workDir/data/okhttp-3.1.0_dex.jar'
resultPath = './out.pickle'

BLOCKSTAT = 'BlockStatement'

stmtList_no_expr = [
        'JumpStatement',
        ]

stmtList_expr_in_1st = [
        'ExpressionStatement',
        'LocalDeclarationStatement',
        'ReturnStatement',
        'ThrowStatement',
        ]

#Condition Stat
stmtList_expr_in_2nd = [
        'DoStatement',
        'WhileStatement',
        'TryStatement',
        'IfStatement',
        'SwitchStatement',
        ]

actionList = [
        'ArrayAccess',
        'ArrayCreation',
        'ArrayInitializer',
        'Assignment',
        'BinaryInfix',
        'Cast',
        'FieldAccess',
        'Literal',
        'Local',
        'MethodInvocation',
        'Parenthesis',
        'TypeName',
        'Unary',
        'Dummy',
        ]

def create_ast(method):
    if method.is_external():
        return
    try:
        dv = DvMethod(method)
        dv.process(doAST=True)

        return dv.get_ast()

    except AttributeError as ae:
        print('ERROR : in creat_ast()')

def parse_ast(ast) :
    contents = ast['body']
    parsed_tree = bfs_for_ast(contents)

def bfs_for_ast(contents):
    if contents[0] == BLOCKSTAT:
        bfs_for_blockStat_ast(contents[2])
    else:
        bfs_for_normalStat_ast(contents)

def bfs_for_blockStat_ast(contents):
    for content in contents:
        bfs_for_ast(content)

def bfs_for_ifStat_cond_ast(contents):
    print(contents)

def bfs_for_ifStat_scope_ast(contents):
    print(contents)

def bfs_for_switch_cond_ast(contents):
    print(contents)

def bfs_for_switch_ksv_ast(contents):
    print(contents)

def bfs_for_normalStat_ast(contents) :
    if contents[0] in stmtList_no_expr:
        print("DP : ", contents)
    elif contents[0] in stmtList_expr_in_1st:
        if type(contents[1]) is type(list()):
            ext_content = copy.deepcopy(contents)
            ext_content[1] = 'extended'
            print("DP : ", ext_content)

            bfs_for_ast(contents[1])
        else:
            print("DP : ", contents)
    elif contents[0] in stmtList_expr_in_2nd:
        if type(contents[2]) is type(list()):
            ext_content = copy.deepcopy(contents)
            ext_content[2] = 'extended'
            print("DP : ", ext_content)

            bfs_for_ast(contents[2])
        else:
            print("DP : ", contents)
    else:
        print("DP : ", contents)

def save_ast():
    with gzip.open(resultPath,'wb') as f:
        pickle.dump(tot, f)

if __name__ == '__main__' :
    a, d, dx = AnalyzeAPK(targetPath)

    for method in dx.get_methods():
        m_ast = create_ast(method)
        parse_ast(m_ast)
        break
