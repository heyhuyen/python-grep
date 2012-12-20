
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


class BoyerMooreSearch:
    """Search using Boyer-Moore algorithm."""
    def __init__(self, pattern):
        self.pattern = pattern
        self.bad_chars = self.preprocess_bad()
        self.good_suffixes = self.preprocess_good()

    def preprocess_bad(self):
        """Calculate shifts for characters in pattern."""
        occ = {}
        for j in xrange(len(self.pattern)):
            char = self.pattern[j]
            occ[char] = j
        return occ

    def whole_suffix_shifts(self):
        """Calculate shifts for mismatched whole suffixes."""
        p = list(self.pattern)
        p.append('')    # add empty string to end
        empty_pos = len(self.pattern)   # aka length of pattern...

        suffix_i = empty_pos
        border_i = suffix_i + 1 # border index

        f = [0] * border_i
        s = [0] * border_i
        assert(len(f) == len(s) and len(s) == len(p))

        f[suffix_i] = border_i # suffix = last char, border = E (@ len(pat) + 1)

        while suffix_i > 0:
            while (border_i <= empty_pos and p[suffix_i - 1] != p[border_i - 1]):
                if s[border_i] == 0:
                    s[border_i] = border_i - suffix_i
                border_i = f[border_i]

            suffix_i -= 1
            border_i -= 1
            f[suffix_i] = border_i

        #return (f, s)
        j = f[0]
        for index, shift in enumerate(s):
            if shift == 0:
                s[index] = j
            if shift == j and j < len(f):
                j = f[j]
        return s

    def partial_suffix_shifts(self, f, s):
        """Calculate shifts for partially mismatched suffixes which occur at beginning of pattern."""
        j = f[0]
        for index, shift in enumerate(s):
            if shift == 0:
                s[index] = j
            if shift == j and j < len(f):
                j = f[j]
        return s

    def preprocess_good(self):
        """Calculate shifts for suffixes in pattern."""
        return self.whole_suffix_shifts()

    def max_shift(self, bad_char, suffix):
        # return max shift between bad_chars and good_suffixes 
        if bad_char in self.bad_chars:
            b = self.bad_chars[bad_char]
        else:
            b = -1
        s = self.good_suffixes[suffix]
        return max(suffix - b - 1, s)

    def search(self, string):
        """Boyer Moore search algorithm."""
        len_str = len(string)
        len_pat = len(self.pattern)
        i = 0
        while i <= len_str - len_pat:
            j = len_pat - 1 #last index of pattern
            while j >= 0 and self.pattern[j] == string[i+j]:
                j -= 1
            if j < 0:
                return i
            else:
                skip = self.max_shift(string[i+j], j+1)
                i += skip
                #s[j+1], j-occ(string[i+j])
        return -1

#        index = 0
#        len_pat = len(self.pattern)
#
#        while index <= len(string) - len_pat:
#            pindex = len_pat - 1
#            while pindex >= 0 and self.pattern[pindex] == string[index + pindex]:
#                pindex -= 1
#            if pindex < 0:
#                return index
#            else:
#                if string[index+pindex] in self.bad_chars:
#                    skip = self.bad_chars[string[index+pindex]]
#                else:
#                    skip = len_pat
#                index += skip
#        return -1

if __name__ == '__main__':
    pattern = 'abbabab'
    b = BoyerMooreSearch(pattern) 
    print b.bad_chars
    print b.good_suffixes
    print b.search('what is thatbabbababaabbabab?')
    print b.search('abbabab')
