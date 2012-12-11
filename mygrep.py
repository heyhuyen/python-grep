import sys
import argparse
import pdb

GREEN = '\033[92m'
END = '\033[0m'

def index_find(pattern, string):
    """Find first occurence of pattern in string."""
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return i
    return -1

def ignore_find(pattern, string):
    """Ignore case."""
    return index_find(pattern.lower(), string.lower())

def color_find(pattern, string, find):
    """Find and color all occurences of pattern in string."""
    result = ''
    index = find(pattern, string)

    while index != -1:
        result += string[:index]
        result += GREEN + string[index:index + len(pattern)] + END
        string = string[index + len(pattern):]
        index = find(pattern, string)

    return result if result == '' else result + string

if __name__ == '__main__':
    # set up argparse argument parser
    parser = argparse.ArgumentParser(description="Find occurrences of a pattern in a text.")
    parser.add_argument('pattern', type=str, help="the pattern to find")
    parser.add_argument('text', type=argparse.FileType('r'), nargs="?", default=sys.stdin, help="the text to search")
    parser.add_argument('--color', action='store_true', help="highlight pattern in output")
    parser.add_argument('--ignore-case', action='store_true', help='ignore case in serach')
    parser.add_argument('--line-number', action='store_true', help='print line numbers, beginning at 1')

    # unpack args
    args = parser.parse_args()
    pattern = args.pattern
    f = args.text

    # assign find fn
    find = index_find
    if args.ignore_case:
        find = ignore_find

    # read lines
    line = f.readline()
    line_n = 0 # counter for line number option
    while line:
        # ugly line number chunk
        n_str = ''
        if args.line_number:
            line_n += 1
            n_str += '%d:' % line_n

        if args.color:
            result = color_find(pattern, line, find)
        else:
            index = find(pattern, line)
            result = line if index != -1 else ''

        # print to stdout and read next line
        if len(result) > 0:
            print n_str + result.strip()
        line = f.readline()

    f.close()
