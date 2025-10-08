import pytest
from Lang import *
from evaluate import *
from Functions import *

def runTestSuite(ast, testCases):
    all_passed = True

    for inputs, expected_result in testCases:
        try:
            actual_result = evaluate(ast, inputs)
            assert actual_result == expected_result, f"Falhou: Esperado {expected_result}, Obtido {actual_result}"
            print("Passou")
        except AssertionError as e:
            print(e)
            all_passed = False
        except Exception as e:
            print(f"Erro durante o teste: {e}")
            all_passed = False

    return all_passed

testCasesf1 = [
    ([("a", 5), ("b", 10)], 15),
    ([("a", 20), ("b", 50)], 70),
    ([("a", 0), ("b", 0)], 0),    
    ([("a", -5), ("b", 5)], 0),
]

testCasesf2 = [
    ([("limite", 5)], 6),
    ([("limite", 10)], 30),
    ([("limite", 0)], 0),
    ([("limite", -5)], 0),
]

testCasesf3 = [
    ([("n", 5)], 120),
    ([("n", 4)], 24),
    ([("n", 6)], 720),
]

testCasesf4 = [([("n", 5)], 120),
               ([("n", 6)], 720),
               ([("n", 10)], 3628800)
]