import sys, os
from argparse import ArgumentParser, FileType
import pdb

GREEN = '\033[32m'
PRETTY_GREEN = '\033[92m'
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
        result += PRETTY_GREEN + string[index:index + len(pattern)] + END
        string = string[index + len(pattern):]
        index = find(pattern, string)

    return result if result == '' else result + string

def print_result(result, no_header, header, lineno):
    """Print found result to standard output."""
    if not no_header:
        sys.stdout.write('%s:' % (header if header != '<stdin>' else '(standard input)'))
    if lineno:
        sys.stdout.write('%d:' % lineno)
    sys.stdout.write(result)

def search_lines(text, find, line_number, color, no_filename):
    line = text.readline()
    lineno = 0 # counter for line number option
    # read lines of a text
    while line:
        if line_number: # ugly lineno chunk
            lineno += 1

        if color:
            result = color_find(pattern, line, find)
        else:
            index = find(pattern, line)
            result = line if index != -1 else ''

        # print to stdout and read next line
        if len(result) > 0:
            print_result(result, no_filename, text.name, lineno)
        line = text.readline()

    text.close()

def pathname(path):
    if os.path.isfile(path):
        return path
    else:
        return 'mygrep: %s: Is a directory\n' % path

def setup_parser():
    parser = ArgumentParser(description='Find occurrences of a pattern in lines of file(s).', add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('pattern', type=str, help='the pattern to find')
    parser.add_argument('files', metavar='FILES', type=pathname, nargs='*', default=[sys.stdin], help='the files(s) to search')
    parser.add_argument('--color', '--colour', action='store_true', help='highlight pattern in output')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='ignore case in search')
    parser.add_argument('-n', '--line-number', action='store_true', help='print line numbers, indexed beginning at 1')
    parser.add_argument('-h', '--no-filename', action='store_true', help='print output without filename headers')
    return parser


if __name__ == '__main__':
    # set up argparse argument parser and get args
    parser = setup_parser()
    args = parser.parse_args()
    pattern = args.pattern
    paths = args.files

    # adjust no_filename
    if not args.no_filename:
        if len(paths) == 1:
            args.no_filename = True

    # assign find fn
    find = index_find
    if args.ignore_case:
        find = ignore_find

    # loop over files
    for path in paths:
        if 'mygrep:' not in path:
            search_lines(open(path, 'r'), find, args.line_number, args.color, args.no_filename)
        else:
            sys.stdout.write(path)
