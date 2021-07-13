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
        # Errors on visit fuctions
        if errorType == -1:
            self.errMsg = 'AST has wrong statement data'
        elif errorType == -2:
            self.errMsg = 'AST has wrong action data'

        # Error that AST is not loaded
        elif errorType == 0:
            self.errMsg = 'AST is not loaded, so you have to load it first'
        
        # Error on parsing statements
        elif errorType == 1:
            self.errMsg = 'Wrong operand in BlockStatement'
        elif errorType == 2:
            self.errMsg = 'Wrong operand in ExpressionStatement'
        elif errorType == 3:
            self.errMsg = 'Wrong operand in LocalDeclarationStatement(decl)'
        elif errorType == 4:
            self.errMsg = 'Wrong operand in ReturnStatement'
        elif errorType == 5:
            self.errMsg = 'Wrong operand in ThrowStatement'
        elif errorType == 6:
            self.errMsg = 'Wrong operand in JumpStatement'
        elif errorType == 70:
            self.errMsg = 'Wrong operand in DoStatement(cond_expr)'
        elif errorType == 71:
            self.errMsg = 'Wrong operand in DoStatement(body_expr)'
        elif errorType == 80:
            self.errMsg = 'Wrong operand in WhileStatement(cond_expr)'
        elif errorType == 81:
            self.errMsg = 'Wrong operand in WhileStatement(body_expr)'
        elif errorType == 90:
            self.errMsg = 'Wrong operand in TryStatement(tryb_expr)'
        elif errorType == 91:
            self.errMsg = 'Wrong operand in TryStatement(pairs_expr)'
        elif errorType == 92:
            self.errMsg = 'Wrong operand in TryStatement(pairs_expr), pairs_expr is None'
        elif errorType == 100:
            self.errMsg = 'Wrong operand in IfStatement(cond_expr)'
        elif errorType == 101:
            self.errMsg = 'Wrong operand in IfStatement(body_expr)'
        elif errorType == 110:
            self.errMsg = 'Wrong operand in SwitchStatement(cond_expr)'
        elif errorType == 111:
            self.errMsg = 'Wrong operand in SwitchStatement(ksv_pairs)'
        elif errorType == 112:
            self.errMsg = 'Wrong operand in SwitchStatement(ksv_pairs), ksv_pairs is None'


        elif errorType == 2:
            self.errMsg = 'Wrong formmated AST is entered'
        
        elif errorType == 3:
            self.errMsg = 'The TryStatement has no pairs'
        elif errorType == 4:
            self.errMsg = 'The switchStatement has no ksv_pairs'
        elif errorType == 5:
            self.errMsg = 'Wrong operand in ArrayAccess action'
        elif errorType == 6:
            self.errMsg = 'Wrong operand in ArrayCreation action'
        elif errorType == 7:
            self.errMsg = 'Wrong operand in ArrayInitializer action'
        elif errorType == 70:
            self.errMsg = 'Wrong operand in ArrayInitializer action, tn is not None'
        elif errorType == 8:
            self.errMsg = 'Wrong operand in Assignment action'
        elif errorType == 80:
            self.errMsg = 'Wrong operand in Assignment action, op is a list() data'
        elif errorType == 9:
            self.errMsg = 'Wrong operand in BinaryInfix action'
        elif errorType == 90:
            self.errMsg = 'Wrong operand in BinaryInfix action, op is a list() data'
        elif errorType == 11:
            self.errMsg = 'Wrong operand in FieldAccess action'
        elif errorType == 12:
            self.errMsg = 'Wrong operand in Literal action, tt field is a list() data'
        elif errorType == 13:
            self.errMsg = 'Wrong operand in Local action'
        elif errorType == 14:
            self.errMsg = 'Wrong operand in MethodInvocation action'
        elif errorType == 15:
            self.errMsg = 'Wrong operand in Parenthesis action'
        elif errorType == 16:
            self.errMsg = 'Wrong operand in TypeName action'
        elif errorType == 17:
            self.errMsg = 'Wrong operand in Unary action'
        elif errorType == 18:
            self.errMsg = 'Wrong operand in Dummy action'
        elif errorType == 180:
            self.errMsg = 'Wrong operand in Dummy action, str(desc)'
        elif errorType == 181:
            self.errMsg = 'Wrong operand in Dummy action, ??? Unexpected constant'
        elif errorType == 182:
            self.errMsg = 'Wrong operand in Dummy action, monitor enter'
        elif errorType == 183:
            self.errMsg = 'Wrong operand in Dummy action, monitor exit'
        elif errorType == 184:
            self.errMsg = 'Wrong operand in Dummy action, new'
        elif errorType == 185:
            self.errMsg = 'Wrong operand in Dummy action, ??? Unexpected op'
        elif errorType == 19:
            self.errMsg = 'Wrong operand in Unary ClassInstanceCreation'
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
            cd = ConstData(ast, len(self.parsedNodes))
            constNode = ASTNode(cd, len(self.parsedNodes))
            self.parsedNodes.append(constNode)

    def visit_statments(self, astBlock):
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
                self.print_parsing_error(1)

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
                self.print_parsing_error(2)

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
                self.print_parsing_error(3)

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
                # self.print_parsing_error(4)
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
                self.print_parsing_error(5)

        elif astBlock[0] == 'JumpStatement':
            stmt = copy_instance(astBlock)

            jmpStmtNodeIndex = len(self.parsedNodes)

            js = JumpStatement(stmt)
            stmtNode = ASTNode(js, jmpStmtNodeIndex)

            self.parsedNodes.append(stmtNode)

            #TODO : Add a routine that prevent crash or wrong behaviors
            # Blah Blah Blah Blah Blah Blah
            # self.print_parsing_error(6)

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

    def visit_actions(self, astBlock):
        if self.isDebug:
            print(set_string_colored('DP Check : function: visit_actions is invoked', Color.GREEN.value))
            pprint(astBlock)

        if astBlock[0] == 'ArrayAccess':
            action = copy_instance(astBlock)

            arrayAccessActionIndex = len(self.parsedNodes)

            # Branch for arr expression
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                arrayAccessAction = ArrayAccess(action)
                actionNode = ASTNode(arrayAccessAction, arrayAccessActionIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0][0]) == type(list()):
                    for subTree in astBlock[1][0]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1][0])
            else:
                self.print_parsing_error(5)

            # Branch for ind expression
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[arrayAccessActionIndex].nodeInfo.update_arrayAccess(action)
                else:
                    arrayAccessAction = ArrayAccess(action)
                    actionNode = ASTNode(arrayAccessAction, arrayAccessActionIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[1][1][0]) == type(list()):
                        for subTree in astBlock[1][1]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[1][1])
            else:
                self.print_parsing_error(5)

        elif astBlock[0] == 'ArrayCreation':
            action = copy_instance(astBlock)

            arrayCreationActionIndex = len(self.parsedNodes)

            # Branch for tn_and_params expression
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                arrayCreationAction = ArrayCreation(action)
                actionNode = ASTNode(arrayCreationAction, arrayCreationActionIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(6)

            # Branch for dim expression
            if type(astBlock[2]) == type(list()):
                action[2] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[arrayCreationActionIndex].nodeInfo.update_arrayCreation(action)
                else:
                    arrayCreationAction = ArrayCreation(action)
                    actionNode = ASTNode(arrayCreationAction, arrayCreationActionIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[2][0]) == type(list()):
                        for subTree in astBlock[2]:
                            self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[2])
            # In this case, dim expression is just a const value like 1
            else:
                pass
                # self.print_parsing_error(6)

        elif astBlock[0] == 'ArrayInitializer':
            action = copy_instance(astBlock)

            arrayInitializerIndex = len(self.parsedNodes)

            # Branch for params expression
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                arrayInitializerAction = ArrayInitializer(action)
                actionNode = ASTNode(arrayInitializerAction, arrayInitializerIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(7)

            if astBlock[2] is not None:
                self.print_parsing_error(70)
            # TODO : Add a routine for handling action[2], 'tn' field

        elif astBlock[0] == 'Assignment':
            action = copy_instance(astBlock)

            assignmentActionIndex = len(self.parsedNodes)

            # Branch for lhs expression
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                assignAction = Assignment(action)
                actionNode = ASTNode(assignAction, assignmentActionIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree)
                else:
                    self.visit_tree(astBlock[1][0])
            else:
                self.print_parsing_error(8)

            # Branch for rhs expression
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[assignmentActionIndex].nodeInfo.update_assignment(action)
                else:
                    assignAction = Assignment(action)
                    actionNode = ASTNode(assignAction, assignmentActionIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[1][1][0]) == type(list()):
                        for subTree in astBlock[1][1]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[1][1])
            else:
                self.print_parsing_error(8)

            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(80)

        elif astBlock[0] == 'BinaryInfix':
            action = copy_instance(astBlock)

            binaryInfixActionIndex = len(self.parsedNodes)

            # Branch for left expression
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                binaryInfixAction = BinaryInfix(action)
                actionNode = ASTNode(binaryInfixAction, binaryInfixActionIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1][0])
            else:
                self.print_parsing_error(9)

            # Branch for right expression
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[binaryInfixActionIndex].nodeInfo.update_binaryInfix(action)
                else:
                    binaryInfixAction = BinaryInfix(action)
                    actionNode = ASTNode(binaryInfixAction, binaryInfixActionIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[1][1][0]) == type(list()):
                        for subTree in astBlock[1][1]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[1][1])
            else:
                self.print_parsing_error(9)

            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(90)

        elif astBlock[0] == 'Cast':
            action = copy_instance(astBlock)

            castActionIndex = len(self.parsedNodes)

            # Branch for tn expression
            if type(astBlock[1][0]) == type(list()):
                action[1][0] = 'extended'

                castAction = Cast(action)
                actionNode = ASTNode(castAction, castActionIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0][0]) == type(list()):
                        for subTree in astBlock[1][0]:
                           self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1][0])
            else:
                self.print_parsing_error(10)

            # Branch for arg expression
            if type(astBlock[1][1]) == type(list()):
                action[1][1] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[castActionIndex].nodeInfo.update_cast(action)
                else:
                    castAction = Cast(action)
                    actionNode = ASTNode(castAction, castActionIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[1][1][0]) == type(list()):
                        for subTree in astBlock[1][1]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[1][1])
            else:
                self.print_parsing_error(10)

        elif astBlock[0] == 'FieldAccess':
            action = copy_instance(astBlock)

            fieldAccessActionIndex = len(self.parsedNodes)

            # Branch for left expression
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                fieldAccessAction = FieldAccess(action)
                actionNode = ASTNode(fieldAccessAction, fieldAccessActionIndex)

                self.parsedNodes.append(actionNode)

                for subTree in astBlock[1]:
                    self.visit_tree(subTree)

            else:
                self.print_parsing_error(11)

        elif astBlock[0] == 'Literal':
            action = copy_instance(astBlock)

            literalActionIndex = len(self.parsedNodes)

            # Branch for result expression
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                literalAction = Literal(action)
                actionNode = ASTNode(literalAction, literalActionIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])

            else:
                literalAction = Literal(action)
                actionNode = ASTNode(literalAction, literalActionIndex)

                self.parsedNodes.append(actionNode)

            if type(astBlock[2]) == type(list()):
                self.print_parsing_error(12)

        elif astBlock[0] == 'Local':
            action = copy_instance(astBlock)

            localActionIndex = len(self.parsedNodes)

            if astBlock[1] is None or type(astBlock[1]) == type(list()):
                self.print_parsing_error(13)
                return

            LocalAction = Local(action)
            actionNode = ASTNode(LocalAction, localActionIndex)

            self.parsedNodes.append(actionNode)


        elif astBlock[0] == 'MethodInvocation':
            action = copy_instance(astBlock)

            methodInvocationIndex = len(self.parsedNodes)

            # TODO : Check the base flag should be considered or not
            # Branch for params expression
            if type(astBlock[1]) == type(list()):
                # Handle the void params
                if len(astBlock[1]) == 0:
                    astBlock[1] = 'void'
                    action[1] = 'void'
                else:
                    action[1] = 'extended'

                methodInvocationAction = MethodInvocation(action)
                actionNode = ASTNode(methodInvocationAction, methodInvocationIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(14)
                print(astBlock)

        elif astBlock[0] == 'Parenthesis':
            action = copy_instance(astBlock)

            parenthesisIndex = len(self.parsedNodes)

            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                parenthesisAction = Parenthesis(action)
                actionNode = ASTNode(parenthesisAction, parenthesisIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(15)

        elif astBlock[0] == 'TypeName':
            action = copy_instance(astBlock)

            typeNameIndex = len(self.parsedNodes)

            if type(astBlock[1]) == type(list()):
                self.print_parsing_error(16)

            typenameAction = TypeName(action)
            actionNode = ASTNode(typenameAction, typeNameIndex)

            self.parsedNodes.append(actionNode)

        elif astBlock[0] == 'Unary':
            action = copy_instance(astBlock)

            UnaryIndex = len(self.parsedNodes)

            # TODO : Check the base flag should be considered or not
            # Branch for left_arr expression
            if type(astBlock[1]) == type(list()):
                action[1] = 'extended'

                unaryAction = Unary(action)
                actionNode = ASTNode(unaryAction, UnaryIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[1][0]) == type(list()):
                    for subTree in astBlock[1]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[1])
            else:
                self.print_parsing_error(17)
                # print(astBlock)

        elif astBlock[0] == 'Dummy':
            action = copy_instance(astBlock)

            dummyIndex = len(self.parsedNodes)

            # print(type(astBlock[1]))
            if type(astBlock[1]) == type(()):
                if astBlock[1][0].startswith('str(desc)'):
                    # TODO: case 1 : dummy(str(desc))
                    self.print_parsing_error(180)

                elif astBlock[1][0].startswith('??? Unexpected constant'):
                    # TODO: case 2 : dummy('??? Unexpected constant: ' + str(op.type))
                    self.print_parsing_error(181)

                elif astBlock[1][0].startswith('monitor enter'):
                    # TODO: case 3 : dummy("monitor enter(", visit_expr(op.var_map[op.ref]), ")")
                    self.print_parsing_error(182)

                elif astBlock[1][0].startswith('monitor exit'):
                    # TODO: case 4 : dummy("monitor exit(", visit_expr(op.var_map[op.ref]), ")")
                    self.print_parsing_error(183)

                elif astBlock[1][0].startswith('new'):
                    # TODO: case 5 : dummy("new ", parse_descriptor(op.type))
                    if type(astBlock[1][1]) == type(list()):
                        action[1] = 'extended'

                        dummyAction = Dummy(action)
                        actionNode = ASTNode(dummyAction, dummyIndex)

                        self.parsedNodes.append(actionNode)

                        if type(astBlock[1][1][0]) == type(list()):
                            for subTree in astBlock[1][1]:
                                self.visit_tree(subTree)
                        else :
                            self.visit_tree(astBlock[1][1])
                    else:
                        self.print_parsing_error(184)
                        print(astBlock[1][1])

                elif astBlock[1][0].startswith('??? Unexpected op'):
                    # TODO: case 6 :dummy('??? Unexpected op: ' + type(op).__name__)
                    self.print_parsing_error(185)
            else:
                self.print_parsing_error(18)

        elif astBlock[0] == 'ClassInstanceCreation':
            action = copy_instance(astBlock)

            classInstanceCreationIndex = len(self.parsedNodes)

            # Branch for params expression
            if type(astBlock[2]) == type(list()):

                # Handle the void params
                if len(astBlock[2]) == 0:
                    astBlock[2] = 'void'
                    action[2] = 'void'
                else:
                    action[2] = 'extended'

                classInstanceCreationAction = ClassInstanceCreation(action)
                actionNode = ASTNode(classInstanceCreationAction, classInstanceCreationIndex)

                self.parsedNodes.append(actionNode)

                if type(astBlock[2][0]) == type(list()):
                    for subTree in astBlock[2]:
                        self.visit_tree(subTree)
                else :
                    self.visit_tree(astBlock[2])
            else:
                self.print_parsing_error(19)
                print(astBlock)

            # Branch for parse_descriptor expression
            if type(astBlock[3]) == type(list()):
                action[3] = 'extended'

                if 'extended' in action:
                    self.parsedNodes[classInstanceCreationIndex].nodeInfo.update_classInstanceCreation(action)
                else:
                    classInstanceCreationAction = ClassInstanceCreation(action)
                    actionNode = ASTNode(classInstanceCreationAction, classInstanceCreationIndex)

                    self.parsedNodes.append(actionNode)

                    if type(astBlock[3][0]) == type(list()):
                        for subTree in astBlock[3]:
                           self.visit_tree(subTree)
                    else :
                        self.visit_tree(astBlock[3])
            else:
                self.print_parsing_error(19)
                print(astBlock)

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
    def __init__(self, pIndex, cIndex):
        self.pIndex = pIndex
        self.cIndex = cIndex

# Class for const Node
class ConstData():
    def __init__(self, data, index):
        self.data = data
        self.index = index