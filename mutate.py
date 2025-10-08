from Lang import *
import random

def random_mutation(node):
    """
    Aplica uma mutação aleatória apenas a operações básicas (soma, subtração, multiplicação, divisão).
    """
    match node:
        case Add(exp1, exp2):
            print("Mutação: Add -> Sub")
            return Sub(exp1, exp2)
        case Sub(exp1, exp2):
            print("Mutação: Sub -> Add")
            return Add(exp1, exp2)
        case Mul(exp1, exp2):
            print("Mutação: Mul -> Div")
            return Div(exp1, exp2)
        case Div(exp1, exp2):
            print("Mutação: Div -> Mul")
            return Mul(exp1, exp2)
        
        case _:
            print("Nenhuma mutação aplicada ao nó:", node)
            return node

def mutate(ast):
    """
    Aplica uma mutação aleatória a um programa Lang (AST).
    Retorna o AST modificado.
    """
    def traverse_and_mutate(node):
        if isinstance(node, (Add, Sub, Mul, Div)) and random.random() < 1:  # 100% de chance de mutar o nó atual
            print("A tentar mutar o nó:", node)
            mutated_node = random_mutation(node)
            if mutated_node != node:
                print("Mutação aplicada:", mutated_node)
            return mutated_node

        match node:
            case Function(name, type, args, content):
                return Function(
                    name,
                    type,
                    args,
                    [traverse_and_mutate(stmt) for stmt in content]
                )
            case Atrib(name, exp):
                return Atrib(name, traverse_and_mutate(exp))
            
            case IFE(exp, content, contentElse):
                return IFE(
                    traverse_and_mutate(exp),
                    [traverse_and_mutate(stmt) for stmt in content],
                    [traverse_and_mutate(stmt) for stmt in contentElse]
                )
            case For(start, cond, end, content):
                return For(
                    traverse_and_mutate(start),
                    traverse_and_mutate(cond),
                    traverse_and_mutate(end),
                    [traverse_and_mutate(stmt) for stmt in content]
                )
            case While(cond, content):
                return While(
                    traverse_and_mutate(cond),
                    [traverse_and_mutate(stmt) for stmt in content]
                )
            case Add(exp1, exp2):
                return Add(traverse_and_mutate(exp1), traverse_and_mutate(exp2))
            case Sub(exp1, exp2):
                return Sub(traverse_and_mutate(exp1), traverse_and_mutate(exp2))
            case Mul(exp1, exp2):
                return Mul(traverse_and_mutate(exp1), traverse_and_mutate(exp2))
            case Div(exp1, exp2):
                return Div(traverse_and_mutate(exp1), traverse_and_mutate(exp2))
            case _:
                return node

    print("Iniciando mutação no AST...")
    mutated_ast = [traverse_and_mutate(func) for func in ast]
    print("Mutação concluída.")
    return mutated_ast