import tokenize
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python show_tokens.py <filename>")
        return

    filename = sys.argv[1]
    with open(filename, 'rb') as f:
        tokens = list(tokenize.tokenize(f.readline))
        for token in tokens:
            print(f"{token.type} {tokenize.tok_name[token.type]} {token.string!r} {token.start} {token.end} {token.line.strip()}")

if __name__ == "__main__":
    main()
