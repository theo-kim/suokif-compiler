from dataclasses import dataclass, field
from typing import List, Any, Optional

@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    # source_text is populated after parsing to hold the original string slice
    source_text: Optional[str] = field(default=None, init=False, repr=False)

@dataclass
class Value(ASTNode):
    """Base class for literal values."""
    content: Any
    original_text: str

@dataclass
class String(Value):
    """Represents a string literal."""
    def __repr__(self) -> str:
        return f"String({self.original_text})"

@dataclass
class Number(Value):
    """Represents a numeric literal."""
    def __repr__(self) -> str:
        return f"Number({self.content})"

@dataclass
class Boolean(Value):
    """Represents a boolean literal."""
    def __repr__(self) -> str:
        return f"Boolean({self.content})"

@dataclass
class Symbol(ASTNode):
    """Represents a symbol identifier."""
    name: str

    def __repr__(self) -> str:
        return f"Symbol({self.name})"

@dataclass
class Variable(ASTNode):
    """Represents a variable identifier (starts with ?)."""
    name: str

    def __post_init__(self):
        if self.name.startswith('?'):
            self.name = self.name[1:]

    def __repr__(self) -> str:
        return f"Variable({self.name})"

@dataclass
class Expression(ASTNode):
    """Represents a nested list of terms (S-expression)."""
    children: List[ASTNode] = field(default_factory=list)

    def __repr__(self) -> str:
        if self.children and isinstance(self.children[0], Symbol):
            func_name = self.children[0].name
            args = ", ".join(repr(c) for c in self.children[1:])
            return f"{func_name}({args})"
        return f"Expression({self.children})"

@dataclass
class Operator(Expression):
    """Base class for SUO-KIF operators."""
    def __repr__(self) -> str:
        args = ", ".join(repr(c) for c in self.children)
        return f"{self.__class__.__name__}({args})"

@dataclass
class Conditional(Operator):
    """Represents the conditional operator (=>)."""
    pass

@dataclass
class Biconditional(Operator):
    """Represents the biconditional operator (<=>)."""
    pass

@dataclass
class And(Operator):
    """Represents the boolean and operator."""
    pass

@dataclass
class Or(Operator):
    """Represents the boolean or operator."""
    pass

@dataclass
class Not(Operator):
    """Represents the boolean not operator."""
    pass

@dataclass
class Exists(Operator):
    """Represents the existential quantifier (exists)."""
    pass

@dataclass
class Eq(Operator):
    """Represents the equality operator"""
    pass

@dataclass
class ForAll(Operator):
    """Represents the universal quantifier (forall)"""
    pass