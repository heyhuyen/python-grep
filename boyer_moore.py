def occ(word, char):
    if char not in word:
        return -1

    return word.rfind(char)

def shift(word, char):
    return len(word) - 1 - occ(word[:-1], char)

def preprocess(pattern, string):
    bad = set(list(string))
    return {ch: shift(pattern, ch) for ch in bad}

def bm_find(pattern, string):
    shift_dict = preprocess(pattern, string)
    index = len(pattern) - 1
    pindices = range(len(pattern))
    pindices.reverse()

    while index < len(string) - 1:
        sindices = range(index - len(pattern) + 1, index + 1)
        for pindex in pindices:
            if string[sindices[pindex]] != pattern[pindex]:
                # non match
                index += shift_dict[string[sindices[pindex]]]
                break
            elif pindex == 0:
                return index - len(pattern) + 1
    return -1
