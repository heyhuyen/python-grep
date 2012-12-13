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
        sys.stdout.write('%s:' % header)
    if lineno:
        sys.stdout.write('%d:' % lineno)
    sys.stdout.write(result)

def grep_file(filename, pattern, find, only_names, line_number, color, no_filename):
    text = sys.stdin if filename == '(standard input)' else open(filename, 'r')
    line = text.readline()
    lineno = 0 # counter for lineno option
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
            if only_names:
                sys.stdout.write('%s\n' % filename)
                break
            else:
                print_result(result, no_filename, filename, lineno)
        line = text.readline()

    text.close()

def grep_files(paths, pattern, find, recurse, only_names, lineno, color, no_filename):
    for path in paths:
        if os.path.isfile(path) or path == '(standard input)':
            grep_file(path, pattern, find, only_names, lineno, color, no_filename)
        else:
            if recurse:
                more_paths = [path + '/' + child for child in os.listdir(path)]
                grep_files(more_paths, pattern, find, recurse, only_names, lineno, color, no_filename)
            else:
                sys.stdout.write('grep: %s: Is a directory\n' % path)

def setup_parser():
    parser = ArgumentParser(description='Find occurrences of a pattern in lines of file(s).', add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('pattern', type=str, help='the pattern to find')
    parser.add_argument('files', metavar='FILES', nargs='*', default=['-'], help='the files(s) to search')
    parser.add_argument('--color', '--colour', action='store_true', help='highlight pattern in output')
    parser.add_argument('-h', '--no-filename', action='store_true', help='print output without filename headers')
    parser.add_argument('-i', '--ignore-case', action='store_true', help='ignore case in search')
    parser.add_argument('-l', '--files-with-matches', action='store_true', help='only output the names of files containing the pattern.')
    parser.add_argument('-n', '--line-number', action='store_true', help='print line numbers, indexed beginning at 1')
    parser.add_argument('-R', '-r', '--recursive', action='store_true', help='recursively search directories')
    return parser

def main():
    # set up argparse argument parser and get args
    parser = setup_parser()
    args = parser.parse_args()
    pattern = args.pattern

    # adjust no_filename
    if not args.no_filename:
        if args.recursive:
            args.no_filename = False
        elif len(args.files) == 1:
            args.no_filename = True

    # assign find fn
    find = index_find
    if args.ignore_case:
        find = ignore_find

    # what to do with files and dirs
    files = [f if f!= '-' else '(standard input)' for f in args.files]
    grep_files(files, pattern, find, args.recursive, args.files_with_matches, args.line_number, args.color, args.no_filename)

if __name__ == '__main__':
    main()
