import sys
import argparse

def myfind(pattern, string, color):
    count = 0
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
               if not color:
                   return 1
               else:
                   count += 1
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find occurrences of a pattern in a file.")
    parser.add_argument('pattern', metavar="PATTERN", type=str, help="the pattern to find")
    parser.add_argument('filename', metavar="FILENAME", type=argparse.FileType('r'), help="the file to search")
    parser.add_argument('--color', metavar="BOOL", type=bool, nargs="?", const=True, help="highlight pattern in output")
    args = parser.parse_args()
    pattern = args.pattern
    f = args.filename
    lines = f.readlines()
    for line in lines:
        if myfind(pattern, line, args.color):
            print line.strip()

