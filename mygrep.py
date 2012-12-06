import sys

def myfind(pattern, string):
    for i in range(len(string)):
        for j in range(len(pattern)):
            if string[i+j] != pattern[j]:
                break
            elif j == len(pattern) - 1:
                return True
    return False

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
        if myfind(pattern, line):
            print line.strip()

