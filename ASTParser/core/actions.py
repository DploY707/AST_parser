class Action():
    def __init__(self, actionInfo):
        self.actionInfo = actionInfo
        self.type = actionInfo[0]

    def __repr__(self):
        return str(self.actionInfo)

class ArrayAccess(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.arr = actionInfo[1][0]
        self.ind = actionInfo[1][1]

    def set_arr(self, expr):
        self.arr = expr

    def set_ind(self, expr):
        self.ind = expr

class ArrayCreation(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.tn_and_params = actionInfo[1]
        self.dim = actionInfo[2]

    def set_tn_and_params(self, expr):
        self.tn_and_params = expr

    def set_dim(self, expr):
        self.dim = expr

class ArrayInitializer(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.params = actionInfo[1]

        # TODO : handle this case
        self.tn = actionInfo[2]

    def set_params(self, params):
        self.params = params

    def set_tn(self, tn):
        self.tn = tn

class Assignment(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.lhs = actionInfo[1][0]
        self.rhs = actionInfo[1][1]
        self.op = actionInfo[2]

    def set_lhs(self, expr):
        self.lhs = expr

    def set_rhs(self, expr):
        self.rhs = expr

    def set_op(self, expr):
        self.op = expr

class BinaryInfix(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.left = actionInfo[1][0]
        self.right = actionInfo[1][1]
        self.op = actionInfo[2]

    def set_left(self, expr):
        self.left = expr

    def set_right(self, expr):
        self.right = expr

    def set_op(self, expr):
        self.op = expr

class Cast(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.tn = actionInfo[1][0]
        self.arg = actionInfo[1][1]

    def set_tn(self, expr):
        self.tn = expr

    def set_arg(self, expr):
        self.arg = expr

class FieldAccess(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.left_arr = actionInfo[1]
        self.triple = actionInfo[2]

    def set_left_arr(self, left_arr):
        self.left_arr = left_arr

    def set_triple(self, triple):
        self.triple = triple

class Literal(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.result = actionInfo[1]
        self.tt = actionInfo[2]

class Local(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.name = actionInfo[1]

class MethodInvocation(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.params = actionInfo[1]
        self.triple = actionInfo[2]
        self.name = actionInfo[3]
        self.base_flag = actionInfo[4]

class Parenthesis(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.expr_arr = actionInfo[1]

class TypeName(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

        # TODO: what is dim?
        self.baset_and_dim = actionInfo[1]

class Unary(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.left_arr = actionInfo[1]
        self.op = actionInfo[2]
        self.isPostfix_flag = actionInfo[3] # when it false, it is a prefix

class Dummy(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class ClassInstanceCreation(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.triple = actionInfo[1]
        self.params = actionInfo[2]
        self.parse_descriptor = actionInfo[3]

    def set_triple(self, expr):
        self.triple = expr

    def set_params(self, expr):
        self.params = expr

    def set_parse_descriptor(self, expr):
        self.parse_descriptor = expr