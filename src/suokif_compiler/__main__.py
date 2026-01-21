import argparse
import sys
from .core import Compiler

def main():
    parser = argparse.ArgumentParser(description="SUO-KIF Compiler CLI")
    parser.add_argument("file", help="Path to the .kif file")
    parser.add_argument("--start-line", type=int, default=1, help="Start line number (1-based)")
    parser.add_argument("--end-line", type=int, help="End line number (1-based)")
    parser.add_argument("--find-symbol", help="Symbol to search for in the compiled AST")
    parser.add_argument("--show-original", action="store_true", help="Show original source line with translation")

    args = parser.parse_args()

    compiler = Compiler()
    try:
        result = compiler.compile_file(args.file, args.start_line, args.end_line)
        if args.find_symbol:
            usages = compiler.find_symbol_usages(args.find_symbol)
            print(f"Found {len(usages)} expressions containing symbol '{args.find_symbol}':")
            for node in usages:
                if args.show_original and node.source_text:
                    print(f"Original: {node.source_text.strip()}")
                print(f"Translated: {node}")
        else:
            for node in result:
                if args.show_original and node.source_text:
                    print(f"Original: {node.source_text.strip()}")
                print(f"Translated: {node}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()