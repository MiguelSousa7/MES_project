from Functions import *
from Parser import *
from evaluate import evaluate
from mutate import mutate
from optimize import opt
from refactor import refactor
from code_smells import code_smells
from instructions import instructions
from instrumentation import *
from Tests import *
from names import names  # Assegura-te de importar a função names

if __name__ == "__main__":
    exemplos = {
        "f1": f1,
        "f2": f2,
        "f3": f3,
        "f4": f4
    }

    while True:
        print("\n=== MENU ===")
        print("0 - Mostrar sintaxe original")
        print("1 - Mostrar Pretty-Printing")
        print("2 - Mostrar sintaxe otimizada")
        print("3 - Mostrar sintaxe refatorada")
        print("4 - Mostrar sintaxe otimizada + refatorada")
        print("5 - Contar Code Smells")
        print("6 - Contar instruções")
        print("7 - Mutação")
        print("8 - Executar função")
        print("9 - Testes")
        print("10 - Instrumentação")
        print("11 - Testes instrumentados")
        print("12 - Sair")

        escolha = input("Escolha uma opção (0 a 12): ")

        if escolha == "12":
            print("Saindo do programa...")
            break

        if escolha not in [str(i) for i in range(13)]:
            print("Opção inválida.")
            continue

        if escolha != "12":
            funcao_escolhida = input("Escolha um exemplo de função (f1, f2, f3, f4, f5, f6): ")
            if funcao_escolhida not in exemplos:
                print("Função inválida.")
                continue

            exemplo = exemplos[funcao_escolhida]

        if escolha == "0":
            print("\n--- Sintaxe Original ---\n")
            print(exemplo)
        elif escolha == "1":
            print("\n--- Pretty-Printing ---\n")
            print(str('\n\n'.join(str(f) for f in exemplo)))
            print("\n--- Nomes ---\n")
            names_list = names(exemplo)
            print(names_list)
        elif escolha == "2":
            print("\n--- Sintaxe Otimizada---\n")
            optimized = opt(exemplo)
            print(optimized)
        elif escolha == "3":
            print("\n--- Sintaxe Refatorada ---\n")
            refactored = refactor(exemplo)
            print(refactored)
        elif escolha == "4":
            print("\n--- Otimização + Refatoração ---\n")
            result = refactor(opt(exemplo))
            print(result)
            print("\n\n")
            for func in result:
                print(func)
        elif escolha == "5":
            print("\n--- Contagem de Code Smells ---\n")
            smells_result = code_smells(exemplo)
            print(smells_result)
        elif escolha == "6":
            print("\n--- Contagem de Instruções ---\n")
            instruction_result = instructions(exemplo)
            print(instruction_result)
        elif escolha == "7":
            print("\n--- Mutação ---\n")
            result = refactor(opt(exemplo))
            mutated = mutate(result)
            print("Original:")
            for func in result:
                print(func)

            print("\nMutado:")
            for func in mutated:
                print(func)

            if funcao_escolhida == "f1":
                testCases = testCasesf1
            elif funcao_escolhida == "f2":
                testCases = testCasesf2
            else:
                testCases = testCasesf3
            runTestSuite(mutated, testCases)
        elif escolha == "8":
            print("\n--- Executando Função ---\n")
            result = refactor(opt(exemplo))
            inputs = []
            for arg in exemplo[0].args:
                valor = input(f"Insira o valor para {arg.name} ({arg.type}): ")
                inputs.append((arg.name, int(valor)))
            resultado = evaluate(result, inputs)
            print(f"Resultado: {resultado}")
        elif escolha == "9":
            print("\n--- Testes ---\n")
            result = refactor(opt(exemplo))
            if funcao_escolhida == "f1":
                testCases = testCasesf1
            elif funcao_escolhida == "f2":
                testCases = testCasesf2
            elif funcao_escolhida == "f3":
                testCases = testCasesf3
            elif funcao_escolhida == "f4":
                testCases = testCasesf4
            runTestSuite(result, testCases)
        elif escolha == "10":
            print("\n--- Instrumentação ---\n")
            result = refactor(opt(exemplo))
            instrumented = instrumentation(result)
            print("Código instrumentado:")
            for func in instrumented:
                print(func)
        elif escolha == "11":
            print("\n--- Testes Instrumentados ---\n")
            result = refactor(opt(exemplo))
            if funcao_escolhida == "f1":
                testCases = testCasesf1
            elif funcao_escolhida == "f2":
                testCases = testCasesf2
            else:
                testCases = testCasesf3
            instrumentedTestSuite(result, testCases)
