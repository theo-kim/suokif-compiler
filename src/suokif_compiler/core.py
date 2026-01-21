import re
from typing import List, Optional
from .ast import (
    ASTNode, Value, Symbol, Variable, Expression, String, Number, Boolean,
    Operator, Conditional, Biconditional, And, Or, Not, Exists, ForAll,
    Eq
)
from .symbol_table import SymbolTable

class Compiler:
    """
    Main class for the SUO-KIF Compiler.
    """
    def __init__(self):
        self.ast: List[ASTNode] = []
        self.symbol_table = SymbolTable()

    def compile(self, kif_string: str) -> List[ASTNode]:
        """
        Parses SUO-KIF string, builds AST and Symbol Table.
        
        Args:
            kif_string (str): The raw KIF data.
            
        Returns:
            List[ASTNode]: The list of parsed AST nodes.
        """
        if not kif_string:
            raise ValueError("Input cannot be empty")
        
        tokens = self._tokenize(kif_string)
        self.ast = self._parse(tokens, kif_string)
        self._build_symbol_table(self.ast)
        
        return self.ast

    def find_symbol_usages(self, symbol_name: str) -> List[ASTNode]:
        """
        Finds all expressions containing the specified symbol.

        Args:
            symbol_name (str): The name of the symbol to find.

        Returns:
            List[ASTNode]: A list of AST nodes where the symbol appears.
        """
        return self.symbol_table.get_references(symbol_name)

    def compile_file(self, file_path: str, start_line: int = 1, end_line: Optional[int] = None) -> List[ASTNode]:
        """
        Reads a SUO-KIF file and compiles it, optionally within a line range.

        Args:
            file_path (str): Path to the .kif file.
            start_line (int): The starting line number (1-based, inclusive).
            end_line (Optional[int]): The ending line number (1-based, inclusive).

        Returns:
            List[ASTNode]: The compiled output.
        """
        with open(file_path, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        start_idx = max(0, start_line - 1)
        subset = lines[start_idx:end_line] if end_line is not None else lines[start_idx:]
        return self.compile("".join(subset))

    def _tokenize(self, text: str) -> List[tuple]:
        """
        Tokenizes the input string into Lisp-like tokens.
        Returns a list of (token_text, start_index, end_index).
        """
        token_pattern = re.compile(r';[^\n]*|"[^"]*"|\(|\)|[^\s()]+')
        tokens = []
        for match in token_pattern.finditer(text):
            token_text = match.group()
            if not token_text.startswith(';'):
                tokens.append((token_text, match.start(), match.end()))
        return tokens

    def _parse(self, tokens: List[tuple], original_text: str) -> List[ASTNode]:
        """Parses a list of tokens into a list of ASTNodes."""
        stack: List[List[ASTNode]] = [[]]
        starts: List[int] = []  # Track start indices of open expressions
        
        for token, start, end in tokens:
            if token == '(':
                new_expr: List[ASTNode] = []
                stack.append(new_expr)
                starts.append(start)
            elif token == ')':
                if len(stack) <= 1:
                    raise ValueError("Unexpected ')'")
                finished_expr_list = stack.pop()
                expr_start = starts.pop()
                
                node = None
                if finished_expr_list and isinstance(finished_expr_list[0], Operator):
                    node = finished_expr_list[0]
                    node.children = finished_expr_list[1:]
                else:
                    node = Expression(children=finished_expr_list)
                
                node.source_text = original_text[expr_start:end]
                stack[-1].append(node)
            else:
                atom = self._create_atom(token)
                atom.source_text = original_text[start:end]
                stack[-1].append(atom)
        
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
        if token == "=" :
            return Eq()
        if token == "forall" :
            return ForAll()

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