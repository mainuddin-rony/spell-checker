def calculate_levenshtein_distance(s1, s2):
    """Return the Levenshtein edit distance between two strings s1 and s2"""
    if s1 == s2:
        return 0
    if len(s1) < len(s2):
        s1, s2 = s2, s1
    if not s1:
        return len(s2)
    previous_row = range(len(s2) + 1)
    for i, column1 in enumerate(s1):
        current_row = [i + 1]
        for j, column2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (column1 != column2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]


def calculate_damerau_levenshtein_distance(s1, s2):
    """Return the Damerau-Levenshtein edit distance between two strings s1 and s2"""
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition

    return d[lenstr1 - 1, lenstr2 - 1]


def identify_distance_type(candidate, word):
    """This function identify the distance type between candidate word and real word"""
    edit = [False] * 4
    correct = ""
    error = ""
    x = ''
    w = ''
    for i in range(min([len(word), len(candidate)]) - 1):
        if candidate[0:i + 1] != word[0:i + 1]:
            if candidate[i:] == word[i - 1:]:
                edit[1] = True
                correct = candidate[i - 1]
                error = ''
                x = candidate[i - 2]
                w = candidate[i - 2] + candidate[i - 1]
                break
            elif candidate[i:] == word[i + 1:]:

                correct = ''
                error = word[i]
                if i == 0:
                    w = '#'
                    x = '#' + error
                else:
                    w = word[i - 1]
                    x = word[i - 1] + error
                edit[0] = True
                break
            if candidate[i + 1:] == word[i + 1:]:
                edit[2] = True
                correct = candidate[i]
                error = word[i]
                x = error
                w = correct
                break
            if candidate[i] == word[i + 1] and candidate[i + 2:] == word[i + 2:]:
                edit[3] = True
                correct = candidate[i] + candidate[i + 1]
                error = word[i] + word[i + 1]
                x = error
                w = correct
                break
    candidate = candidate[::-1]
    word = word[::-1]
    for i in range(min([len(word), len(candidate)]) - 1):
        if candidate[0:i + 1] != word[0:i + 1]:
            if candidate[i:] == word[i - 1:]:
                edit[1] = True
                correct = candidate[i - 1]
                error = ''
                x = candidate[i - 2]
                w = candidate[i - 2] + candidate[i - 1]
                break
            elif candidate[i:] == word[i + 1:]:

                correct = ''
                error = word[i]
                if i == 0:
                    w = '#'
                    x = '#' + error
                else:
                    w = word[i - 1]
                    x = word[i - 1] + error
                edit[0] = True
                break
            if candidate[i + 1:] == word[i + 1:]:
                edit[2] = True
                correct = candidate[i]
                error = word[i]
                x = error
                w = correct
                break
            if candidate[i] == word[i + 1] and candidate[i + 2:] == word[i + 2:]:
                edit[3] = True
                correct = candidate[i] + candidate[i + 1]
                error = word[i] + word[i + 1]
                x = error
                w = correct
                break
    if word == candidate:
        return "None", '', '', '', ''
    if edit[1]:
        return "del", correct, error, x, w
    elif edit[0]:
        return "ins", correct, error, x, w
    elif edit[2]:
        return "sub", correct, error, x, w
    elif edit[3]:
        return "trans", correct, error, x, w


def other_dl_distance(s1,s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition

    return d[lenstr1 - 1, lenstr2 - 1]