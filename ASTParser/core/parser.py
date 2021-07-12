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
# from core.actions import Cast
from core.actions import FieldAccess
from core.actions import Literal
from core.actions import Local
from core.actions import MethodInvocation
# from core.actions import Parenthesis
# from core.actions import TypeName
# from core.actions import Unary
# from core.actions import Dummy

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

    def print_parsing_error(self, errorType):
        if errorType == 1:
            self.errMsg = 'AST is not loaded, so you have to load it first'
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
            self.errMsg = 'Wrong operand in Local MethodInvocation'
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
                    self.parsedNodes[tryStmtNodeIndex].nodeInfo.update_tryStatement(stmt)
                else:
                    ts = TryStatement(stmt)
                    stmtNode = ASTNode(ts, tryStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if astBlock[3] is None:
                    self.print_parsing_error(3)
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
                    self.parsedNodes[switchStmtNodeIndex].nodeInfo.update_switchStatement(stmt)
                else:
                    ss = SwitchStatement(stmt)
                    stmtNode = ASTNode(ss, switchStmtNodeIndex)

                    self.parsedNodes.append(stmtNode)

                if astBlock[3] is None:
                    self.print_parsing_error(4)
                else:
                    self.visit_pairs(astBlock[3])

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

        elif astBlock[0] == 'TypeName':
            action = copy_instance(astBlock)

        elif astBlock[0] == 'Unary':
            action = copy_instance(astBlock)

        elif astBlock[0] == 'Dummy':
            action = copy_instance(astBlock)

        elif astBlock[0] == 'ClassInstanceCreation':
            action = copy_instance(astBlock)

        else:
            # TODO : Handle the unknown type of actions
            print(astBlock)

            tmp_instance = copy_instance(astBlock)

            tmp_action = Action(tmp_instance)

            actionNode = ASTNode(tmp_action, len(self.parsedNodes))
            self.parsedNodes.append(actionNode)

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