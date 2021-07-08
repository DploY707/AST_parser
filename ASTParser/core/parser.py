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
from core.statements import SwitchStatement
from core.statements import BlockStatement

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
        ]


class ASTParser():
    def __init__(self):
        self.ast = None
        self.errMsg = ''
        self.parsedNodes = list()
        self.parsedEdges = list()

    def print_parsing_error(self, errType):
        if errType == 1:
            self.errMsg = 'AST is not loaded, so you have to load it first'
        elif errorType == 2:
            self.errMsg = 'Wrong formmated AST is entered'
        else :
            self.errMsg = 'TODO'

        print(set_string_colored(self.errMsg, Color.RED.value))

    def load_ast(self, ast):
        self.ast = ast['body']

    def parse_ast(self):
        print(set_string_colored('DP Check : function: parse_ast is invoked', Color.GREEN.value))

        # self.initialize_ast()
        self.visit_tree(self.ast)

        print(len(self.parsedNodes))
        
    def visit_tree(self, ast):
        print(set_string_colored('DP Check : function: visit_tree is invoked', Color.GREEN.value))
        print(set_string_colored("DP Check : " + str(ast), Color.GREEN.value))

        pprint(ast)

        if ast[0] in stmtList:
            self.visit_statments(ast)
        elif ast[0] in actionList:
            self.visit_actions(ast)
        else:
            pass
        '''
        if type(ast) == type(list()):
            for subTree in ast:
                if subTree[0] in stmtList:
                    self.visit_statments(subTree)
                elif subTree[0] in actionList:
                    self.visit_actions(subTree)
                else:
                    pass
        else:
            if ast in stmtList:
                self.visit_statments(subTree)
            elif ast in actionList:
                self.visit_actions(subTree)
            else:
                pass
        '''

    def visit_statments(self, astBlock):
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
            pass

        elif astBlock[0] == 'DoStatement':
            pass

        elif astBlock[0] == 'WhileStatement':
            pass

        elif astBlock[0] == 'TryStatement':
            pass

        elif astBlock[0] == 'IfStatement':
            stmt = copy_instance(astBlock)

        elif astBlock[0] == 'SwitchStatement':
            pass

    def visit_actions(self, astBlock):
        print(set_string_colored('DP Check : function: visit_actions is invoked', Color.GREEN.value))
        pprint(astBlock)

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


    def show_whole_ast(self):
        if self.ast:
            pprint(self.ast)
        else:
            self.print_parsing_error(1)


# Class for parsed node of AST
class ASTNode():
    def __init__(self, stmt, index):
        self.stmt = stmt
        self.index = index
        