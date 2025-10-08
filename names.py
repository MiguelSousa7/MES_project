from Lang import *

def names(ast):
    def getName(node):
        match node:
            case Function(name, _, _, _):
                return [name]
            case Arg(_, name):
                return [name]
            case Atrib(name, _):
                return [name]
            case Var(name):
                return [name]
            case _:
                return []

    nomes = st.full_tdTU(
        lambda x: st.adhocTU(st.failTU, getName, x),
        obj(ast)
    )
    return list(set(nomes))
