import argparse
import sys
from .core import Compiler

def main():
    parser = argparse.ArgumentParser(description="SUO-KIF Compiler CLI")
    parser.add_argument("file", help="Path to the .kif file")
    parser.add_argument("--start-line", type=int, default=1, help="Start line number (1-based)")
    parser.add_argument("--end-line", type=int, help="End line number (1-based)")

    args = parser.parse_args()

    compiler = Compiler()
    try:
        result = compiler.compile_file(args.file, args.start_line, args.end_line)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()