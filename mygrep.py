import sys
import argparse
import pdb

GREEN = '\033[92m'
END = '\033[0m'

# plain vanilla version
# returns True first match
# False if not found
def plain_find(pattern, string, ignore):
    string_mod = string
    if ignore:
        pattern = pattern.lower()
        string_mod = string.lower()
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string_mod[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return string
    return ''

# plain vanilla version returning index
def index_find(pattern, string, ignore):
    string_mod = string
    if ignore:
        pattern = pattern.lower()
        string_mod = string.lower()
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string_mod[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return i
    return -1

# adds color
def color_find(pattern, string, ignore):
    result = ''
    index = index_find(pattern, string, ignore)
    if index == -1:
        return result
    while index != -1:
        result += string[:index]
        result += GREEN + string[index:index + len(pattern)] + END
        string = string[index + len(pattern):]
        index = index_find(pattern, string, ignore)
    result += string
    return result

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

    # read lines
    line = f.readline()
    line_n = 0
    while line:
        n_str = ''
        if args.line_number:
            line_n += 1
            n_str += '%d:' % line_n
        if args.color:
            result = color_find(pattern, line, args.ignore_case)
        else:
            result = plain_find(pattern, line, args.ignore_case)
        if len(result) > 0:
            print n_str + result.strip()
        line = f.readline()
    f.close()
