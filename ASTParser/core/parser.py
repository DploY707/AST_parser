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


class ASTParser():
    def __init__(self, flag = False):
        self.isDebug = flag
        self.ast = None
        self.errMsg = ''
        self.parsedNodes = list()
        self.parsedEdges = list()

    def print_parsing_error(self, errorType):
        # Errors in large scale
        if errorType == -1:
            self.errMsg = 'ERR_NO(-1): AST has wrong statement data'
        elif errorType == -2:
            self.errMsg = 'ERR_NO(-2): AST has wrong action data'
        elif errorType == -3:
            self.errMsg = 'ERR_NO(-3): parent node index is an invalid value'

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
            self.errMsg = 'ERR_NO(60): Wrong operand in JumpStatement'
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
            self.errMsg = 'ERR_NO(1031): Wrong operand in ArrayInitializer(tn), tn is not None'
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
        elif errorType == 1080:
            self.errMsg = 'ERR_NO(1080): Wrong operand in Literal(tt), tt is list() data'
        elif errorType == 1090:
            self.errMsg = 'ERR_NO(1090): Wrong operand in Local(name), name is None or list() data'
        elif errorType == 1100:
            self.errMsg = 'ERR_NO(1100): Wrong operand in MethodInvocation(params)'
        elif errorType == 1110:
            self.errMsg = 'ERR_NO(1110): Wrong operand in Parenthesis(expr_arr)'
        elif errorType == 1120:
            self.errMsg = 'ERR_NO(1120): Wrong operand in TypeName(baset_and_dim)'
        elif errorType == 1130:
            self.errMsg = 'ERR_NO(1130): Wrong operand in Unary(left_arr)'
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
            self.errMsg = 'ERR_NO(1150): Wrong operand in ClassInstanceCreation(params)'
        elif errorType == 1151:
            self.errMsg = 'ERR_NO(1151): Wrong operand in ClassInstanceCreation(parse_descriptor)'

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
        
    def visit_tree(self, ast, parent = -1):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_tree is invoked', Color.GREEN.value))
            print(set_string_colored("DP Check : " + str(ast), Color.GREEN.value))

            pprint(ast)

        if ast is None:
            return

        if ast[0] in stmtList:
            self.visit_statments(ast, parent)
        elif ast[0] in actionList:
            self.visit_actions(ast, parent)
        else:
            cd = ConstData(ast, len(self.parsedNodes))
            constNode = ASTNode(cd, len(self.parsedNodes))
            self.parsedNodes.append(constNode)

    def visit_statments(self, astBlock, parent):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_statments is invoked', Color.GREEN.value))
            pprint(astBlock)

        if astBlock[0] == 'BlockStatement':
            stmt = copy_instance(astBlock)

            blockStmtNodeIndex = len(self.parsedNodes)

            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                bs = BlockStatement(stmt)
                stmtNode = ASTNode(bs, blockStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                for subTree in astBlock[2]:
                    self.visit_tree(subTree)
            else:
                self.print_parsing_error(10)

        elif astBlock[0] == 'ExpressionStatement':
            stmt = copy_instance(astBlock)

            exprStmtNodeIndex = len(self.parsedNodes)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                es = ExpressionStatement(stmt)
                stmtNode = ASTNode(es, exprStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(20)

        elif astBlock[0] == 'LocalDeclarationStatement':
            stmt = copy_instance(astBlock)

            localDeclStmtNodeIndex = len(self.parsedNodes)

            # Branch for expr
            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                lds = LocalDeclarationStatement(stmt)
                stmtNode = ASTNode(lds, localDeclStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                # CHECK: In usual, this case, astBlock[1] is None
                lds = LocalDeclarationStatement(stmt)
                stmtNode = ASTNode(lds, localDeclStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

            # Branch for decl
            if type(astBlock[2]) == type(list()):
                stmt[2] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[localDeclStmtNodeIndex].nodeInfo.update_localDeclarationStatement(stmt)
                else:
                    lds = LocalDeclarationStatement(stmt)
                    stmtNode = ASTNode(lds, localDeclStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[2])
            else:
                self.print_parsing_error(30)

        elif astBlock[0] == 'ReturnStatement':
            stmt = copy_instance(astBlock)

            returnStmtNodeIndex = len(self.parsedNodes)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                rs = ReturnStatement(stmt)
                stmtNode = ASTNode(rs, returnStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                # CHECK: In usual, this case, astBlock[1] is None
                # self.print_parsing_error(40)
                rs = ReturnStatement(stmt)
                stmtNode = ASTNode(rs, returnStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

        elif astBlock[0] == 'ThrowStatement':
            stmt = copy_instance(astBlock)

            throwStmtNodeIndex = len(self.parsedNodes)

            if type(astBlock[1]) == type(list()):
                stmt[1] = 'extended'

                ts = ThrowStatement(stmt)
                stmtNode = ASTNode(ts, throwStmtNodeIndex)

                self.parsedNodes.append(stmtNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(50)

        elif astBlock[0] == 'JumpStatement':
            stmt = copy_instance(astBlock)

            jmpStmtNodeIndex = len(self.parsedNodes)

            js = JumpStatement(stmt)
            stmtNode = ASTNode(js, jmpStmtNodeIndex)

            self.parsedNodes.append(stmtNode)

            #TODO : Add a routine that prevent crash or wrong behaviors
            # Blah Blah Blah Blah Blah Blah
            # self.print_parsing_error(60)

        elif astBlock[0] == 'DoStatement':
            stmt = copy_instance(astBlock)

            doStmtNodeIndex = len(self.parsedNodes)

            # Branch for cond_expr
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
                self.print_parsing_error(70)

            # Branch for body_expr
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[doStmtNodeIndex].nodeInfo.update_doStatement(stmt)
                else:
                    ds = DoStatement(stmt)
                    stmtNode = ASTNode(ds, doStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[3])
            else:
                self.print_parsing_error(71)

        elif astBlock[0] == 'WhileStatement':
            stmt = copy_instance(astBlock)

            whileStmtNodeIndex = len(self.parsedNodes)

            # Branch for cond_expr
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
                self.print_parsing_error(80)

            # Branch for body_expr
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[whileStmtNodeIndex].nodeInfo.update_whileStatement(stmt)
                else:
                    ws = WhileStatement(stmt)
                    stmtNode = ASTNode(ws, whileStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[3])
            else:
                self.print_parsing_error(81)

        # CHECK : what is the meaning of pair formed data
        elif astBlock[0] == 'TryStatement':
            stmt = copy_instance(astBlock)

            tryStmtNodeIndex = len(self.parsedNodes)

            # Branch for tryb_expr
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
                self.print_parsing_error(90)

            # Branch for pairs_expr
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                # Node Creation
                if 'extended' in stmt:
                    self.parsedNodes[tryStmtNodeIndex].nodeInfo.update_tryStatement(stmt)
                else:
                    ts = TryStatement(stmt)
                    stmtNode = ASTNode(ts, tryStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                # Visit the pair formed expr for parsing the AST
                if astBlock[3] is None:
                    self.print_parsing_error(92)
                else:
                    self.visit_pairs(astBlock[3])
            else:
                self.print_parsing_error(91)

        elif astBlock[0] == 'IfStatement':
            stmt = copy_instance(astBlock)

            ifStmtNodeIndex = len(self.parsedNodes)

            # Branch for cond_expr
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
                self.print_parsing_error(100)

            # Branch for body_expr
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[ifStmtNodeIndex].nodeInfo.update_ifStatement(stmt)
                else:
                    ifs = IfStatement(stmt)
                    stmtNode = ASTNode(ifs, ifStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if type(astBlock[3][0]) == type(list()):
                    for subTree in astBlock[3]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[3])
            else:
                self.print_parsing_error(101)

        elif astBlock[0] == 'SwitchStatement':
            stmt = copy_instance(astBlock)

            switchStmtNodeIndex = len(self.parsedNodes)

            # Branch for cond_expr
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
                self.print_parsing_error(110)

            # Branch for ksv_pairs
            # CHECK : How to interpret the meaning of pairs
            if type(astBlock[3]) == type(list()):
                stmt[3] = 'extended'

                if 'extended' in stmt:
                    self.parsedNodes[switchStmtNodeIndex].nodeInfo.update_switchStatement(stmt)
                else:
                    ss = SwitchStatement(stmt)
                    stmtNode = ASTNode(ss, switchStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if astBlock[3] is None:
                    self.print_parsing_error(112)
                else:
                    self.visit_pairs(astBlock[3])
            else:
                self.print_parsing_error(111)

        else:
            self.print_parsing_error(-1)

    def visit_actions(self, astBlock, parent):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_actions is invoked', Color.GREEN.value))
            pprint(astBlock)

        if astBlock[0] == 'ArrayAccess':
            action = copy_instance(astBlock)

            arrAccessNodeIndex = len(self.parsedNodes)

            # Branch for arr
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                arrayAccessAction = ArrayAccess(action)
                actionNode = ASTNode(arrayAccessAction, arrAccessNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0][0]) == type(list()):
                    for subTree in astBlock[1][0]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1][0])
            else:
                self.print_parsing_error(1010)

            # Branch for ind
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[arrAccessNodeIndex].nodeInfo.update_arrayAccess(action)
                else:
                    arrayAccessAction = ArrayAccess(action)
                    actionNode = ASTNode(arrayAccessAction, arrAccessNodeIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[1][1][0]) == type(list()):
                        for subTree in astBlock[1][1]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[1][1])
            else:
                self.print_parsing_error(1011)

        elif astBlock[0] == 'ArrayCreation':
            action = copy_instance(astBlock)

            arrCreationNodeIndex = len(self.parsedNodes)

            # Branch for tn_and_params
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                arrayCreationAction = ArrayCreation(action)
                actionNode = ASTNode(arrayCreationAction, arrCreationNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(1020)

            # Branch for dim
            if type(astBlock[2]) == type(list()):
                action[2] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[arrCreationNodeIndex].nodeInfo.update_arrayCreation(action)
                else:
                    arrayCreationAction = ArrayCreation(action)
                    actionNode = ASTNode(arrayCreationAction, arrCreationNodeIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[2][0]) == type(list()):
                        for subTree in astBlock[2]:
                            self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[2])
            else:
                # In this case, dim is just a const value like 1
                pass

        elif astBlock[0] == 'ArrayInitializer':
            action = copy_instance(astBlock)

            arrInitializerNodeIndex = len(self.parsedNodes)

            # Branch for params
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                arrayInitializerAction = ArrayInitializer(action)
                actionNode = ASTNode(arrayInitializerAction, arrInitializerNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(1030)

            # Branch for tn
            if astBlock[2] is not None:
                self.print_parsing_error(1031)

            # TODO : Add a routine for handling action[2], 'tn' field

        elif astBlock[0] == 'Assignment':
            action = copy_instance(astBlock)

            assignNodeIndex = len(self.parsedNodes)

            # Branch for lhs
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                assignAction = Assignment(action)
                actionNode = ASTNode(assignAction, assignNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree)
                else:
                    self.visit_tree(astBlock[1][0])
            else:
                self.print_parsing_error(1040)

            # Branch for rhs
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[assignNodeIndex].nodeInfo.update_assignment(action)
                else:
                    assignAction = Assignment(action)
                    actionNode = ASTNode(assignAction, assignNodeIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[1][1][0]) == type(list()):
                        for subTree in astBlock[1][1]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[1][1])
            else:
                self.print_parsing_error(1041)

            # Branch for op
            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(1042)

        elif astBlock[0] == 'BinaryInfix':
            action = copy_instance(astBlock)

            binInfixNodeIndex = len(self.parsedNodes)

            # Branch for left
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                binaryInfixAction = BinaryInfix(action)
                actionNode = ASTNode(binaryInfixAction, binInfixNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1][0])
            else:
                self.print_parsing_error(1050)

            # Branch for right
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[binInfixNodeIndex].nodeInfo.update_binaryInfix(action)
                else:
                    binaryInfixAction = BinaryInfix(action)
                    actionNode = ASTNode(binaryInfixAction, binInfixNodeIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[1][1][0]) == type(list()):
                        for subTree in astBlock[1][1]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[1][1])
            else:
                self.print_parsing_error(1051)

            # Branch for op
            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(1052)

        elif astBlock[0] == 'Cast':
            action = copy_instance(astBlock)

            castNodeIndex = len(self.parsedNodes)

            # Branch for tn
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                castAction = Cast(action)
                actionNode = ASTNode(castAction, castNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1][0])
            else:
                self.print_parsing_error(1060)

            # Branch for arg
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[castNodeIndex].nodeInfo.update_cast(action)
                else:
                    castAction = Cast(action)
                    actionNode = ASTNode(castAction, castNodeIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[1][1][0]) == type(list()):
                        for subTree in astBlock[1][1]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[1][1])
            else:
                self.print_parsing_error(1061)

        elif astBlock[0] == 'FieldAccess':
            action = copy_instance(astBlock)

            fieldAccessNodeIndex = len(self.parsedNodes)

            # Branch for left
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                fieldAccessAction = FieldAccess(action)
                actionNode = ASTNode(fieldAccessAction, fieldAccessNodeIndex)

                self.parsedNodes.append(actionNode)

                for subTree in astBlock[1]:
                    self.visit_tree(subTree)

            else:
                self.print_parsing_error(1070)

        elif astBlock[0] == 'Literal':
            action = copy_instance(astBlock)

            literalNodeIndex = len(self.parsedNodes)

            # Branch for result
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                literalAction = Literal(action)
                actionNode = ASTNode(literalAction, literalNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])

            else:
                literalAction = Literal(action)
                actionNode = ASTNode(literalAction, literalNodeIndex)

                self.parsedNodes.append(actionNode)

            # Branch for tt
            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(1080)

        elif astBlock[0] == 'Local':
            action = copy_instance(astBlock)

            localNodeIndex = len(self.parsedNodes)

            # Branch for name
            if astBlock[1] is None or type(astBlock[1]) == type(list()):
                self.print_parsing_error(1090)
                return

            LocalAction = Local(action)
            actionNode = ASTNode(LocalAction, localNodeIndex)

            self.parsedNodes.append(actionNode)

        elif astBlock[0] == 'MethodInvocation':
            action = copy_instance(astBlock)

            methodInvocationNodeIndex = len(self.parsedNodes)

            # CHECK : What is the base_flag??
            # Branch for params
            if type(astBlock[1]) == type(list()):
                # Handle the void params
                if len(astBlock[1]) == 0:
                    astBlock[1] = 'void'
                    action[1] = 'void'
                else:
                    action[1] = 'extended'

                methodInvocationAction = MethodInvocation(action)
                actionNode = ASTNode(methodInvocationAction, methodInvocationNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(1100)

        elif astBlock[0] == 'Parenthesis':
            action = copy_instance(astBlock)

            parenthesisNodeIndex = len(self.parsedNodes)

            # Branch for expr_arr
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                parenthesisAction = Parenthesis(action)
                actionNode = ASTNode(parenthesisAction, parenthesisNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(1110)

        elif astBlock[0] == 'TypeName':
            action = copy_instance(astBlock)

            typeNameNodeIndex = len(self.parsedNodes)

            # Branch for baset_and_dim
            if type(astBlock[1]) == type(list()):
                self.print_parsing_error(1120)

            typenameAction = TypeName(action)
            actionNode = ASTNode(typenameAction, typeNameNodeIndex)

            self.parsedNodes.append(actionNode)

        elif astBlock[0] == 'Unary':
            action = copy_instance(astBlock)

            UnaryNodeIndex = len(self.parsedNodes)

            # Branch for left_arr expression
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                unaryAction = Unary(action)
                actionNode = ASTNode(unaryAction, UnaryNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(1130)

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

                        if type(astBlock[1][1][0]) == type(list()):
                            for subTree in astBlock[1][1]:
                                self.visit_tree(subTree)
                        else :
                            self.visit_tree(astBlock[1][1])
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

            # Branch for params
            if type(astBlock[2]) == type(list()):

                # Handle the void params
                if len(astBlock[2]) == 0:
                    astBlock[2] = 'void'
                    action[2] = 'void'
                else:
                    action[2] = 'extended'

                classInstanceCreationAction = ClassInstanceCreation(action)
                actionNode = ASTNode(classInstanceCreationAction, clsInstanceCreationNodeIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[2])
            else:
                self.print_parsing_error(1150)
                print(astBlock)

            # Branch for parse_descriptor
            if type(astBlock[3]) == type(list()):
                action[3] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[clsInstanceCreationNodeIndex].nodeInfo.update_classInstanceCreation(action)
                else:
                    classInstanceCreationAction = ClassInstanceCreation(action)
                    actionNode = ASTNode(classInstanceCreationAction, clsInstanceCreationNodeIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[3][0]) == type(list()):
                        for subTree in astBlock[3]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[3])
            else:
                self.print_parsing_error(1151)

        else:
            self.print_parsing_error(-2)
            print(astBlock)

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

    def create_edges(self, pIndex, cIndex, type):
        if cIndex != 0:
            if pIndex != -1:
                ast_edge = ASTEdge(pIndex, cIndex, type)

                self.parsedEdges.append(ast_edge)
            else:
                self.print_parsing_error(-3)

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

# Class for managing the edge information among the parsedNodes of AST
class ASTEdge():
    def __init__(self, pIndex, cIndex, type):
        self.pIndex = pIndex
        self.cIndex = cIndex
        self.type = ''

# Class for const Node
class ConstData():
    def __init__(self, data, index):
        self.data = data
        self.index = index