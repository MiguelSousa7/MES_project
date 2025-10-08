from Lang import *

def evaluate(ast, inputs):
    """
    Avalia um programa Lang (AST) com os inputs fornecidos.
    """
    environment = {var: value for var, value in inputs}

    def eval_exp(exp):
        match exp:
            case Number(value):
                return value
            case Var(name):
                if name in environment:
                    return environment[name]
                else:
                    raise ValueError(f"Variável '{name}' não inicializada.")
            case Add(exp1, exp2):
                return eval_exp(exp1) + eval_exp(exp2)
            case Sub(exp1, exp2):
                return eval_exp(exp1) - eval_exp(exp2)
            case Mul(exp1, exp2):
                return eval_exp(exp1) * eval_exp(exp2)
            case Div(exp1, exp2):
                return eval_exp(exp1) // eval_exp(exp2)
            case Mod(exp1, exp2):
                return eval_exp(exp1) % eval_exp(exp2)
            case Eq(exp1, exp2):
                return eval_exp(exp1) == eval_exp(exp2)
            case Not(exp):
                return not eval_exp(exp)
            case Conj(exp1, exp2):
                return eval_exp(exp1) and eval_exp(exp2)
            case Dis(exp1, exp2):
                return eval_exp(exp1) or eval_exp(exp2)
            case Greater(exp1, exp2):
                return eval_exp(exp1) > eval_exp(exp2)
            case GreaterEq(exp1, exp2):
                return eval_exp(exp1) >= eval_exp(exp2)
            case Less(exp1, exp2):
                return eval_exp(exp1) < eval_exp(exp2)
            case LessEq(exp1, exp2):
                return eval_exp(exp1) <= eval_exp(exp2)
            case true():
                return True
            case false():
                return False
            case _:
                raise ValueError(f"Expressão desconhecida: {exp}")

    def exec_stmt(stmt):
        match stmt:
            case Atrib(name, exp):
                environment[name] = eval_exp(exp)
            case Ret(exp):
                return eval_exp(exp)
            case IFE(cond, content, contentElse):
                if eval_exp(cond):
                    for stmt in content:
                        result = exec_stmt(stmt)
                        if result is not None:
                            return result
                else:
                    for stmt in contentElse:
                        result = exec_stmt(stmt)
                        if result is not None:
                            return result
            case For(start, cond, end, content):
                exec_stmt(start)
                while eval_exp(cond):
                    for stmt in content:
                        result = exec_stmt(stmt)
                        if result is not None:
                            return result
                    exec_stmt(end)
            case While(cond, content):
                while eval_exp(cond):
                    for stmt in content:
                        result = exec_stmt(stmt)
                        if result is not None:
                            return result
            case Print(exp):
                if isinstance(exp, str):
                    print(exp)
                else:
                    print(eval_exp(exp))
            case _:
                raise ValueError(f"Instrução desconhecida: {stmt}")

    for stmt in ast[0].content:
        result = exec_stmt(stmt)
        if result is not None:
            return result
    return None