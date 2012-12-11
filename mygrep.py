import sys
import argparse
import pdb

GREEN = '\033[92m'
END = '\033[0m'

# plain vanilla version
# returns index of first match
# -1 if not found
def plainfind(pattern, string):
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return i
    return -1

# adds color
def colorfind(pattern, string):
    result = ''
    index = plainfind(pattern, string)
    if index == -1:
        return result
    while index != -1:
        result += string[:index]
        result += GREEN + pattern + END
        string = string[index + len(pattern):]
        index = plainfind(pattern, string)
    result += string
    return result

if __name__ == '__main__':
    # set up argparse argument parser
    parser = argparse.ArgumentParser(description="Find occurrences of a pattern in a text.")
    parser.add_argument('pattern', type=str, help="the pattern to find")
    parser.add_argument('text', type=argparse.FileType('r'), nargs="?", default=sys.stdin, help="the text to search")
    parser.add_argument('--color', action='store_true', help="highlight pattern in output")

    # unpack args
    args = parser.parse_args()
    pattern = args.pattern
    f = args.text

    # read lines
    line = f.readline()
    while line:
        if args.color:
            result = colorfind(pattern, line)
            if len(result) > 0:
                print result.strip()
        else:
            result = plainfind(pattern, line)
            if result != -1:
                print line.strip()
        line = f.readline()
    f.close()
