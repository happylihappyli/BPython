import tokenize
import sys

def dump_tokens(filename):
    with open(filename, 'rb') as f:
        tokens = list(tokenize.tokenize(f.readline))
        for token in tokens:
            print(token)

if __name__ == "__main__":
    dump_tokens(sys.argv[1])
