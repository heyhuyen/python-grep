import sys
import argparse

def myfind(pattern, string):
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find occurrences of a pattern in a file.")
    parser.add_argument('pattern', metavar="PATTERN", type=str, help="the pattern to find")
    parser.add_argument('filename', metavar="FILENAME", type=argparse.FileType('r'), help="the file to search")
    args = parser.parse_args()
    pattern = args.pattern
    f = args.filename
    lines = f.readlines()
    for line in lines:
        if myfind(pattern, line):
            print line.strip()

