import sys

if __name__ == '__main__':
    if len(sys.argv) == 3:
        pattern, filename = sys.argv[1:]
        print "Pattern: %s Filename: %s" % (pattern, filename)
    else:
        print "Usage: mygrep.py <pattern> <filename>"
        sys.exit()

    f = open(filename)
    lines = f.readlines()
    for line in lines:
        if line.find(pattern) != -1:
            print line.strip()

