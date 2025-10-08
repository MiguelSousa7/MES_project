from parsy import string, regex, seq, whitespace, alt, forward_declaration
from Lang import *

# === Helpers básicos ===
opt_ws = whitespace.optional()
lparen = string("(") << opt_ws
rparen = string(")") << opt_ws
lbrace = string("{") << opt_ws
rbrace = string("}") << opt_ws
semicolon = string(";") << opt_ws
lt_op = opt_ws >> string('<') << opt_ws
gt_op = opt_ws >> string('>') << opt_ws
le_op = opt_ws >> string('<=') << opt_ws
ge_op = opt_ws >> string('>=') << opt_ws

# === Literais e identificadores ===
def parse_number():
    return regex(r'\d+').map(lambda x: Number(int(x))).desc("number")

def parse_identifier():
    return regex(r'[a-zA-Z_][a-zA-Z0-9_]*').map(Var)

def parse_true():
    return string("true").result(true())

def parse_false():
    return string("false").result(false())

# === Expressões ===
def parse_expr():
    expr = forward_declaration()

    simple_expr = alt(
        parse_number(),
        parse_true(),
        parse_false(),
        parse_identifier(),
        seq(lparen >> expr << rparen)
    )

    not_expr = (opt_ws >> string("!") >> opt_ws >> simple_expr).map(lambda e: Not(e))
    eq_expr = seq(simple_expr, opt_ws >> string("==") << opt_ws, simple_expr).map(lambda t: Eq(t[0], t[2]))
    and_expr = seq(simple_expr, opt_ws >> string("&&") << opt_ws, simple_expr).map(lambda t: Conj(t[0], t[2]))
    or_expr = seq(simple_expr, opt_ws >> string("||") << opt_ws, simple_expr).map(lambda t: Dis(t[0], t[2]))
    mul_expr = seq(simple_expr, opt_ws >> string("*") << opt_ws, simple_expr).map(lambda t: Mul(t[0], t[2]))
    div_expr = seq(simple_expr, opt_ws >> string("/") << opt_ws, simple_expr).map(lambda t: Div(t[0], t[2]))
    add_expr = seq(simple_expr, opt_ws >> string("+") << opt_ws, simple_expr).map(lambda t: Add(t[0], t[2]))
    sub_expr = seq(simple_expr, opt_ws >> string("-") << opt_ws, simple_expr).map(lambda t: Sub(t[0], t[2]))
    greater_expr = seq(simple_expr, gt_op, simple_expr).map(lambda t: Greater(t[0], t[2]))
    greater_eq_expr = seq(simple_expr, ge_op, simple_expr).map(lambda t: GreaterEq(t[0], t[2]))
    less_expr = seq(simple_expr, lt_op, simple_expr).map(lambda t: Less(t[0], t[2]))
    less_eq_expr = seq(simple_expr, le_op, simple_expr).map(lambda t: LessEq(t[0], t[2]))

    expr.become(alt(
        eq_expr, not_expr, and_expr, or_expr,
        mul_expr, div_expr, add_expr, sub_expr, greater_eq_expr, greater_expr,
        less_eq_expr, less_expr,
        parse_true(), parse_false(), simple_expr
    ))

    return expr

# === Argumentos ===
def parse_arg():
    return seq(
        regex(r'(int|float|char|bool|void)') << whitespace.at_least(1),
        parse_identifier()
    ).map(lambda t: Arg(type=t[0], name=t[1].name))

def parse_args_list():
    return (
        lparen >>
        parse_arg().sep_by(string(',') << opt_ws) <<
        rparen
    ).map(lambda args: Args(args=args))

# === Instruções ===
def parse_stmt():
    expr = parse_expr()
    stmt = forward_declaration()
    content = forward_declaration()

    # Assignment (com ";")
    assign_stmt = seq(
        parse_identifier().map(lambda v: v.name),
        opt_ws >> string("=") << opt_ws,
        expr,
        semicolon
    ).map(lambda t: Atrib(name=t[0], exp=t[2]))

    # Return
    ret_stmt = (string("return") << whitespace.at_least(1) >> expr << semicolon).map(Ret)

    # If / Else
    if_stmt = seq(
        string("if") << whitespace.at_least(1) >> lparen,
        expr,
        rparen >> lbrace,
        content,
        rbrace,
        seq(string("else") << whitespace.at_least(1) >> lbrace, content, rbrace).optional()
    ).map(lambda t: IFE(exp=t[1], content=t[3], contentElse=t[5][1] if t[5] else []))

    # While
    while_stmt = seq(
        string("while") << whitespace.at_least(1) >> lparen,
        expr,
        rparen >> lbrace,
        content,
        rbrace
    ).map(lambda t: While(cond=t[1], content=t[3]))

    # Assignment sem ";" (para for)
    assign_expr = seq(
        parse_identifier().map(lambda v: v.name),
        opt_ws >> string("=") << opt_ws,
        expr
    ).map(lambda t: Atrib(name=t[0], exp=t[2]))

    # For
    for_stmt = seq(
        string("for") << whitespace.optional() >> lparen >> assign_expr << semicolon,
        expr << semicolon,
        assign_expr << rparen,
        lbrace >> content << rbrace
    ).map(lambda t: For(start=t[0], cond=t[1], end=t[2], content=t[3]))

    # Print
    print_stmt = (string("print") >> opt_ws >> lparen >> expr << rparen << semicolon).map(Print)

    stmt.become(alt(
        assign_stmt,
        ret_stmt,
        if_stmt,
        while_stmt,
        for_stmt,
        print_stmt
    ))

    content.become(stmt.at_least(1))
    return stmt

