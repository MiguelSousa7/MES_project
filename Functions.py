from Lang import *

f1 = [
    Function(
        "soma",
        "int",
        [Arg("int", "a"), Arg("int", "b")],
        [
            Atrib("soma", Add(Mul(Eq(Var("a"), Dis(true(), Conj(false(), true()))), Number(1)), Add(Var("b"), Number(0)))),
            Print(Var("soma")),
            Ret(Var("soma"))
        ]
    )
]

f2 = [
    Function(
        "soma_pares_ate",
        "int",
        [Arg("int", "limite")],
        [
            Atrib("soma", Number(0)),
            Atrib("i", Number(0)),

            IFE(
                Dis(GreaterEq(Var("limite"), Number(0)), Greater(Var("limite"), Number(-1))),
                [
                    For(
                        Atrib("i", Number(0)),
                        LessEq(Var("i"), Var("limite")),
                        Atrib("i", Add(Var("i"), Number(1))),
                        [
                            IFE(
                                Conj(Eq(Mod(Var("i"), Number(2)), Number(0)), true()),
                                [
                                    Atrib("soma", Add(Var("soma"), Var("i")))
                                ],
                                []
                            )
                        ]
                    )
                ],
                []
            ),

            IFE(
                Not(Eq(Var("soma"), Number(0))),
                [
                    Atrib("soma", Add(Var("soma"), Number(0)))
                ],
                []
            ),

            Ret(Var("soma"))
        ]
    )
]

f3 = [
    Function(
        "fatorial",
        "int",
        [Arg("int", "n")],
        [
            Atrib("fatorial", Number(1)),
            For(
                Atrib("i", Number(1)),
                LessEq(Var("i"), Var("n")),
                Atrib("i", Add(Var("i"), Number(1))),
                [
                    Atrib("fatorial", Mul(Var("fatorial"), Var("i")))
                ]
            ),

            Ret(Var("fatorial"))
        ]
    )
]

f4 = [
    Function(
        "fatorial_limite",
        "int",
        [Arg("int", "n")],
        [
            IFE(
                Less(Var("n"), Number(10)),
                [Ret(Number(-1))],
                []
            ),
            Atrib("res", Number(1)),
            For(
                Atrib("i", Number(1)),
                LessEq(Var("i"), Var("n")),
                Atrib("i", Add(Var("i"), Number(1))),
                [
                    Atrib("res", Mul(Var("res"), Var("i")))
                ]
            ),
            Ret(Var("res"))
        ]
    )
]