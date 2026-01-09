from dataclasses import dataclass, field
from typing import List, Any

@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass

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
class Operator(ASTNode):
    """Base class for SUO-KIF operators."""
    pass

@dataclass
class Conditional(Operator):
    """Represents the conditional operator (=>)."""
    def __repr__(self) -> str:
        return "Conditional(=>)"

@dataclass
class Biconditional(Operator):
    """Represents the biconditional operator (<=>)."""
    def __repr__(self) -> str:
        return "Biconditional(<=>)"

@dataclass
class And(Operator):
    """Represents the boolean and operator."""
    def __repr__(self) -> str:
        return "And(and)"

@dataclass
class Or(Operator):
    """Represents the boolean or operator."""
    def __repr__(self) -> str:
        return "Or(or)"

@dataclass
class Not(Operator):
    """Represents the boolean not operator."""
    def __repr__(self) -> str:
        return "Not(not)"

@dataclass
class Exists(Operator):
    """Represents the existential quantifier (exists)."""
    def __repr__(self) -> str:
        return "Exists(exists)"

@dataclass
class Expression(ASTNode):
    """Represents a nested list of terms (S-expression)."""
    children: List[ASTNode] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Expression({self.children})"