from Lang import *

def optEq(x,y):
    match(x,y):
        case (_, true()):
            return x
        case (true(), _):
            return y
        case (_, false()):
            return Not(x)
        case (false(), _):
            return Not(y)
        
def exprRefact(exp):
    match exp:
        case IFE(x, [Ret(true())], [Ret(false())]):
            return x
        case IFE(true(), [Ret(x)], [Ret(y)]):
            return x
        case Eq(x, true()) | Eq(true(), x):
            return optEq(x, true())
        case Eq(x, false()) | Eq(false(), x):
            return optEq(x, false())
        case _:
            raise st.StrategicError



def refactor(ast):
    return st.innermost(lambda x: st.adhocTP(st.failTP, exprRefact, x), obj(ast)).node()