import cProfile
import sys, os
from argparse import ArgumentParser, FileType
from boyer_moore import BoyerMooreSearch

GREEN = '\033[32m'
PRETTY_GREEN = '\033[92m'
END = '\033[0m'

class NaiveSearch:
    def __init__(self, pattern):
        self.pattern = pattern

    def search(self, string):
        """Find first occurence of pattern in string."""
        len_pat = len(self.pattern)
        len_str = len(string)
        i = 0
        while i < len_str:
            j = 0
            while j < len_pat and self.pattern[j] == string[i+j]:
                j += 1
            if j == len_pat:
                return i
            i += 1
        return -1


#        i = 0
#        while i < len(string):
#            j = 0
#            while j < len(self.pattern) and self.pattern[j] == string[i+j]:
#                j += 1
#            if j == len(self.pattern):
#                return i
#            i += 1
#        return -1

        #for i in xrange(len(string)):
        #    for j in xrange(len(self.pattern)):
        #        if string[i+j] != self.pattern[j]:
        #            break
        #        elif j == len(self.pattern) - 1:
        #            return i
        #return -1

       # len_pat = len(self.pattern)
       # len_str = len(string)
       # for i in xrange(len_str):
       #     for j in xrange(len_pat):
       #         if string[i+j] != self.pattern[j]:
       #             break
       #         elif j == len_pat - 1:
       #             return i
       # return -1

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
    return parser

def main():
    # set up argparse argument parser and get args
    parser = setup_parser()
    args = parser.parse_args()
    pattern = args.pattern

    # assign search object
    #searcher = NaiveSearch(pattern)
    # find = naive.search
    searcher = BoyerMooreSearch(pattern)

    # what to do with files and dirs
    files = [f if f!= '-' else '(standard input)' for f in args.files]
    grep_files(files, searcher, args.recursive, args.color)

if __name__ == '__main__':
    #main()
    cProfile.run('main()')
