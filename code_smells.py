from Lang import *

def detectSmells(x):
    match x:
        case IFE(_, [Ret(true())], [Ret(false())]):
            return [("RedundantReturn", 1)]
        case Mul(Number(0), _) | Mul(_, Number(0)):
            return [("UselessMulZero", 1)]
        case Mul(Number(1), _) | Mul(_, Number(1)):
            return [("UselessMulOne", 1)]
        case Add(Number(0), _) | Add(_, Number(0)):
            return [("UselessAddZero", 1)]
        case Dis(true(), _) | Dis(_, true()):
            return [("UselessOrTrue", 1)]
        case Conj(false(), _) | Conj(_, false()):
            return [("UselessAndFalse", 1)]
        case _:
            raise st.StrategicError

def code_smells(z):
    # Collect list of (smell, count) pairs
    pairs = st.full_tdTU(lambda x: st.adhocTU(st.failTU, detectSmells, x), obj(z))
    # Aggregate into a dictionary
    result = defaultdict(int)
    for smell, count in pairs:
        result[smell] += count
    return dict(result)