def occ(word, char):
    if char not in word:
        return -1

    return word.rfind(char)

def shift(word, char):
    return len(word) - 1 - occ(word[:-1], char)

def preprocess(pattern):
    bad = set(list(pattern))
    return {ch: shift(pattern, ch) for ch in bad}

def bm_find(pattern, string, shifts):
    index = len(pattern) - 1
    pindices = range(len(pattern))
    pindices.reverse()

    while index < len(string) - 1:
        sindices = range(index - len(pattern) + 1, index + 1)
        for pindex in pindices:
            str_char = string[sindices[pindex]]
            if str_char != pattern[pindex]:
                # non match
                if str_char in shifts:
                    index += shifts[string[sindices[pindex]]]
                else:
                    index += len(pattern)
                break
            elif pindex == 0:
                return index - len(pattern) + 1
    return -1
