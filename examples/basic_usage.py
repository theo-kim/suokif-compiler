import sys
import os

# Ensure we can import the package if running from the repo root without installing
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from suokif_compiler import Compiler

def main():
    kif_data = "(instance Gemini AI)"
    
    print(f"Input: {kif_data}")
    
    compiler = Compiler()
    try:
        output = compiler.compile(kif_data)
        print(output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()