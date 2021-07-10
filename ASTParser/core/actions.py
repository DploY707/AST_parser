class Action():
    def __init__(self, actionInfo):
        self.actionInfo = actionInfo

    def __repr__(self):
        return str(self.actionInfo)

class ArrayAccess(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class ArrayCreation(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class ArrayInitializer(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class Assignment(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class BinaryInfix(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class Cast(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class FieldAccess(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class Literal(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class Local(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

class MethodInvocation(Action):
    def __init__(self, actionInfo):
        super().__init__(actionInfo)

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
