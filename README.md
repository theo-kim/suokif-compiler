# SUO-KIF Compiler

A Python library for compiling SUO-KIF (Standard Upper Ontology Knowledge Interchange Format). Thsi will produce a compiled binary of an ontology

## Installation

```bash
pip install suokif-compiler
```

## Usage

```python
from suokif_compiler import Compiler

compiler = Compiler()
result = compiler.compile("(instance Mary Human)")
print(result)
```

## Development

To install dependencies and run tests:

```bash
pip install -e .[dev]
pytest
```