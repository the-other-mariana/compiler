from terminals import TYPES, RESERVED, ACCUMULATORS, UN_OPERATORS, LOGIC, BIN_OPERATORS,  PUNCTUATION, LIBS
import re

LIBRARIES = []
for lib in LIBS:
    LIBRARIES.append("<" + lib + ">")
    LIBRARIES.append('"' + lib + '"')
# dict for all found lexemes
lexemes = {t: [] for t in TYPES}

# read input
f = open('input/main.cpp', 'r')
lines = f.readlines()

# delete empty lines
lines = [l.strip() for l in lines]
lines = [l for l in lines if not l == '\n' and not l =='']
print(lines)

for i in range(len(lines)):
    lines[i] = lines[i].replace('\n', '')
    items = lines[i].split()
    found = False
    for item in items:
        found = False
        if item in RESERVED:
            lexemes['reserved'].append(tuple([item, i]))
            found = True
            continue
        if item in ACCUMULATORS:
            lexemes['operators'].append(tuple([item, i]))
            found = True
            continue
        if item in UN_OPERATORS:
            lexemes['operators'].append(tuple([item, i]))
            found = True
            continue
        if item in BIN_OPERATORS:
            lexemes['operators'].append(tuple([item, i]))
            found = True
            continue
        if item in PUNCTUATION:
            lexemes['punctuation'].append(tuple([item, i]))
            found = True
            continue
        if item in LIBRARIES or '.h' in item:
            lexemes['libs'].append(tuple([item, i]))
            found = True
            continue
        if found:
            found = False
            break
        # LACK OF SPACES
        # the only way of lacking spaces and having keywords is if keywords are separated by punctuations
        keys = re.split(r';|\(|\)|\{|}|\[|]|,|:|\.', item)
        print(keys)
        for k in keys:
            found = False
            if k in RESERVED:
                lexemes['reserved'].append(tuple([k, i]))
                found = True
                continue
            if found:
                found = False
                break
        # in case you have operators with no spaces
        if len(item) > 2:
            idx = 0
            found = False
            factor = 1
            buffer = ""
            while (True):
                if idx >= len(item):
                    break

                # for identifiers
                if idx == 0:
                    # if identifier is spaced
                    if item[idx].isalpha() and item.isalnum():
                        lexemes['identifiers'].append(tuple([item, idx]))
                        break
                    else:
                        # if identifier is mixed with operators
                        buffer = ""
                        for c in item:
                            if c.isalnum() and item[0].isalpha():
                                buffer += c
                            elif not c.isalnum():
                                break
                        lexemes['identifiers'].append(tuple([buffer, idx]))
                        idx += len(buffer)

                found = False
                letter = item[idx]

                # for operators
                for o in BIN_OPERATORS:
                    # binary
                    if letter == o and item[idx + 1] != '=' and item[idx + 1] != letter:
                        lexemes['operators'].append(tuple([o, idx]))
                        factor = 1
                        found = True
                        break
                    # accumulators
                    if letter == o and item[idx + 1] == '=':
                        lexemes['operators'].append(tuple([o+'=', idx]))
                        factor = 2
                        found = True
                    # unary
                    if letter == o and item[idx + 1] == letter:
                        lexemes['operators'].append(tuple([o+o, idx]))
                        factor = 2
                        found = True
                if found:
                    idx += factor
                    continue
                for o in PUNCTUATION:
                    if letter == o:
                        lexemes['punctuation'].append(tuple([o, idx]))
                        factor = 1
                        found = True
                        break
                if found:
                    idx += factor
                    continue
                for o in LOGIC:
                    if letter == o and item[idx + 1] == '=':
                        lexemes['logic'].append(tuple([o+'=', idx]))
                        factor = 2
                        found = True
                        break
                    if letter == o and item[idx + 1] != '=':
                        lexemes['logic'].append(tuple([o, idx]))
                        factor = 1
                        found = True
                        break
                idx += factor

    print(i, lines[i].split())
print(lexemes)
