from Lang import *
from hypothesis import given, strategies as st
from evaluate import evaluate

# ========== GERADORES DE EXPRESSÕES ==========

@st.composite
def const_exprs(draw):
    val = draw(st.integers(min_value=-100, max_value=100))
    return Number(val)

# Gera variáveis x ou y.
@st.composite
def var_exprs(draw):
    name = draw(st.sampled_from(["x", "y"]))
    return Var(name)

# -------- EXPRESSÕES COM POSSÍVEIS ERROS (sem validação) --------

@st.composite
def compound_exprs(draw, depth=0):
    if depth > 2:
        return draw(st.one_of(const_exprs(), var_exprs()))

    expr_gen = st.deferred(lambda: compound_exprs(depth=depth + 1))
    e1 = draw(expr_gen)
    e2 = draw(expr_gen)

    op = draw(st.sampled_from([Add, Sub, Mul, Div, Eq, Greater, Less, GreaterEq, LessEq, Conj, Dis]))
    return op(e1, e2)

# -------- EXPRESSÕES SEGURAS (com validação) --------

@st.composite
def safe_div_expr(draw, depth=0):
    e1 = draw(compound_exprs_safe(depth=depth + 1))
    denom = draw(const_exprs().filter(lambda x: x.value != 0))
    return Div(e1, denom)

@st.composite
def compound_exprs_safe(draw, depth=0):
    if depth > 2:
        return draw(st.one_of(const_exprs(), var_exprs()))

    expr_gen = st.deferred(lambda: compound_exprs_safe(depth=depth + 1))
    e1 = draw(expr_gen)
    e2 = draw(expr_gen)

    op = draw(st.sampled_from([Add, Sub, Mul, Eq, Greater, Less, GreaterEq, LessEq, Conj, Dis]))
    return op(e1, e2)

@st.composite
def safe_expr(draw, depth=0):
    return draw(st.one_of(compound_exprs_safe(depth=depth), safe_div_expr(depth=depth)))

# ========== GERADORES DE CONTEÚDO ==========

@st.composite
def content_stmt(draw, depth=0, safe=False):
    expr = draw(safe_expr(depth=depth) if safe else compound_exprs(depth=depth))
    kind = draw(st.sampled_from(["ret", "atrib", "print"]))

    if kind == "ret":
        return Ret(expr)
    elif kind == "atrib":
        var_name = draw(st.sampled_from(["x", "y", "z"]))
        return Atrib(var_name, expr)
    elif kind == "print":
        return Print(expr)

@st.composite
def content_block(draw, depth=0, safe=False):
    stmts = draw(st.lists(content_stmt(depth=depth, safe=safe), min_size=1, max_size=3))
    return stmts

# ========== GERADORES DE FUNÇÕES ==========

@st.composite
def lang_function(draw):
    fname = draw(st.sampled_from(["foo", "bar", "baz", "gg"]))
    args = [Arg("int", "x"), Arg("int", "y")]
    body = draw(content_block(safe=False))
    return Function(name=fname, type="int", args=args, content=body)

@st.composite
def valid_lang_function(draw):
    fname = draw(st.sampled_from(["foo", "bar", "baz", "gg"]))
    args = [Arg("int", "x"), Arg("int", "y")]
    body = draw(content_block(safe=True))
    return Function(name=fname, type="int", args=args, content=body)

# ========== GERADOR DE INPUTS ==========

@st.composite
def random_inputs(draw):
    x_val = draw(st.integers(min_value=-100, max_value=100))
    y_val = draw(st.integers(min_value=-100, max_value=100))
    return [("x", x_val), ("y", y_val)]

# ========== TESTES ==========

@given(func=lang_function(), inputs=random_inputs())
def test_may_crash(func, inputs):
    print("\n[Possivelmente Inválida] Função gerada:")
    print(func)
    try:
        evaluate([func], inputs)
    except Exception:
        pass

@given(func=valid_lang_function(), inputs=random_inputs())
def test_valid_does_not_crash(func, inputs):
    print("\n[Válida] Função gerada:")
    print(func)
    try:
        evaluate([func], inputs)
    except Exception as e:
        assert False, f"Erro inesperado em função válida: {e}"

@given(func=valid_lang_function(), inputs=random_inputs())
def test_determinism(func, inputs):
    print("\n[Determinismo] Função gerada:")
    print(func)
    print("Inputs:", inputs)
    r1 = evaluate([func], inputs)
    r2 = evaluate([func], inputs)
    assert r1 == r2, "Função não é determinística!"

@given(const_exprs())
def test_const_expr_stable(expr):
    func = Function(name="test", type="int", args=[], content=[Ret(expr)])
    print("\n[Constante] Função gerada:")
    print(func)
    val1 = evaluate([func], [])
    val2 = evaluate([func], [])
    assert val1 == val2, "Expressão constante não é estável"