def parse_content():
    return parse_stmt().at_least(1)

# === Funções ===
def parse_function():
    type_kw = regex(r'(int|float|char|bool|void)') << whitespace.at_least(1)
    return seq(
        type_kw,
        parse_identifier().map(lambda v: v.name),
        parse_args_list(),
        lbrace >> parse_content() << rbrace
    ).map(lambda t: Function(type=t[0], name=t[1], args=t[2], content=t[3]))

# === Programa completo ===
def parse_program():
    return parse_function().many().map(lambda funcs: funcs)

# === Função principal ===
def parser(code: str) -> list[Function]:
    return parse_program().parse(code)

def run_tests(option):
    examples = {
        "2": [
            "int test() { x = 10; }",
            "int test() { y = x + 5; }"
        ],
        "3": [
            "int test() { return 2 + 3; }",
            "int test() { return x * 2; }"
        ],
        "4": [
            "int test() { if (x == 10) { return 1; } }",
            "int test() { if (x == 10) { x = 1; } else { x = 0; } }"
        ],
        "5": [
            "int test() { for (x = 0; x == 10; x = x + 1) { return x; } }"
        ],
        "6": [
            "int test() { while (x == 10) { x = x + 1; } }"
        ],
        "7": [
            "int soma(int x, int y) { x = x + y; return x; }", #funfa
            "void printHello() { return x; }", #funfa
            "int erro(int x) { x = x + ; return x; }", #erro
            "int soma(int x, int y) { x = x + y return x; }", #erro
            "int soma(int x, int y { x = x + y; return x; }", #erro
            "int soma(int x, int y) { x = x + y; return x;", #erro
            "inteiro soma(int x, int y) { x = x + y; return x; }", #erro
            "soma(int x, int y) { x = x + y; return x; }", #erro
            "int (int x, int y) { x = x + y; return x; }", #erro
            "int soma(x, y) { x = x + y; return x; }", #erro
            "int soma(int, int) { x = x + y; return x; }", #erro
            "return 5;", # erro
            "int soma(int x, int y) { x = ; return x; }", #erro
            "int soma(int x, int y) { return; }", #erro
            "int soma(int x, int y) { return x; return y; }", #erro
            "int soma(int x, int y) { z = x + y; return z; }", #funfa
            "int soma(int x, int y) { return \"texto\"; }", #erro
            "int soma(int x, int y) { while (x < 10) {x = x + 1;} return x; }", #funfa
            "int soma(int x, int y) { for (x = 0; x < 10 x = x + 1) { x = x + 1; } return x; }", #erro
            "int soma(int x, int y) { for x = 0; x < 10; x = x + 1 { x = x + 1; } return x; }", #erro
            "int soma(int x, int y) { while x < 10 { x = x + 1; } return x; }" #erro
        ],
        "8": [
            "int test(int x, float total) { return x; }"
        ],
        "9": [
            "int test() { return true && false; }",
            "int test() { return a || c; }"
        ],
        "10": [
            "int main() { print(x + 1); print(true && false); return 0; }"
        ]
    }

    selected = examples.get(option)
    if not selected:
        print("Opção inválida.")
        return

    print(f"\n=== Executando testes da opção {option} ===")
    for code in selected:
        try:
            print(f"\nCódigo:\n{code}")
            result = parser(code)
            print("AST:", repr(result))
        except Exception as e:
            print(f"Erro de sintaxe: {e}")

if __name__ == "__main__":
    while True:
        print("\n=== MENU DE TESTES ===")
        print("1 - Expressões simples")
        print("2 - Atribuição")
        print("3 - Return")
        print("4 - If Statement")
        print("5 - For Statement")
        print("6 - While Statement")
        print("7 - Funções (válidas e inválidas)")
        print("8 - Argumentos")
        print("9 - Conjunção e Disjunção")
        print("10 - Print Statement")
        print("0 - Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == "0":
            print("Saindo...")
            break
        else:
            run_tests(escolha)
