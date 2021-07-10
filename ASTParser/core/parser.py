from pprint import pprint
from copy import deepcopy as copy_instance

from core.statements import Statement
from core.statements import BlockStatement
from core.statements import ExpressionStatement
from core.statements import LocalDeclarationStatement
from core.statements import ReturnStatement
from core.statements import ThrowStatement
from core.statements import JumpStatement
from core.statements import DoStatement
from core.statements import WhileStatement
from core.statements import TryStatement
from core.statements import IfStatement
from core.statements import SwitchStatement
from core.statements import BlockStatement

from core.actions import Action

from core.utils import Color
from core.utils import set_string_colored

stmtList = [
        'ExpressionStatement',
        'LocalDeclarationStatement',
        'ReturnStatement',
        'ThrowStatement',
        'JumpStatement',
        'DoStatement',
        'WhileStatement',
        'TryStatement',
        'IfStatement',
        'SwitchStatement',
        'BlockStatement',
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
        'ClassInstanceCreation' # TODO: Analyze this case
        ]


class ASTParser():
    def __init__(self, flag = False):
        self.isDebug = flag
        self.ast = None
        self.errMsg = ''
        self.parsedNodes = list()
        self.parsedEdges = list()

    def print_parsing_error(self, errType):
        if errType == 1:
            self.errMsg = 'AST is not loaded, so you have to load it first'
        elif errorType == 2:
            self.errMsg = 'Wrong formmated AST is entered'
        elif errorType == 3:
            self.errMsg = 'The TryStatement has no pairs'
        elif errorType == 4:
            self.errMsg = 'The switchStatement has no ksv_pairs'
        else :
            self.errMsg = 'TODO'

        print(set_string_colored(self.errMsg, Color.RED.value))

    def load_ast(self, ast):
        self.ast = ast['body']

    def parse_ast(self):
        if self.isDebug:
            print(set_string_colored('DP Check : function: parse_ast is invoked', Color.GREEN.value))

        # self.initialize_ast()
        self.visit_tree(self.ast)

        if self.isDebug:
            print(len(self.parsedNodes))
        
    def visit_tree(self, ast):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_tree is invoked', Color.GREEN.value))
            print(set_string_colored("DP Check : " + str(ast), Color.GREEN.value))

            pprint(ast)

        if ast is None:
            return

        if ast[0] in stmtList:
            self.visit_statments(ast)
        elif ast[0] in actionList:
            self.visit_actions(ast)
        else:
            pass

    def visit_statments(self, astBlock):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_statments is invoked', Color.GREEN.value))
            pprint(astBlock)

        if astBlock[0] == 'BlockStatement':
            stmt = copy_instance(astBlock)
            stmt[2] = 'extended'

            bs = BlockStatement(stmt)
            stmtNode = ASTNode(bs, len(self.parsedNodes))

            self.parsedNodes.append(stmtNode)

            for subTree in astBlock[2]:
                self.visit_tree(subTree)

        elif astBlock[0] == 'ExpressionStatement':
            stmt = copy_instance(astBlock)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                es = ExpressionStatement(stmt)
                stmtNode = ASTNode(es, len(self.parsedNodes))

                self.parsedNodes.append(stmtNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                es = ExpressionStatement(stmt)
                stmtNode = ASTNode(es, len(self.parsedNodes))

                self.parsedNodes.append(stmtNode)

        elif astBlock[0] == 'LocalDeclarationStatement':
            stmt = copy_instance(astBlock)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                lds = LocalDeclarationStatement(stmt)
                stmtNode = ASTNode(lds, len(self.parsedNodes))

                self.parsedNodes.append(stmtNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                lds = LocalDeclarationStatement(stmt)
                stmtNode = ASTNode(lds, len(self.parsedNodes))

                self.parsedNodes.append(stmtNode)

        elif astBlock[0] == 'ReturnStatement':
            stmt = copy_instance(astBlock)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                rs = ReturnStatement(stmt)
                stmtNode = ASTNode(rs, len(self.parsedNodes))

                self.parsedNodes.append(stmtNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                rs = ReturnStatement(stmt)
                stmtNode = ASTNode(rs, len(self.parsedNodes))

                self.parsedNodes.append(stmtNode)

        elif astBlock[0] == 'ThrowStatement':
            stmt = copy_instance(astBlock)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                ts = ThrowStatement(stmt)
                stmtNode = ASTNode(ts, len(self.parsedNodes))

                self.parsedNodes.append(stmtNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                ts = ThrowStatement(stmt)
                stmtNode = ASTNode(ts, len(self.parsedNodes))

                self.parsedNodes.append(stmtNode)

        elif astBlock[0] == 'JumpStatement':
            stmt = copy_instance(astBlock)

            js = JumpStatement(stmt)
            stmtNode = ASTNode(js, len(self.parsedNodes))

            self.parsedNodes.append(stmtNode)

        elif astBlock[0] == 'DoStatement':
            stmt = copy_instance(astBlock)

            doStmtNodeIndex = len(self.parsedNodes)

            # Branch for control expression
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                ds = DoStatement(stmt)
                stmtNode = ASTNode(ds, doStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[2])
            else:
                ds = DoStatement(stmt)
                stmtNode = ASTNode(ds, doStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

            # Branch for scopes(body) expression
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[doStmtNodeIndex].data.update_doStatement(stmt)
                else:
                    ds = DoStatement(stmt)
                    stmtNode = ASTNode(ds, doStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[3])

        elif astBlock[0] == 'WhileStatement':
            stmt = copy_instance(astBlock)

            whileStmtNodeIndex = len(self.parsedNodes)

            # Branch for control expression
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                ws = WhileStatement(stmt)
                stmtNode = ASTNode(ws, whileStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[2])
            else:
                ws = WhileStatement(stmt)
                stmtNode = ASTNode(ws, whileStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

            # Branch for scopes(body) expression
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[whileStmtNodeIndex].data.update_whileStatement(stmt)
                else:
                    ws = WhileStatement(stmt)
                    stmtNode = ASTNode(ws, whileStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[3])

        ## TODO : How to handle and how to interpret the pair formed data
        elif astBlock[0] == 'TryStatement':
            stmt = copy_instance(astBlock)

            tryStmtNodeIndex = len(self.parsedNodes)

            # Branch for try block
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                ts = TryStatement(stmt)
                stmtNode = ASTNode(ts, tryStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[2])
            else:
                ts = TryStatement(stmt)
                stmtNode = ASTNode(ts, tryStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

            # Branch for pairs
            # TODO : pairs is??
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[tryStmtNodeIndex].data.update_tryStatement(stmt)
                else:
                    ts = TryStatement(stmt)
                    stmtNode = ASTNode(ts, tryStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if astBlock[3] is None:
                    print_parsing_error(3)
                else:
                    self.visit_pairs(astBlock[3])


        elif astBlock[0] == 'IfStatement':
            stmt = copy_instance(astBlock)

            ifStmtNodeIndex = len(self.parsedNodes)

            # Branch for control expression
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                ifs = IfStatement(stmt)
                stmtNode = ASTNode(ifs, ifStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[2])
            else:
                ifs = IfStatement(stmt)
                stmtNode = ASTNode(ifs, ifStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

            # Branch for scopes(body) expression
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[ifStmtNodeIndex].data.update_ifStatement(stmt)
                else:
                    ifs = IfStatement(stmt)
                    stmtNode = ASTNode(ifs, ifStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[3])

        elif astBlock[0] == 'SwitchStatement':
            stmt = copy_instance(astBlock)

            switchStmtNodeIndex = len(self.parsedNodes)

            # Branch for try block
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                ss = SwitchStatement(stmt)
                stmtNode = ASTNode(ss, switchStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[2])
            else:
                ss = SwitchStatement(stmt)
                stmtNode = ASTNode(ss, switchStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

            # Branch for pairs
            # TODO : pairs is??
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[switchStmtNodeIndex].data.update_switchStatement(stmt)
                else:
                    ss = SwitchStatement(stmt)
                    stmtNode = ASTNode(ss, switchStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if astBlock[3] is None:
                    print_parsing_error(3)
                else:
                    self.visit_pairs(astBlock[3])

    def visit_actions(self, astBlock):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_actions is invoked', Color.GREEN.value))
            pprint(astBlock)

        tmp_instance = copy_instance(astBlock)

        tmp_action = Action(tmp_instance)

        actionNode = ASTNode(tmp_action, len(self.parsedNodes))
        self.parsedNodes.append(actionNode)

        if astBlock[0] == 'ArrayAccess':
            pass

        elif astBlock[0] == 'ArrayCreation':
            pass

        elif astBlock[0] == 'ArrayInitializer':
            pass

        elif astBlock[0] == 'Assignment':
            pass

        elif astBlock[0] == 'BinaryInfix':
            pass

        elif astBlock[0] == 'Cast':
            pass

        elif astBlock[0] == 'FieldAccess':
            pass

        elif astBlock[0] == 'Literal':
            pass

        elif astBlock[0] == 'Local':
            pass
            
        elif astBlock[0] == 'MethodInvocation':
            pass

        elif astBlock[0] == 'Parenthesis':
            pass

        elif astBlock[0] == 'TypeName':
            pass

        elif astBlock[0] == 'Unary':
            pass

        else:
            pass

    def visit_pairs(self, tupleList):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_pairs is invoked', Color.GREEN.value))
            pprint(tupleList)

        for pairTuple in tupleList:
            for t in pairTuple:
                if type(t[0]) == type(list()):
                    for subTree in t:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(t)

    def show_whole_ast(self):
        if self.ast:
            pprint(self.ast)
        else:
            self.print_parsing_error(1)


# Class for parsed node of AST
class ASTNode():
    def __init__(self, data, index):
        self.data = data
        self.index = index

# Class for managing the edge information among the parsedNodes of AST
class ASTEdge():
    def __init__(self, pIndex, cIndex):
        self.pIndex = pIndex
        self.cIndex = cIndex