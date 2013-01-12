This is a python implementation of the Unix [grep](http://pubs.opengroup.org/onlinepubs/9699919799/utilities/grep.html) command.

Written during [Hacker School](https://www.hackerschool.com/), Batch[4], Fall 2012.

## Usage
    python mygrep.py [--help] [--color] [-h] [-i] [-l] [-n] [-R]
                 pattern [FILES [FILES ...]]

    Find matches of a pattern in lines of file(s).

    positional arguments:
    pattern               the pattern to find
    FILES                 the files(s) to search

    optional arguments:
    --help                     show this help message and exit
    --color, --colour          highlight matches
    -h, --no-filename          print without filename headers
    -i, --ignore-case          case-insensitive search
    -l, --files-with-matches   print only filenames with matches
    -n, --line-number          print line numbers, indexed from 1
    -R, -r, --recursive        recursively search directories

If called with no file arguments, reads from standard input and follows grep's behavior when reading from standard input. Can also be used with pipes.

## Boyer-Moore Algorithm
As an exercise in optimazation, I looked into string searching algorithms to make mygrep faster. I decided to go with Boyer-Moore because that's what GNU's grep is based on. I worked on a separate mini-version of mygrep for testing:

    python search_test.py [--help] [--color] [-R] [-b] pattern [FILES [FILES ...]]

    Find occurrences of a pattern in lines of file(s).

    positional arguments:
    pattern              the pattern to find
    FILES                the files(s) to search

    optional arguments:
    --help               show this help message and exit
    --color, --colour    highlight pattern in output
    -R, -r, --recursive  recursively search directories
    -b, --boyer-moore    search with boyer-moore algorithm

### Test
Using naive search `python search_test.py King bible.txt`:

    real    0m2.173s
    user    0m2.144s
    sys 0m0.024s

Using Boyer_Moore search `python search_test.py King bible.txt -b`, you can see it's a little faster:

    real    0m1.732s
    user    0m1.705s
    sys 0m0.023s

But not nearly as fast as regular grep `grep King bible.txt`:

    real    0m0.200s
    user    0m0.196s
    sys 0m0.004s

## Resources
- [BSD grep man page](http://www.openbsd.org/cgi-bin/man.cgi?query=grep)
- [Why GNU grep is fast](http://lists.freebsd.org/pipermail/freebsd-current/2010-August/019310.html)
- Boyer-Moore string search algorithm [explanation](http://www.inf.fh-flensburg.de/lang/algorithmen/pattern/bmen.htm)
- [visualizer](http://www.utdallas.edu/~besp/demo/John2010/boyer-moore.htm) for Boyer Moore's bad char heuristic
- python [argparse](http://docs.python.org/2/library/argparse.html) module

##Todo/Extension Ideas
- use boyer-moore in mygrep.py
- figure out if output can handle colors, when piping or writing results to a file.
