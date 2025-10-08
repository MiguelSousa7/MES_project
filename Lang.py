from pyztrategic.zipper import obj
import pyztrategic.strategy as st
import random

from collections import defaultdict
from dataclasses import dataclass

type Lang = list[Function]

type Args = list[Arg]

type Content = IFE | Ret | Atrib | For | While

type Exp = Add | Mul | Sub | Div | Var | Number | true | false | Eq | Not

@dataclass
class Function:
    name: str
    type: str
    args: Args
    content: list[Content]
    def __str__(self):
        args_str = ', '.join(str(arg) for arg in self.args)
        content_str = '\n'.join(f'    {str(stmt)}' for stmt in self.content)
        return f"{self.type} {self.name}({args_str}) {{\n{content_str}\n}}"
    
#feito
@dataclass
class Arg:
    type: str
    name : str
    def __str__(self):
        return f"{self.type} {self.name}"

@dataclass
class Args:
    args: list[Arg]
    def __str__(self):
        return ', '.join(str(arg) for arg in self.args)

#feito   
@dataclass
class Ret:
    exp: Exp
    def __str__(self):
        return f"return {self.exp};"
    
#feito
@dataclass
class IFE:
    exp: Exp
    content: list[Content]
    contentElse: list[Content]
    def __str__(self):
        if_str = f"if ({self.exp}) \n" + '\n'.join(f'\t{str(stmt)}' for stmt in self.content) + "\n}"
        if self.contentElse:
            else_str = " else {\n" + '\n'.join(f'\t{str(stmt)}' for stmt in self.contentElse) + "\n}"
            return if_str + else_str
        return if_str

#feito
@dataclass
class Atrib:
    name: str
    exp: Exp
    def __str__(self):
        return f"{self.name} = {self.exp};"

#feito
@dataclass
class For:
    start: Exp
    cond: Exp
    end: Exp
    content: list[Content]
    def __str__(self):
        body = '\n'.join(f'    {str(stmt)}' for stmt in self.content)
        return f"for ({self.start}; {self.cond}; {self.end}) {{\n{body}\n}}"

#feito
@dataclass
class While:
    cond: Exp
    content: list[Content]
    def __str__(self):
        body = '\n'.join(f'    {str(stmt)}' for stmt in self.content)
        return f"while ({self.cond}) {{\n{body}\n}}"
    
#feito
@dataclass
class Add:
    exp1: Exp
    exp2: Exp
    def __str__(self):
        return f"({self.exp1} + {self.exp2})"
    
#feito
@dataclass
class Sub:
    exp1: Exp
    exp2: Exp
    def __str__(self):
        return f"({self.exp1} - {self.exp2})"
    
#feito
@dataclass
class Div:
    exp1: Exp
    exp2: Exp
    def __str__(self):
        return f"({self.exp1} / {self.exp2})"
    
#feito
@dataclass
class Mul:
    exp1: Exp
    exp2: Exp
    def __str__(self):
        return f"({self.exp1} * {self.exp2})"
    
@dataclass
class Mod:
    exp1: Exp
    exp2: Exp
    def __str__(self):
        return f"({self.exp1} % {self.exp2})"

#feito
@dataclass
class Var:
    name: str
    def __str__(self):
        return self.name

#feito
@dataclass
class Number:
    value: int
    def __str__(self):
        return str(self.value)

#feito
@dataclass
class true:
    pass
    def __str__(self):
            return "true"

#feito
@dataclass
class false:
    pass
    def __str__(self):
        return "false"

#feito
@dataclass
class Eq:
    exp1: Exp
    exp2: Exp
    def __str__(self):
        return f"({self.exp1} == {self.exp2})"

#feito
@dataclass
class Not:
    exp: Exp
    def __str__(self):
        return f"!{self.exp}"

@dataclass
class Dis:
    exp1 : Exp
    exp2 : Exp
    def __str__(self):
        return f"({self.exp1} || {self.exp2})"

@dataclass
class Conj:
    exp1 : Exp
    exp2 : Exp
    def __str__(self):
        return f"({self.exp1} && {self.exp2})"
    
@dataclass
class Greater:
    exp1 : Exp
    exp2 : Exp
    def __str__(self):
        return f"({self.exp1} > {self.exp2})"
    
@dataclass
class GreaterEq:
    exp1 : Exp
    exp2 : Exp
    def __str__(self):
        return f"({self.exp1} >= {self.exp2})"
    
@dataclass
class Less:
    exp1 : Exp
    exp2 : Exp
    def __str__(self):
        return f"({self.exp1} < {self.exp2})"
  
@dataclass
class LessEq:
    exp1 : Exp
    exp2 : Exp
    def __str__(self):
        return f"({self.exp1} <= {self.exp2})"

@dataclass
class Array:
    elements: list[Exp]
    def __str__(self):
        return "[" + ", ".join(str(e) for e in self.elements) + "]"

@dataclass
class Print:
    exp: Exp | str
    def __str__(self):
        return f"print({self.exp});"