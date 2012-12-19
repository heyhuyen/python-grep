class BoyerMooreSearch:
    """Search using Boyer-Moore algorithm."""
    def __init__(self, pattern):
        self.pattern = pattern
        self.bad_chars = self.preprocess_bad()
        self.good_suffixes = self.preprocess_good()

    def occurrence(self, string, char):
        """Find right most occurrence of char in word. Returns -1 if not found."""
        #return word.rfind(char)
        indices = range(len(string))
        indices.reverse()
        for i in indices:
            if string[i] == char:
                return i
        return -1

    def bad_char_shift(self, bad_char):
        """Calculate distance to shift pattern for mismatched character."""
        return len(self.pattern) - 1 - self.occurrence(self.pattern[:-1], bad_char)

    def preprocess_bad(self):
        """Calculate shifts for characters in pattern."""
        chars = set(list(self.pattern))
        return {char: self.bad_char_shift(char) for char in chars}

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

        return (f,s)

    def partial_suffix_shifts(self):
        """Calculate shifts for partially mismatched suffixes which occur at beginning of pattern."""
        pass

    def preprocess_good(self):
        """Calculate shifts for suffixes in pattern."""
        return self.whole_suffix_shifts()
        # partial_suffix_shifts()

    def search(self, string):
        """Boyer Moore search algorithm."""
        index = len(self.pattern) - 1
        pindices = range(len(self.pattern))
        pindices.reverse()

        while index < len(string) - 1:
            sindices = range(index - len(self.pattern) + 1, index + 1)
            for pindex in pindices:
                str_char = string[sindices[pindex]]
                if str_char != self.pattern[pindex]:
                    # non match
                    if str_char in self.bad_chars:
                        index += self.bad_chars[string[sindices[pindex]]]
                    else:
                        index += len(self.pattern)
                    break
                elif pindex == 0:
                    return index - len(self.pattern) + 1
        return -1

if __name__ == '__main__':
    pattern = 'abbabab'
    b = BoyerMooreSearch(pattern) 
    print b.bad_chars
    print b.good_suffixes
