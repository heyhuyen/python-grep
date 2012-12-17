import cProfile
import sys, os
from argparse import ArgumentParser, FileType
from boyer_moore import bm_find, preprocess

GREEN = '\033[32m'
PRETTY_GREEN = '\033[92m'
END = '\033[0m'

def index_find(pattern, string, shifts):
    """Find first occurence of pattern in string."""
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return i
    return -1

def color_find(pattern, string, find, shifts):
    """Find and color all occurences of pattern in string."""
    result = ''
    index = find(pattern, string, shifts)

    while index != -1:
        result += string[:index]
        result += PRETTY_GREEN + string[index:index + len(pattern)] + END
        string = string[index + len(pattern):]
        index = find(pattern, string, shifts)

    return result if result == '' else result + string

def grep_file(filename, pattern, find, color, shifts):
    text = sys.stdin if filename == '(standard input)' else open(filename, 'r')
    line = text.readline()
    while line:
        if color:
            result = color_find(pattern, line, find, shifts)
        else:
            index = find(pattern, line, shifts)
            result = line if index != -1 else ''

        # print to stdout and read next line
        if len(result) > 0:
            sys.stdout.write('%s:%s' % (filename, result))
        line = text.readline()

    text.close()

def grep_files(paths, pattern, find, recurse, color, shifts):
    for path in paths:
        if os.path.isfile(path) or path == '(standard input)':
            grep_file(path, pattern, find, color, shifts)
        else:
            if recurse:
                more_paths = [path + '/' + child for child in os.listdir(path)]
                grep_files(more_paths, pattern, find, recurse, color, shifts)
            else:
                sys.stdout.write('grep: %s: Is a directory\n' % path)

def setup_parser():
    parser = ArgumentParser(description='Find occurrences of a pattern in lines of file(s).', add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('pattern', type=str, help='the pattern to find')
    parser.add_argument('files', metavar='FILES', nargs='*', default=['-'], help='the files(s) to search')
    parser.add_argument('--color', '--colour', action='store_true', help='highlight pattern in output')
    parser.add_argument('-R', '-r', '--recursive', action='store_true', help='recursively search directories')
    return parser

def main():
    # set up argparse argument parser and get args
    parser = setup_parser()
    args = parser.parse_args()
    pattern = args.pattern

    # assign find fn
    #find = index_find
    #shifts = None
    shifts = preprocess(pattern)
    find = bm_find

    # what to do with files and dirs
    files = [f if f!= '-' else '(standard input)' for f in args.files]
    grep_files(files, pattern, find, args.recursive, args.color, shifts)

if __name__ == '__main__':
    #main()
    cProfile.run('main()')
