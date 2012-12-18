import sys, os
from argparse import ArgumentParser, FileType

GREEN = '\033[32m'
PRETTY_GREEN = '\033[92m'
END_COLOR = '\033[0m'

def index_find(pattern, string):
    """Find index of pattern match in string. Returns -1 if not found."""
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return i
    return -1

def ignore_case_find(pattern, string):
    """Look for pattern in string, ignoring case."""
    return index_find(pattern.lower(), string.lower())

def find(pattern, string, ignore_case):
    """Find the pattern in the string. Return -1 if not found."""
    if ignore_case:
        return ignore_case_find(pattern, string)
    else:
        return index_find(pattern, string)

def color_find(pattern, string, ignore_case):
    """Find all matches of pattern in string. Returns colored string, or empty string if not found."""
    result = ''
    index = find(pattern, string, ignore_case)

    while index != -1:
        result += string[:index]
#------------------------------------------------------------------------------
        result += PRETTY_GREEN + string[index:index + len(pattern)] + END_COLOR
        string = string[index + len(pattern):]
        index = find(pattern, string, ignore_case)

    return result if result == '' else result + string

def get_match(pattern, string, color, ignore_case):
    """Find the pattern in the string. Returns the match result or the empty string if not found."""
    if color:
        return color_find(pattern, string, ignore_case)
    else:
        index = find(pattern, string, ignore_case)
        return string if index != -1 else ''

def print_result(print_header, header, print_lineno, lineno, print_line, line):
    """Print result to standard output."""
    result = ''
    if print_header:
        result += '%s' % header
    if print_lineno:
        if len(result) > 0:
            result += ':'
        result += '%d' % lineno
    if print_line:
        if len(result) > 0:
            result += ':'
        result += line
    sys.stdout.write('%s\n' % result.strip('\n'))

def grep_file(filename, pattern, color, ignore_case, print_headers,
                print_lineno, print_lines):
    """Search a single file or standard input."""
    text = sys.stdin if filename == '(standard input)' else open(filename, 'r')

    line = text.readline()
    lineno = 1
    while line:
        result = get_match(pattern, line, color, ignore_case)
        if len(result) > 0:
            print_result(print_headers, filename, print_lineno, lineno,
                            print_lines, result)
            if print_headers and not print_lines: # files-with-matches option
                break
        line = text.readline()
        lineno += 1

    text.close()

def grep_files(paths, pattern, recurse, color, ignore_case, print_headers,
                print_lineno, print_line):
    """Search files and directories."""
    for path in paths:
        if os.path.isfile(path) or path == '(standard input)':
            grep_file(path, pattern, color, ignore_case, print_headers,
                        print_lineno, print_line)
        else:
            if recurse:
                more_paths = [path + '/' + child for child in os.listdir(path)]
                grep_files(more_paths, pattern, recurse, color, ignore_case,
                            print_headers, print_lineno, print_line)
            else:
                sys.stdout.write('grep: %s: Is a directory\n' % path)

def setup_parser():
    """Configure command line argument parser object."""
    parser = ArgumentParser(description='Find matches of a pattern in ' \
                            'lines of file(s).', add_help=False)
    parser.add_argument('--help', action='help', help='show this help ' \
                        'message and exit')
    parser.add_argument('pattern', type=str, help='the pattern to find')
    parser.add_argument('files', metavar='FILES', nargs='*', default=['-'],
                        help='the files(s) to search')
    parser.add_argument('--color', '--colour', action='store_true',
                        help='highlight matches')
    parser.add_argument('-h', '--no-filename', action='store_true',
                        help='print without filename headers')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help='case-insensitive search')
    parser.add_argument('-l', '--files-with-matches', action='store_true',
                        help='print only filenames with matches')
    parser.add_argument('-n', '--line-number', action='store_true',
                        help='print line numbers, indexed from 1')
    parser.add_argument('-R', '-r', '--recursive', action='store_true',
                        help='recursively search directories')
    return parser

DEFAULT_PRINT_OPTIONS = (False, False, True)

def main():
    parser = setup_parser()
    args = parser.parse_args()
    pattern = args.pattern
    files = [f if f!= '-' else '(standard input)' for f in args.files]

    print_headers, print_lineno, print_lines = DEFAULT_PRINT_OPTIONS
    if args.files_with_matches:
        print_headers = True
        print_lines = False
    else:
        if args.recursive or len(files) > 1:
            print_headers = True
        if args.line_number:
            print_lineno = True
        if args.no_filename:
            print_headers = False

    grep_files(files, pattern, args.recursive, args.color, args.ignore_case,
                print_headers, print_lineno, print_lines)

if __name__ == '__main__':
    main()
