import sys
import fileinput
from argparse import ArgumentParser, FileType
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

def print_result(result, textname, lineno):
    if len(texts) > 1:  # replace this check, texts not in local scope
        if textname == '<stdin>':
            textname = '(standard input)'
        sys.stdout.write('%s:' % textname)
    if lineno > 0:
        sys.stdout.write('%d:' % lineno)
    sys.stdout.write(result)

if __name__ == '__main__':
    # set up argparse argument parser
    parser = ArgumentParser(description="Find occurrences of a pattern in lines of text(s).")
    parser.add_argument('pattern', type=str, help="The pattern to find.")
    parser.add_argument('files', metavar="FILES", type=FileType('r'), nargs="*", help="the files(s) to search")
    parser.add_argument('--color', action='store_true', help="Highlight pattern in output.")
    parser.add_argument('--ignore-case', action='store_true', help='Ignore case in serach.')
    parser.add_argument('--line-number', action='store_true', help='Print line numbers. Indexed beginning at 1.')

    # unpack args
    args = parser.parse_args()
    pattern = args.pattern
    texts = args.files

    # assign find fn
    find = index_find
    if args.ignore_case:
        find = ignore_find

    # loop over files
    for text in texts:
        # read lines of a text
        line = text.readline()
        lineno = 0 # counter for line number option
        while line:
            # ugly line number chunk
            if args.line_number:
                lineno += 1

            if args.color:
                result = color_find(pattern, line, find)
            else:
                index = find(pattern, line)
                result = line if index != -1 else ''

            # print to stdout and read next line
            if len(result) > 0:
                print_result(result, text.name, lineno)
            line = text.readline()

        text.close()
