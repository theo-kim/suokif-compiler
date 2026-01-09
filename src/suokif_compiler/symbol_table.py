from typing import Dict, List
from .ast import ASTNode

class SymbolTable:
    """
    Stores symbols and references to the AST nodes where they appear.
    """
    def __init__(self):
        self.table: Dict[str, List[ASTNode]] = {}

    def add_reference(self, symbol_name: str, node: ASTNode) -> None:
        if symbol_name not in self.table:
            self.table[symbol_name] = []
        self.table[symbol_name].append(node)

    def __repr__(self) -> str:
        return f"SymbolTable({list(self.table.keys())})"