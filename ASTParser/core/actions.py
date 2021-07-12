class Action():
    def __init__(self, actionInfo):
        self.actionInfo = actionInfo

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

    def update_arrayAccess(actionInfo):
        self.actionInfo = actionInfo
        set_arr(actionInfo[1][0])
        set_ind(actionInfo[1][1])

class ArrayCreation(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.tn_and_params = actionInfo[1]
        self.dim = actionInfo[2]

    def set_tn_and_params(self, expr):
        self.tn_and_params = expr

    def set_dim(self, expr):
        self.dim = expr

    def update_arrayCreation(actionInfo):
        self.actionInfo = actionInfo
        set_tn_and_params(actionInfo[1])
        set_dim(actionInfo[2])

class ArrayInitializer(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.params = actionInfo[1]

        # TODO : handle this case
        self.tn = actionInfo[2]

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

    def update_assignment(actionInfo):
        self.actionInfo = actionInfo
        set_lhs(actionInfo[1][0])
        set_rhs(actionInfo[1][1])
        set_op(actionInfo[2])

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

    def update_binaryInfix(actionInfo):
        self.actionInfo = actionInfo
        set_left(actionInfo[1][0])
        set_right(actionInfo[1][1])
        set_op(actionInfo[2])


class Cast(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.left_arr = actionInfo[1]

class FieldAccess(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
        self.left_arr = actionInfo[1]
        self.triple = actionInfo[2]

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

class TypeName(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class Unary(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class Dummy(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class ClassInstanceCreation(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)
