import re
from typing import List, Optional
from .ast import (
    ASTNode, Value, Symbol, Variable, Expression, String, Number, Boolean,
    Operator, Conditional, Biconditional, And, Or, Not, Exists
)
from .symbol_table import SymbolTable

class Compiler:
    """
    Main class for the SUO-KIF Compiler.
    """
    def __init__(self):
        self.ast: List[ASTNode] = []
        self.symbol_table = SymbolTable()

    def compile(self, kif_string: str) -> str:
        """
        Parses SUO-KIF string, builds AST and Symbol Table.
        
        Args:
            kif_string (str): The raw KIF data.
            
        Returns:
            str: A string representation of the parsed AST.
        """
        if not kif_string:
            raise ValueError("Input cannot be empty")
        
        tokens = self._tokenize(kif_string)
        self.ast = self._parse(tokens)
        self._build_symbol_table(self.ast)
        
        return f"Compiled AST: {self.ast}"

    def compile_file(self, file_path: str, start_line: int = 1, end_line: Optional[int] = None) -> str:
        """
        Reads a SUO-KIF file and compiles it, optionally within a line range.

        Args:
            file_path (str): Path to the .kif file.
            start_line (int): The starting line number (1-based, inclusive).
            end_line (Optional[int]): The ending line number (1-based, inclusive).

        Returns:
            str: The compiled output.
        """
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        start_idx = max(0, start_line - 1)
        subset = lines[start_idx:end_line] if end_line is not None else lines[start_idx:]
        return self.compile("".join(subset))

    def _tokenize(self, text: str) -> List[str]:
        """Tokenizes the input string into Lisp-like tokens."""
        token_pattern = re.compile(r';[^\n]*|"[^"]*"|\(|\)|[^\s()]+')
        return [t for t in token_pattern.findall(text) if not t.startswith(';')]

    def _parse(self, tokens: List[str]) -> List[ASTNode]:
        """Parses a list of tokens into a list of ASTNodes."""
        stack: List[List[ASTNode]] = [[]]
        
        for token in tokens:
            if token == '(':
                new_expr: List[ASTNode] = []
                stack.append(new_expr)
            elif token == ')':
                if len(stack) <= 1:
                    raise ValueError("Unexpected ')'")
                finished_expr_list = stack.pop()
                expr_node = Expression(children=finished_expr_list)
                stack[-1].append(expr_node)
            else:
                stack[-1].append(self._create_atom(token))
        
        if len(stack) != 1:
            raise ValueError("Unclosed '('")
        return stack[0]

    def _create_atom(self, token: str) -> ASTNode:
        """Determines if a token is a Symbol, Variable, or Value."""
        if token.startswith('"') or token.startswith('`'):
            return String(content=token, original_text=token)
        
        if token.startswith('?'):
            return Variable(name=token)

        if token == "true":
            return Boolean(content=True, original_text=token)
        if token == "false":
            return Boolean(content=False, original_text=token)

        if token == "=>":
            return Conditional()
        if token == "<=>":
            return Biconditional()
        if token == "and":
            return And()
        if token == "or":
            return Or()
        if token == "not":
            return Not()
        if token == "exists":
            return Exists()

        try:
            val = float(token)
            return Number(content=val, original_text=token)
        except ValueError:
            return Symbol(name=token)

    def _build_symbol_table(self, nodes: List[ASTNode]) -> None:
        """Populates the symbol table by traversing the AST."""
        self.symbol_table = SymbolTable()
        for node in nodes:
            self._traverse_and_collect(node, parent=None)

    def _traverse_and_collect(self, node: ASTNode, parent: Optional[Expression]) -> None:
        if isinstance(node, Expression):
            for child in node.children:
                self._traverse_and_collect(child, parent=node)
        elif isinstance(node, Symbol):
            ref_node = parent if parent else node
            self.symbol_table.add_reference(node.name, ref_node)