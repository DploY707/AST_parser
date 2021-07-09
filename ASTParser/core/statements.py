class Statement():
    def __init__(self, stmtInfo):
        self.stmtInfo = stmtInfo

    def __repr__(self):
        return str(self.stmtInfo)

class ExpressionStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.expr = stmtInfo[1]

class LocalDeclarationStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.expr = stmtInfo[1]
        self.decl = stmtInfo[2]

class ReturnStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.expr = stmtInfo[1]

class ThrowStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.expr = stmtInfo[1]

class JumpStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.keyword = stmtInfo[1]
        self.emptyField = stmtInfo[2]

        # TODO: handle stmtInfo[2]

class DoStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.cond_expr = stmtInfo[2]
        self.body_expr = stmtInfo[3]

    def set_cond_expr(self, expr):
        self.cond_expr = expr

    def set_body_expr(self, expr):
        self.body_expr = expr

    def update_doStatement(self, stmtInfo):
        self.stmtInfo = stmtInfo
        self.set_cond_expr(stmtInfo[2])
        self.set_body_expr(stmtInfo[3])

class WhileStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.cond_expr = stmtInfo[2]
        self.body_expr = stmtInfo[3]

    def set_cond_expr(self, expr):
        self.cond_expr = expr

    def set_body_expr(self, expr):
        self.body_expr = expr

    def update_whileStatement(self, stmtInfo):
        self.stmtInfo = stmtInfo
        self.set_cond_expr(stmtInfo[2])
        self.set_body_expr(stmtInfo[3])

class TryStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.tryb_expr = stmtInfo[2]
        self.pairs_expr = stmtInfo[3]

class IfStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.cond_expr = stmtInfo[2]
        self.scop_expr = stmtInfo[3]

    def set_cond_expr(self, expr):
        self.cond_expr = expr

    def set_scop_expr(self, expr):
        self.scop_expr = expr

    def update_ifStatement(self, stmtInfo):
        self.stmtInfo = stmtInfo
        self.set_cond_expr(stmtInfo[2])
        self.set_scop_expr(stmtInfo[3])

class SwitchStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        # TODO:


# Block state is a special statement
# TODO : What is block stat is?
class BlockStatement(Statement):
    def __init__(self, stmtInfo):
        super().__init__(stmtInfo)
        self.expr = stmtInfo[2]