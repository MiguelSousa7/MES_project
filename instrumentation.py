from Lang import *
from Tests import *

def instrumentation(ast: Lang) -> Lang:
    """
    Instrumenta um programa Lang para auxiliar na localização de falhas.
    Adiciona instruções Print para monitorar o estado do programa.
    """
    def instrument_node(node):
        match node:
            case Function(name, type, args, content):
                instrumented_content = []
                instrumented_content.append(Print(f"Entrar na função {name}"))
                for stmt in content:
                    instrumented_content.extend(instrument_node(stmt))
                instrumented_content.append(Print(f"Saiu da função {name}"))
                return [Function(name, type, args, instrumented_content)]

            case Atrib(name, exp):
                return [
                    Print(f"Expressão {name} = {exp}"),
                    Atrib(name, exp)
                ]

            case IFE(cond, content, contentElse):
                return [
                    Print(f"Entrando no bloco if com cond = {cond}")
                ] + instrument_node_list(content) + [
                    Print(f"Entrando no bloco else com cond = {cond}")
                ] + instrument_node_list(contentElse)

            case For(start, cond, end, content):
                return (
                    instrument_node(start) +
                    [Print(f"Iniciando iteração do for com cond = {cond}")] +
                    instrument_node_list(content) +
                    instrument_node(end) + 
                    [Print(f"Finalizando iteração do for com cond = {cond}")]
                )

            case While(cond, content):
                return [
                    Print(f"Iniciando iteração do while com cond = {cond}")
                ] + instrument_node_list(content) + [
                    Print(f"Finalizando iteração do while com cond = {cond}")
                ]

            case Ret(exp):
                return [
                    Print(f"Retornando {exp}"),
                    Ret(exp)
                ]

            case Print(exp):
                return [Print(exp)]

            case _:
                return [node]

    def instrument_node_list(nodes):
        """
        Instrumenta uma lista de nós e retorna uma lista linear de instruções.
        """
        instrumented = []
        for node in nodes:
            instrumented.extend(instrument_node(node))
        return instrumented

    return [func for node in ast for func in instrument_node(node)]

def instrumentedTestSuite(ast, test_cases):
    instrumented_ast = instrumentation(ast)
    
    all_passed = True

    for inputs, expected_result in test_cases:
        try:
            print("\n--- Executando Teste ---")
            actual_result = evaluate(instrumented_ast, inputs)
            
            assert actual_result == expected_result, f"Falhou: Esperado {expected_result}, Obtido {actual_result}"
            print("Passou")
        except AssertionError as e:
            print(e)
            all_passed = False
        except Exception as e:
            print(f"Erro durante o teste: {e}")
            all_passed = False

    return all_passed