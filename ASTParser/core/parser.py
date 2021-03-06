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
from core.actions import ArrayAccess
from core.actions import ArrayCreation
from core.actions import ArrayInitializer
from core.actions import Assignment
from core.actions import BinaryInfix
from core.actions import Cast
from core.actions import FieldAccess
from core.actions import Literal
from core.actions import Local
from core.actions import MethodInvocation
from core.actions import Parenthesis
from core.actions import TypeName
from core.actions import Unary
from core.actions import Dummy
from core.actions import ClassInstanceCreation

from core.utils import Color
from core.utils import set_string_colored

stmtList = [
        'BlockStatement',
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

dataList = [
        'Keyword', # This case is for JumpStatement
        'Dimension', # This case if for ArrayCreation, the dimension of array should be 1
        'OP', # This case is for Assignment / Binaryinfix
        'Triple', # This case is for FieldAccess
        'Type', # This case is for Literal
        'APIName', # This case is for MethodInvocation
        'Register',
        'Value',
        # 'Class',
        # 'Method',
        ]

class ASTParser():
    def __init__(self, flag = False):
        self.isDebug = flag
        self.ast = None
        self.errMsg = ''
        self.parsedNodes = list()
        self.parsedEdges = list()
        self.entryFlag = True

    def print_parsing_error(self, errorType):
        # Errors in large scale
        if errorType == -1:
            self.errMsg = 'ERR_NO(-1): AST has wrong statement data'
        elif errorType == -2:
            self.errMsg = 'ERR_NO(-2): AST has wrong action data'
        elif errorType == -3:
            self.errMsg = 'ERR_NO(-3): Invalied node index value is used on connecting edges'
        elif errorType == -4:
            self.errMsg = 'ERR_NO(-4): Unexpected ConstNode is created'

        # Error that AST is not loaded
        elif errorType == 0:
            self.errMsg = 'ERR_NO(0): AST is not loaded, so you have to load it first'
        
        # Error on parsing statements
        elif errorType == 10:
            self.errMsg = 'ERR_NO(10): Wrong operand in BlockStatement'
        elif errorType == 20:
            self.errMsg = 'ERR_NO(20): Wrong operand in ExpressionStatement'
        elif errorType == 30:
            self.errMsg = 'ERR_NO(30): Wrong operand in LocalDeclarationStatement(decl)'
        elif errorType == 40:
            self.errMsg = 'ERR_NO(40): Wrong operand in ReturnStatement'
        elif errorType == 50:
            self.errMsg = 'ERR_NO(50): Wrong operand in ThrowStatement'
        elif errorType == 60:
            self.errMsg = 'ERR_NO(60): Wrong operand in JumpStatement (keyword is not break)'
        elif errorType == 70:
            self.errMsg = 'ERR_NO(70): Wrong operand in DoStatement(cond_expr)'
        elif errorType == 71:
            self.errMsg = 'ERR_NO(71): Wrong operand in DoStatement(body_expr)'
        elif errorType == 80:
            self.errMsg = 'ERR_NO(80): Wrong operand in WhileStatement(cond_expr)'
        elif errorType == 81:
            self.errMsg = 'ERR_NO(81): Wrong operand in WhileStatement(body_expr)'
        elif errorType == 90:
            self.errMsg = 'ERR_NO(90): Wrong operand in TryStatement(tryb_expr)'
        elif errorType == 91:
            self.errMsg = 'ERR_NO(91): Wrong operand in TryStatement(pairs_expr)'
        elif errorType == 92:
            self.errMsg = 'ERR_NO(92): Wrong operand in TryStatement(pairs_expr), pairs_expr is None'
        elif errorType == 100:
            self.errMsg = 'ERR_NO(100): Wrong operand in IfStatement(cond_expr)'
        elif errorType == 101:
            self.errMsg = 'ERR_NO(101): Wrong operand in IfStatement(body_expr)'
        elif errorType == 110:
            self.errMsg = 'ERR_NO(110): Wrong operand in SwitchStatement(cond_expr)'
        elif errorType == 111:
            self.errMsg = 'ERR_NO(111): Wrong operand in SwitchStatement(ksv_pairs)'
        elif errorType == 112:
            self.errMsg = 'ERR_NO(112): Wrong operand in SwitchStatement(ksv_pairs), ksv_pairs is None'

        # Error on parsing actions
        elif errorType == 1010:
            self.errMsg = 'ERR_NO(1010): Wrong operand in ArrayAccess(arr)'
        elif errorType == 1011:
            self.errMsg = 'ERR_NO(1011): Wrong operand in ArrayAccess(ind)'
        elif errorType == 1020:
            self.errMsg = 'ERR_NO(1020): Wrong operand in ArrayCreation(tn_and_params)'
        elif errorType == 1030:
            self.errMsg = 'ERR_NO(1030): Wrong operand in ArrayInitializer(params)'
        elif errorType == 1031:
            self.errMsg = 'ERR_NO(1031): Wrong operand in ArrayInitializer(tn), tn is a list'
        elif errorType == 1040:
            self.errMsg = 'ERR_NO(1040): Wrong operand in Assignment(lhs)'
        elif errorType == 1041:
            self.errMsg = 'ERR_NO(1041): Wrong operand in Assignment(rhs)'
        elif errorType == 1042:
            self.errMsg = 'ERR_NO(1042): Wrong operand in Assignment(op), op is list() data'
        elif errorType == 1050:
            self.errMsg = 'ERR_NO(1050): Wrong operand in BinaryInfix(left)'
        elif errorType == 1051:
            self.errMsg = 'ERR_NO(1051): Wrong operand in BinaryInfix(right)'
        elif errorType == 1052:
            self.errMsg = 'ERR_NO(1052): Wrong operand in BinaryInfix(op), op is list() data'
        elif errorType == 1060:
            self.errMsg = 'ERR_NO(1060): Wrong operand in Cast(tn)'
        elif errorType == 1061:
            self.errMsg = 'ERR_NO(1061): Wrong operand in Cast(arg)'
        elif errorType == 1070:
            self.errMsg = 'ERR_NO(1070): Wrong operand in FieldAccess(left)'
        elif errorType == 1071:
            self.errMsg = 'ERR_NO(1071): Wrong operand in FieldAccess(triple)'
        elif errorType == 1080:
            self.errMsg = 'ERR_NO(1080): Wrong operand in Literal(tt), tt is not tuple with length == 2'
        elif errorType == 1090:
            self.errMsg = 'ERR_NO(1090): Wrong operand in Local(name), name is None or list() data'
        elif errorType == 1091:
            self.errMsg = 'ERR_NO(1091): Wrong operand in Local(name), name is un-handled foramt'
        elif errorType == 1100:
            self.errMsg = 'ERR_NO(1100): Wrong operand in MethodInvocation(params)'
        elif errorType == 1101:
            self.errMsg = 'ERR_NO(1101): Wrong operand in MethodInvocation(triple)'
        elif errorType == 1110:
            self.errMsg = 'ERR_NO(1110): Wrong operand in Parenthesis(expr_arr)'
        elif errorType == 1120:
            self.errMsg = 'ERR_NO(1120): Wrong operand in TypeName(baset_and_dim)'
        elif errorType == 1130:
            self.errMsg = 'ERR_NO(1130): Wrong operand in Unary(left_arr)'
        elif errorType == 1131:
            self.errMsg = 'ERR_NO(1131): Wrong operand in Unary(OP)'
        elif errorType == 1140:
            self.errMsg = 'ERR_NO(1140): Wrong operand in Dummy'
        elif errorType == 1141:
            self.errMsg = 'ERR_NO(1141): Wrong operand in Dummy, str(desc)'
        elif errorType == 1142:
            self.errMsg = 'ERR_NO(1142): Wrong operand in Dummy, ??? Unexpected constant'
        elif errorType == 1143:
            self.errMsg = 'ERR_NO(1143): Wrong operand in Dummy, monitor enter'
        elif errorType == 1144:
            self.errMsg = 'ERR_NO(1144): Wrong operand in Dummy, monitor exit'
        elif errorType == 1145:
            self.errMsg = 'ERR_NO(1145): Wrong operand in Dummy, new'
        elif errorType == 1146:
            self.errMsg = 'ERR_NO(1146): Wrong operand in Dummy, ??? Unexpected op'
        elif errorType == 1150:
            self.errMsg = 'ERR_NO(1150): Wrong operand in ClassInstanceCreation(triple)'
        elif errorType == 1151:
            self.errMsg = 'ERR_NO(1151): Wrong operand in ClassInstanceCreation(params)'
        elif errorType == 1152:
            self.errMsg = 'ERR_NO(1152): Wrong operand in ClassInstanceCreation(parse_descriptor)'

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
        
    def visit_tree(self, ast, pIndex = -1):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_tree is invoked', Color.GREEN.value))
            print(set_string_colored("DP Check : " + str(ast), Color.GREEN.value))

            pprint(ast)

        if ast is None:
            return

        # DP DEBUG:
        # if pIndex != -1:
            # print(pIndex)

        if ast[0] in stmtList:
            self.visit_statments(ast, pIndex)
        elif ast[0] in actionList:
            self.visit_actions(ast, pIndex)
        else:
            if self.parsedNodes[pIndex].nodeInfo.type == 'BlockStatement':
                # In this case, the elemnets in the ast should be a value not a list!!!
                constValueNodeIndex = len(self.parsedNodes)

                if type(ast) != type(list()):
                    self.print_parsing_error(-4)
                    print(set_string_colored(str(ast), Color.RED.value))
                    return

                for const_value in ast:
                    cv = ConstData(str(const_value), 'Value')
                    constNode = ASTNode(cv, constValueNodeIndex)

                    self.parsedNodes.append(constNode)
                    self.create_edges(pIndex, constValueNodeIndex, None)

                    constValueNodeIndex += 1
            else:
                self.print_parsing_error(-4)

    def visit_statments(self, astBlock, pIndex):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_statments is invoked', Color.GREEN.value))
            pprint(astBlock)

        if astBlock[0] == 'BlockStatement':
            stmt = copy_instance(astBlock)

            if len(astBlock[2]) == 0:
                empty_list = ['EMPTY_LIST']
                astBlock[2].append(empty_list)

            blockStmtNodeIndex = len(self.parsedNodes)

            bs = BlockStatement(stmt)
            stmtNode = ASTNode(bs, blockStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, blockStmtNodeIndex, None)

            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                for subTree in astBlock[2]:
                    self.visit_tree(subTree, blockStmtNodeIndex)
            else:
                self.print_parsing_error(10)

        elif astBlock[0] == 'ExpressionStatement':
            stmt = copy_instance(astBlock)

            exprStmtNodeIndex = len(self.parsedNodes)

            es = ExpressionStatement(stmt)
            stmtNode = ASTNode(es, exprStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, exprStmtNodeIndex, None)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, exprStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[1], exprStmtNodeIndex)
            else:
                self.print_parsing_error(20)

        elif astBlock[0] == 'LocalDeclarationStatement':
            stmt = copy_instance(astBlock)

            localDeclStmtNodeIndex = len(self.parsedNodes)

            lds = LocalDeclarationStatement(stmt)
            stmtNode = ASTNode(lds, localDeclStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, localDeclStmtNodeIndex, None)

            # Branch for expr
            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, localDeclStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[1], localDeclStmtNodeIndex)
        
            # Branch for decl
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree, localDeclStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[2], localDeclStmtNodeIndex)
            else:
                self.print_parsing_error(30)

        elif astBlock[0] == 'ReturnStatement':
            stmt = copy_instance(astBlock)

            returnStmtNodeIndex = len(self.parsedNodes)

            rs = ReturnStatement(stmt)
            stmtNode = ASTNode(rs, returnStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, returnStmtNodeIndex, None)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, returnStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[1], returnStmtNodeIndex)

        elif astBlock[0] == 'ThrowStatement':
            stmt = copy_instance(astBlock)

            throwStmtNodeIndex = len(self.parsedNodes)

            ts = ThrowStatement(stmt)
            stmtNode = ASTNode(ts, throwStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, throwStmtNodeIndex, None)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, throwStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[1], throwStmtNodeIndex)
            else:
                self.print_parsing_error(50)

        elif astBlock[0] == 'JumpStatement':
            stmt = copy_instance(astBlock)

            jmpStmtNodeIndex = len(self.parsedNodes)

            js = JumpStatement(stmt)
            stmtNode = ASTNode(js, jmpStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, jmpStmtNodeIndex, None)

            if astBlock[1] != 'break':
                self.print_parsing_error(60)
                return
            else:
                stmt[1] = 'extended'

                keywordNodeIndex = len(self.parsedNodes)

                kw = ConstData(str(astBlock[1]), 'Keyword')
                constNode = ASTNode(kw, keywordNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(jmpStmtNodeIndex, keywordNodeIndex, None)

        elif astBlock[0] == 'DoStatement':
            stmt = copy_instance(astBlock)

            doStmtNodeIndex = len(self.parsedNodes)

            ds = DoStatement(stmt)
            stmtNode = ASTNode(ds, doStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, doStmtNodeIndex, None)

            # Branch for cond_expr
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree, doStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[2], doStmtNodeIndex)
            else:
                self.print_parsing_error(70)

            # Branch for body_expr
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree, doStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[3], doStmtNodeIndex)
            else:
                self.print_parsing_error(71)

        elif astBlock[0] == 'WhileStatement':
            stmt = copy_instance(astBlock)

            whileStmtNodeIndex = len(self.parsedNodes)

            ws = WhileStatement(stmt)
            stmtNode = ASTNode(ws, whileStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, whileStmtNodeIndex, None)

            # Branch for cond_expr
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree, whileStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[2], whileStmtNodeIndex)
            else:
                self.print_parsing_error(80)

            # Branch for body_expr
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree, whileStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[3], whileStmtNodeIndex)
            else:
                self.print_parsing_error(81)

        # CHECK : what is the meaning of pair formed data
        elif astBlock[0] == 'TryStatement':
            stmt = copy_instance(astBlock)

            tryStmtNodeIndex = len(self.parsedNodes)

            ts = TryStatement(stmt)
            stmtNode = ASTNode(ts, tryStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, tryStmtNodeIndex, None)

            # Branch for tryb_expr
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree, tryStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[2], tryStmtNodeIndex)
            else:
                self.print_parsing_error(90)

            # Branch for pairs_expr
            if type(astBlock[3]) == type(list()):
                # Node Creation
                stmt[3] = 'extended'

                # Visit the pair formed expr for parsing the AST
                if astBlock[3] is None:
                    self.print_parsing_error(92)
                else:
                    self.visit_pairs(astBlock[3], pIndex)
            else:
                self.print_parsing_error(91)

        elif astBlock[0] == 'IfStatement':
            stmt = copy_instance(astBlock)

            ifStmtNodeIndex = len(self.parsedNodes)

            ifs = IfStatement(stmt)
            stmtNode = ASTNode(ifs, ifStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, ifStmtNodeIndex, None)

            # Branch for cond_expr
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree, ifStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[2], ifStmtNodeIndex)
            else:
                self.print_parsing_error(100)

            # Branch for body_expr
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree, ifStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[3], ifStmtNodeIndex)
            else:
                self.print_parsing_error(101)

        elif astBlock[0] == 'SwitchStatement':
            stmt = copy_instance(astBlock)

            switchStmtNodeIndex = len(self.parsedNodes)

            ss = SwitchStatement(stmt)
            stmtNode = ASTNode(ss, switchStmtNodeIndex)

            self.parsedNodes.append(stmtNode)
            self.create_edges(pIndex, switchStmtNodeIndex, None)

            # Branch for cond_expr
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree, switchStmtNodeIndex)
                else :
                    self.visit_tree(astBlock[2], switchStmtNodeIndex)
            else:
                self.print_parsing_error(110)

            # Branch for ksv_pairs
            # CHECK : How to interpret the meaning of pairs
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if astBlock[3] is None:
                    self.print_parsing_error(112)
                else:
                    self.visit_pairs(astBlock[3], pIndex)
            else:
                self.print_parsing_error(111)

        else:
            self.print_parsing_error(-1)

    def visit_actions(self, astBlock, pIndex):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_actions is invoked', Color.GREEN.value))
            pprint(astBlock)

        if astBlock[0] == 'ArrayAccess':
            action = copy_instance(astBlock)

            arrAccessNodeIndex = len(self.parsedNodes)

            arrayAccessAction = ArrayAccess(action)
            actionNode = ASTNode(arrayAccessAction, arrAccessNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, arrAccessNodeIndex, None)

            # Branch for arr
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                if type(astBlock[1][0][0]) == type(list()):
                    for subTree in astBlock[1][0]:
                        self.visit_tree(subTree, arrAccessNodeIndex)
                else :
                    self.visit_tree(astBlock[1][0], arrAccessNodeIndex)
            else:
                self.print_parsing_error(1010)

            # Branch for ind
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if type(astBlock[1][1][0]) == type(list()):
                    for subTree in astBlock[1][1]:
                        self.visit_tree(subTree, arrAccessNodeIndex)
                else :
                    self.visit_tree(astBlock[1][1], arrAccessNodeIndex)
            else:
                self.print_parsing_error(1011)

        elif astBlock[0] == 'ArrayCreation':
            action = copy_instance(astBlock)

            arrCreationNodeIndex = len(self.parsedNodes)

            arrayCreationAction = ArrayCreation(action)
            actionNode = ASTNode(arrayCreationAction, arrCreationNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, arrCreationNodeIndex, None)

            # Branch for tn_and_params
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, arrCreationNodeIndex)
                else :
                    self.visit_tree(astBlock[1], arrCreationNodeIndex)
            else:
                self.print_parsing_error(1020)

            # Branch for dim
            if type(astBlock[2]) == type(list()):
                action[2] = 'extended'

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree, arrCreationNodeIndex)
                else :
                    self.visit_tree(astBlock[2], arrCreationNodeIndex)
            else:
                # In this case, dim is just a const value like 1
                action[2] = 'extended'

                dimensionNodeIndex = len(self.parsedNodes)

                dim = ConstData(str(astBlock[2]), 'Dimension')
                constNode = ASTNode(dim, dimensionNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(arrCreationNodeIndex, dimensionNodeIndex, None)

        elif astBlock[0] == 'ArrayInitializer':
            action = copy_instance(astBlock)

            arrInitializerNodeIndex = len(self.parsedNodes)

            arrayInitializerAction = ArrayInitializer(action)
            actionNode = ASTNode(arrayInitializerAction, arrInitializerNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, arrInitializerNodeIndex, None)

            # Branch for params
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, arrInitializerNodeIndex)
                else :
                    self.visit_tree(astBlock[1], arrInitializerNodeIndex)
            else:
                self.print_parsing_error(1030)

            # Branch for tn
            if astBlock[2] is None:
                pass
            else:
                action[2] = 'extended'

                if type(astBlock[2]) == type(list()):
                    if type(astBlock[2][0]) == type(list()):
                        for subTree in astBlock[2]:
                            self.visit_tree(subTree, arrInitializerNodeIndex)
                    else :
                        self.visit_tree(astBlock[2], arrInitializerNodeIndex) 
                else:
                    self.print_parsing_error(1031)

        elif astBlock[0] == 'Assignment':
            action = copy_instance(astBlock)

            assignNodeIndex = len(self.parsedNodes)

            assignAction = Assignment(action)
            actionNode = ASTNode(assignAction, assignNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, assignNodeIndex, None)

            # Branch for lhs
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree, assignNodeIndex)
                else:
                    self.visit_tree(astBlock[1][0], assignNodeIndex)
            else:
                self.print_parsing_error(1040)

            # Branch for rhs
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if type(astBlock[1][1][0]) == type(list()):
                    for subTree in astBlock[1][1]:
                        self.visit_tree(subTree, assignNodeIndex)
                else :
                    self.visit_tree(astBlock[1][1], assignNodeIndex)
            else:
                self.print_parsing_error(1041)

            # Branch for op
            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(1042)
            else:
                action[2] = 'extended'

                opNodeIndex = len(self.parsedNodes)

                if astBlock[2] == '':
                    op = ConstData('NOP', 'OP')
                else:
                    op = ConstData(str(astBlock[2]), 'OP')

                constNode = ASTNode(op, opNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(assignNodeIndex, opNodeIndex, None)

        elif astBlock[0] == 'BinaryInfix':
            action = copy_instance(astBlock)

            binInfixNodeIndex = len(self.parsedNodes)

            binaryInfixAction = BinaryInfix(action)
            actionNode = ASTNode(binaryInfixAction, binInfixNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, binInfixNodeIndex, None)

            # Branch for left
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree, binInfixNodeIndex)
                else :
                    self.visit_tree(astBlock[1][0], binInfixNodeIndex)
            else:
                self.print_parsing_error(1050)

            # Branch for right
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if type(astBlock[1][1][0]) == type(list()):
                    for subTree in astBlock[1][1]:
                        self.visit_tree(subTree, binInfixNodeIndex)
                else :
                    self.visit_tree(astBlock[1][1], binInfixNodeIndex)
            else:
                self.print_parsing_error(1051)

            # Branch for op
            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(1052)
            else:
                action[2] = 'extended'

                opNodeIndex = len(self.parsedNodes)

                if astBlock[2] == '':
                    op = ConstData('NOP', 'OP')
                else:
                    op = ConstData(str(astBlock[2]), 'OP')

                constNode = ASTNode(op, opNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(binInfixNodeIndex, opNodeIndex, None)

        elif astBlock[0] == 'Cast':
            action = copy_instance(astBlock)

            castNodeIndex = len(self.parsedNodes)

            castAction = Cast(action)
            actionNode = ASTNode(castAction, castNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, castNodeIndex, None)

            # Branch for tn
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree, castNodeIndex)
                else :
                    self.visit_tree(astBlock[1][0], castNodeIndex)
            else:
                self.print_parsing_error(1060)

            # Branch for arg
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if type(astBlock[1][1][0]) == type(list()):
                    for subTree in astBlock[1][1]:
                        self.visit_tree(subTree, castNodeIndex)
                else :
                    self.visit_tree(astBlock[1][1], castNodeIndex)
            else:
                self.print_parsing_error(1061)

        elif astBlock[0] == 'FieldAccess':
            action = copy_instance(astBlock)

            fieldAccessNodeIndex = len(self.parsedNodes)

            fieldAccessAction = FieldAccess(action)
            actionNode = ASTNode(fieldAccessAction, fieldAccessNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, fieldAccessNodeIndex, None)

            # Branch for left
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                for subTree in astBlock[1]:
                    self.visit_tree(subTree, fieldAccessNodeIndex)
            else:
                self.print_parsing_error(1070)

            if type(astBlock[2]) == type(tuple()):
                action[2] = 'extended'

                tripleNodeIndex = len(self.parsedNodes)
                triple = ConstData(astBlock[2], 'Triple')

                constNode = ASTNode(triple, tripleNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(fieldAccessNodeIndex, tripleNodeIndex, None)
            else:
                if astBlock[2] == [None, 'length', None]:
                    # This case is same as None, so we do not make a node for this
                    pass
                else:
                    self.print_parsing_error(1071)

        elif astBlock[0] == 'Literal':
            action = copy_instance(astBlock)

            literalNodeIndex = len(self.parsedNodes)

            literalAction = Literal(action)
            actionNode = ASTNode(literalAction, literalNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, literalNodeIndex, None)

            # Branch for result
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, literalNodeIndex)
                else :
                    self.visit_tree(astBlock[1], literalNodeIndex)

            else:
                # Add const value node with astBlock[1]
                action[1] = 'extended'

                constValueNodeIndex = len(self.parsedNodes)

                cv = ConstData(str(astBlock[1]), 'Value')
                constNode = ASTNode(cv, constValueNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(literalNodeIndex, constValueNodeIndex, None)

            # Branch for tt
            if type(astBlock[2]) != type(tuple()) and len(astBlock[2]) != 2:
                self.print_parsing_error(1080)
            else:
                typeNodeIndex = len(self.parsedNodes)

                typeStr = astBlock[2][0]

                action[2] = 'extended'

                typeInfo = ConstData(typeStr, 'Type')
                typeNode = ASTNode(typeInfo, typeNodeIndex)

                self.parsedNodes.append(typeNode)
                self.create_edges(literalNodeIndex, typeNodeIndex, None)


        elif astBlock[0] == 'Local':
            action = copy_instance(astBlock)

            localNodeIndex = len(self.parsedNodes)

            LocalAction = Local(action)
            actionNode = ASTNode(LocalAction, localNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, localNodeIndex, None)

            # Branch for name
            if astBlock[1] is None or type(astBlock[1]) == type(list()):
                self.print_parsing_error(1090)
                return
            else:
                registerNodeIndex = len(self.parsedNodes)

                regStr = ''

                if astBlock[1] == 'this':
                    regStr = 'thisptr'
                elif astBlock[1] == 'super':
                    regStr = 'super'
                elif astBlock[1].startswith('v'):
                    regStr = 'variable'
                elif astBlock[1].startswith('p'):
                    regStr = 'pointer'
                elif astBlock[1].startswith('_'):
                    regStr = '_'
                else:
                    print(astBlock[1])
                    self.print_parsing_error(1091)
                    return

                action[1] = 'extended'

                regInfo = ConstData(regStr, 'Register')
                regNode = ASTNode(regInfo, registerNodeIndex)

                self.parsedNodes.append(regNode)
                self.create_edges(localNodeIndex, registerNodeIndex, None)

        elif astBlock[0] == 'MethodInvocation':
            action = copy_instance(astBlock)

            methodInvocationNodeIndex = len(self.parsedNodes)

            methodInvocationAction = MethodInvocation(action)
            actionNode = ASTNode(methodInvocationAction, methodInvocationNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, methodInvocationNodeIndex, None)

            # CHECK : What is the base_flag??
            # Branch for params
            if type(astBlock[1]) == type(list()):
                # Handle the void params
                if len(astBlock[1]) == 0:
                    action[1] = 'extended'

                    constValueNodeIndex = len(self.parsedNodes)

                    cv = ConstData('void', 'Value')
                    constNode = ASTNode(cv, constValueNodeIndex)

                    self.parsedNodes.append(constNode)
                    self.create_edges(methodInvocationNodeIndex, constValueNodeIndex, None)
                else:
                    action[1] = 'extended'

                    if type(astBlock[1][0]) == type(list()):
                        for subTree in astBlock[1]:
                            self.visit_tree(subTree, methodInvocationNodeIndex)
                    else :
                        self.visit_tree(astBlock[1], methodInvocationNodeIndex)
            else:
                self.print_parsing_error(1100)

            if type(astBlock[2]) == type(tuple()) and len(astBlock[2]) != 3:
                self.print_parsing_error(1101)
                return
            else:
                action[2] = 'extended'

                tripleNodeIndex = len(self.parsedNodes)
                triple = ConstData(astBlock[2], 'Triple')

                constNode = ASTNode(triple, tripleNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(methodInvocationNodeIndex, tripleNodeIndex, None)

            action[3] = 'extended'

            apiNameNodeIndex = len(self.parsedNodes)
            apiName = ConstData(astBlock[3], 'APIName')

            constNode = ASTNode(apiName, apiNameNodeIndex)

            self.parsedNodes.append(constNode)
            self.create_edges(methodInvocationNodeIndex, apiNameNodeIndex, None)

        elif astBlock[0] == 'Parenthesis':
            action = copy_instance(astBlock)

            parenthesisNodeIndex = len(self.parsedNodes)

            parenthesisAction = Parenthesis(action)
            actionNode = ASTNode(parenthesisAction, parenthesisNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, parenthesisNodeIndex, None)

            # Branch for expr_arr
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, parenthesisNodeIndex)
                else :
                    self.visit_tree(astBlock[1], parenthesisNodeIndex)
            else:
                self.print_parsing_error(1110)

        elif astBlock[0] == 'TypeName':
            action = copy_instance(astBlock)

            typeNameNodeIndex = len(self.parsedNodes)

            typenameAction = TypeName(action)
            actionNode = ASTNode(typenameAction, typeNameNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, typeNameNodeIndex, None)

            # Branch for baset_and_dim
            if type(astBlock[1]) != type(tuple()) and len(astBlock[1]) != 2:
                self.print_parsing_error(1120)
            else:
                typeNodeIndex = len(self.parsedNodes)

                typeStr = astBlock[1][0]

                action[1] = 'extended'

                typeInfo = ConstData(typeStr, 'Type')
                typeNode = ASTNode(typeInfo, typeNodeIndex)

                self.parsedNodes.append(typeNode)
                self.create_edges(typeNameNodeIndex, typeNodeIndex, None)

        elif astBlock[0] == 'Unary':
            action = copy_instance(astBlock)

            UnaryNodeIndex = len(self.parsedNodes)

            unaryAction = Unary(action)
            actionNode = ASTNode(unaryAction, UnaryNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, UnaryNodeIndex, None)

            # Branch for left_arr expression
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree, UnaryNodeIndex)
                else :
                    self.visit_tree(astBlock[1], UnaryNodeIndex)
            else:
                self.print_parsing_error(1130)

            # Branch for op
            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(1131)
            else:
                action[2] = 'extended'

                opNodeIndex = len(self.parsedNodes)

                if astBlock[2] == '':
                    op = ConstData('NOP', 'OP')
                else:
                    op = ConstData(str(astBlock[2]), 'OP')

                constNode = ASTNode(op, opNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(UnaryNodeIndex, opNodeIndex, None)


        elif astBlock[0] == 'Dummy':
            action = copy_instance(astBlock)

            dummyNodeIndex = len(self.parsedNodes)

            # print(type(astBlock[1]))
            if type(astBlock[1]) == type(()):
                if astBlock[1][0].startswith('str(desc)'):
                    # TODO: case 1 : dummy(str(desc))
                    self.print_parsing_error(1141)

                elif astBlock[1][0].startswith('??? Unexpected constant'):
                    # TODO: case 2 : dummy('??? Unexpected constant: ' + str(op.type))
                    self.print_parsing_error(1142)

                elif astBlock[1][0].startswith('monitor enter'):
                    # TODO: case 3 : dummy("monitor enter(", visit_expr(op.var_map[op.ref]), ")")
                    self.print_parsing_error(1143)

                elif astBlock[1][0].startswith('monitor exit'):
                    # TODO: case 4 : dummy("monitor exit(", visit_expr(op.var_map[op.ref]), ")")
                    self.print_parsing_error(1144)

                elif astBlock[1][0].startswith('new'):
                    # TODO: case 5 : dummy("new ", parse_descriptor(op.type))
                    if type(astBlock[1][1]) == type(list()):
                        action[1] = 'extended'

                        dummyAction = Dummy(action)
                        actionNode = ASTNode(dummyAction, dummyNodeIndex)

                        self.parsedNodes.append(actionNode)
                        self.create_edges(pIndex, dummyNodeIndex, None)

                        if type(astBlock[1][1][0]) == type(list()):
                            for subTree in astBlock[1][1]:
                                self.visit_tree(subTree, dummyNodeIndex)
                        else :
                            self.visit_tree(astBlock[1][1], dummyNodeIndex)
                    else:
                        self.print_parsing_error(1145)
                        print(astBlock[1][1])

                elif astBlock[1][0].startswith('??? Unexpected op'):
                    # TODO: case 6 :dummy('??? Unexpected op: ' + type(op).__name__)
                    self.print_parsing_error(1146)
            else:
                self.print_parsing_error(1140)

        elif astBlock[0] == 'ClassInstanceCreation':
            action = copy_instance(astBlock)

            clsInstanceCreationNodeIndex = len(self.parsedNodes)

            classInstanceCreationAction = ClassInstanceCreation(action)
            actionNode = ASTNode(classInstanceCreationAction, clsInstanceCreationNodeIndex)

            self.parsedNodes.append(actionNode)
            self.create_edges(pIndex, clsInstanceCreationNodeIndex, None)

            # Branch for triple
            if type(astBlock[1]) != type(tuple()) and len(astBlock[1]) != 3:
                self.print_parsing_error(1150)
            else:
                action[1] = 'extended'

                tripleNodeIndex = len(self.parsedNodes)
                triple = ConstData(astBlock[1], 'Triple')

                constNode = ASTNode(triple, tripleNodeIndex)

                self.parsedNodes.append(constNode)
                self.create_edges(clsInstanceCreationNodeIndex, tripleNodeIndex, None)

            # Branch for params
            if type(astBlock[2]) == type(list()):
                action[2] = 'extended'

                # Handle the void params
                if len(astBlock[2]) == 0:
                    constValueNodeIndex = len(self.parsedNodes)

                    cv = ConstData('void', 'Value')
                    constNode = ASTNode(cv, constValueNodeIndex)

                    self.parsedNodes.append(constNode)
                    self.create_edges(clsInstanceCreationNodeIndex, constValueNodeIndex, None)

                else:
                    if type(astBlock[2][0]) == type(list()):
                        for subTree in astBlock[2]:
                            self.visit_tree(subTree, clsInstanceCreationNodeIndex)
                    else :
                        self.visit_tree(astBlock[2], clsInstanceCreationNodeIndex)
            else:
                self.print_parsing_error(1151)
                print(astBlock)

            # Branch for parse_descriptor
            if type(astBlock[3]) == type(list()):
                action[3] = 'extended'

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree, clsInstanceCreationNodeIndex)
                else :
                    self.visit_tree(astBlock[3], clsInstanceCreationNodeIndex)
            else:
                self.print_parsing_error(1152)

        else:
            self.print_parsing_error(-2)
            print(astBlock)

    def visit_pairs(self, tupleList, pIndex):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_pairs is invoked', Color.GREEN.value))
            pprint(tupleList)

        for pairTuple in tupleList:
            for t in pairTuple:
                if type(t[0]) == type(list()):
                    for subTree in t:
                        self.visit_tree(subTree, pIndex)
                else :
                    self.visit_tree(t, pIndex)

    def create_edges(self, pIndex, cIndex, edge_type):
        if self.isDebug:
            print(set_string_colored('DP Check : ' + str(pIndex, cIndex), Color.GREEN.value))
            print(set_string_colored('DP Check : ' + str(self.parsedNodes[cIndex].nodeInfo), Color.GREEN.value))

        if self.entryFlag:
            if pIndex == -1 and cIndex == 0:
                ast_edge = ASTEdge(pIndex, cIndex, edge_type)
                self.parsedEdges.append(ast_edge)

                self.entryFlag = False
            else:
                self.print_parsing_error(-3)
        else:
            if pIndex == -1 or cIndex == 0:
                self.print_parsing_error(-3)
            else:
                ast_edge = ASTEdge(pIndex, cIndex, edge_type)
                self.parsedEdges.append(ast_edge)
            
    def show_whole_ast(self):
        if self.ast:
            pprint(self.ast)
        else:
            self.print_parsing_error(0)


# Class for parsed node of AST
class ASTNode():
    def __init__(self, data, index):
        self.nodeInfo = data
        self.index = index

# Class for parsed node of AST on value (not a statement, and not an action)
class ConstData():
    def __init__(self, value, const_type):
        self.type = const_type
        self.value = value

    def __repr__(self):
        return (
            'type: ' + str(self.type)
            + ' / value:' + str(self.value)
            )

# Class for managing the edge information among the parsedNodes of AST
class ASTEdge():
    def __init__(self, pIndex, cIndex, type):
        self.pIndex = pIndex
        self.cIndex = cIndex
        self.type = ''

    def __repr__(self):
        return(
            'pIndex: ' + str(self.pIndex)
            + ' / cIndex: ' + str(self.cIndex)
            + ' / type: ' + str(self.type)
            )