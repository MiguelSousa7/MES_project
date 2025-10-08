from Lang import *

def optDis(x,y):
    match(x, y):
        case true(), _:
            return true()
        case _, true():
            return true()
        case false(), false():
            return false()
        case _, _:
            raise st.StrategicError

def optConj(x,y):   
    match(x, y):
        case false(), _:
            return false()
        case _, false():
            return false()
        case true(), true():
            return true()
        case _, _:
            raise st.StrategicError

def optAdd(x, y):
    match(x, y):
        case Number(0), _:
            return y
        case _, Number(0):
            return x
        case Number(xx), Number(yy):
            return Number(xx + yy)
        case _:
            raise st.StrategicError

def optMul(x,y):
    match(x, y):
        case (Number(0), _) | (_, Number(0)):
            return Number(0)
        case _, Number(1):
            return x
        case Number(1), _:
            return y
        case Number(xx), Number(yy):
            return Number(xx * yy)
        case _:
            raise st.StrategicError

def expr(exp):
    match exp:
        case Dis(x, y):
            return optDis(x, y)
        case Conj(x, y):
            return optConj(x, y)
        case Add(x, y):
            return optAdd(x, y)
        case Mul(x, y):
            return optMul(x, y)
        case _:
            raise st.StrategicError

def opt(z):
    return st.innermost(lambda x: st.adhocTP(st.failTP, expr, x), obj(z)).node()