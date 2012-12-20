import cProfile
import sys, os
from argparse import ArgumentParser, FileType
from boyer_moore import BoyerMooreSearch, NaiveSearch

GREEN = '\033[32m'
PRETTY_GREEN = '\033[92m'
END = '\033[0m'

def color_find(string, searcher):
    """Find and color all occurences of pattern in string."""
    result = ''
    index = searcher.search(string)

    while index != -1:
        result += string[:index]
        result += PRETTY_GREEN + string[index:index + len(searcher.pattern)] + END
        string = string[index + len(searcher.pattern):]
        index = searcher.search(string)

    return result if result == '' else result + string

def grep_file(filename, searcher, color):
    text = sys.stdin if filename == '(standard input)' else open(filename, 'r')
    line = text.readline()
    while line:
        if color:
            result = color_find(line, searcher)
        else:
            index = searcher.search(line)
            result = line if index != -1 else ''

        # print to stdout and read next line
        if len(result) > 0:
            sys.stdout.write('%s' % (result))
        line = text.readline()

    text.close()

def grep_files(paths, searcher, recurse, color):
    for path in paths:
        if os.path.isfile(path) or path == '(standard input)':
            grep_file(path, searcher, color)
        else:
            if recurse:
                more_paths = [path + '/' + child for child in os.listdir(path)]
                grep_files(more_paths, searcher, recurse, color)
            else:
                sys.stdout.write('grep: %s: Is a directory\n' % path)

def setup_parser():
    parser = ArgumentParser(description='Find occurrences of a pattern in lines of file(s).', add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('pattern', type=str, help='the pattern to find')
    parser.add_argument('files', metavar='FILES', nargs='*', default=['-'], help='the files(s) to search')
    parser.add_argument('--color', '--colour', action='store_true', help='highlight pattern in output')
    parser.add_argument('-R', '-r', '--recursive', action='store_true', help='recursively search directories')
    parser.add_argument('-b', '--boyer-moore', action='store_true', help='search with boyer-moore algorithm')
    return parser

def main():
    # set up argparse argument parser and get args
    parser = setup_parser()
    args = parser.parse_args()
    pattern = args.pattern

    if args.boyer_moore:
        searcher = BoyerMooreSearch(pattern)
    else:
        searcher = NaiveSearch(pattern)

    # what to do with files and dirs
    files = [f if f!= '-' else '(standard input)' for f in args.files]
    grep_files(files, searcher, args.recursive, args.color)

if __name__ == '__main__':
    main()
    #cProfile.run('main()')
