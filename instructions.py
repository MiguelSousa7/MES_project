from collections import defaultdict
from Lang import *

def countInstruction(x):
    match x:
        case Atrib(_, _):
            return [("Atrib", 1)]
        case IFE(_, _, _):
            return [("IFE", 1)]
        case Ret(_):
            return [("Ret", 1)]
        case For(_, _, _, _):
            return [("For", 1)]
        case While(_, _):
            return [("While", 1)]
        case _:
            raise st.StrategicError

def instructions(z):
    pairs = st.full_tdTU(lambda x: st.adhocTU(st.failTU, countInstruction, x), obj(z))
    result = defaultdict(int)
    for instr, count in pairs:
        result[instr] += count
    return dict(result)