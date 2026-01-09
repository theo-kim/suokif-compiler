import pytest
from suokif_compiler import Compiler

def test_compiler_initialization():
    compiler = Compiler()
    assert isinstance(compiler, Compiler)
    assert compiler.rules == []

def test_compile_basic_string():
    compiler = Compiler()
    result = compiler.compile("(instance Mary Human)")
    assert result == "Compiled: (instance Mary Human)"

def test_compile_empty_error():
    compiler = Compiler()
    with pytest.raises(ValueError):
        compiler.compile("")