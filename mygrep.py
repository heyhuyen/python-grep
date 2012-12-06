import sys
import argparse

GREEN = '\033[92m'
END = '\033[0m'

def myfind(pattern, string, color):
    count = 0
    result = ''
    index = 0
    while index < len(string):
        for j in range(len(pattern)):
            if string[index+j] != pattern[j]:
                result += string[index]
                break
            elif j == len(pattern) - 1:
               if not color:
                   return string
               else:
                   count += 1
                   result += GREEN + pattern + END
                   index += j
        index += 1
    if count == 0:
        result = ''
    return result

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
        result = myfind(pattern, line, args.color)
        if len(result) > 0:
            print result.strip()
