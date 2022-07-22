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
#lines = [l for l in lines if not l == '\n' and not l =='']
print(lines)

for i in range(len(lines)):
    lines[i] = lines[i].replace('\n', '')
    items = lines[i].split()
    found = False
    opened = False
    lit_buffer = ""
    for item in items:
        found = False
        if item in RESERVED:
            lexemes['reserved'].append(tuple([item, i+1]))
            found = True
            continue
        if item in ACCUMULATORS:
            lexemes['operators'].append(tuple([item, i+1]))
            found = True
            continue
        if item in UN_OPERATORS:
            lexemes['operators'].append(tuple([item, i+1]))
            found = True
            continue
        if item in BIN_OPERATORS:
            lexemes['operators'].append(tuple([item, i+1]))
            found = True
            continue
        if item in PUNCTUATION:
            lexemes['punctuation'].append(tuple([item, i+1]))
            found = True
            continue
        if item in LIBRARIES or '.h' in item:
            lexemes['libs'].append(tuple([item, i+1]))
            found = True
            continue
        if re.match(r'^".*"$', item):
            # regex for starts and ends with double quotes
            lexemes['literal'].append(tuple([item.replace('"', ''), i+1]))
            found = True
            continue
        if re.match(r"^'.*'$", item):
            # regex for starts and ends with single quotes
            lexemes['literal'].append(tuple([item.replace("'", ''), i+1]))
            found = True
            continue
        if found:
            found = False
            break
        # LACK OF SPACES
        # the only way of lacking spaces and having keywords is if keywords are separated by punctuations
        idx = 0
        keys = re.split(r';|\(|\)|\{|}|\[|]|,|:|\.', item)
        for k in keys:
            found = False
            if k in RESERVED:
                lexemes['reserved'].append(tuple([k, i+1]))
                idx += len(k) + 1
                found = True
                continue
            if found:
                found = False
                break
        # in case you have an expression with no spaces
        if len(item) >= 1:

            found = False
            factor = 1
            buffer = ""
            while (True):
                if idx >= len(item):
                    break
                # for identifiers
                buffer = ""
                for c in item[idx:]:
                    if (buffer + c).isidentifier():
                        buffer += c
                    elif not c.isalnum():
                        break
                if buffer != "" and buffer not in RESERVED:
                    lexemes['identifiers'].append(tuple([buffer, i+1]))
                    idx += len(buffer)
                if idx >= len(item):
                    continue

                # for numeric constants
                v = 0
                if item[idx].isdigit():
                    v = v * 10 + int(item[idx])
                    idx += 1
                    decimal = False
                    counter = 0
                    while idx < len(item):
                        if item[idx] != '.' and not item[idx].isdigit():
                            break
                        if item[idx].isdigit() and not decimal:
                            peek = item[idx]
                            v = v * 10 + int(peek)
                            idx += 1
                        if item[idx].isdigit() and decimal:
                            counter += 1
                            peek = item[idx]
                            v = v + (int(peek) / (10 ** counter))
                            idx += 1
                        if item[idx] == '.':
                            decimal = True
                            idx += 1
                    lexemes['numeric'].append(tuple([v, i+1]))
                    if idx >= len(item):
                        continue
                # for string literals
                if item[idx] == '"' and not opened:
                    opened = True
                    # start from the second char
                    idx += 1
                    while idx < len(item):
                        if item[idx] == '"':
                            lexemes['literal'].append(tuple([lit_buffer, i+1]))
                            lit_buffer = ""
                            opened = False
                            break
                        else:
                            lit_buffer += item[idx]
                            if idx < (len(item) - 1):
                                idx += 1
                            else:
                                lit_buffer += " "
                                idx += 1
                                break
                if idx >= len(item):
                    continue
                if opened:
                    while idx < len(item):
                        if item[idx] == '"' and opened:
                            lexemes['literal'].append(tuple([lit_buffer, i+1]))
                            lit_buffer = ""
                            opened = False
                            break
                        else:
                            lit_buffer += item[idx]
                            if idx < (len(item) - 1):
                                idx += 1
                            else:
                                idx += 1
                                break
                if idx >= len(item):
                    continue

                found = False
                letter = item[idx]
                # for operators
                for o in BIN_OPERATORS:
                    # binary as last element
                    if letter == o and idx == (len(item) - 1):
                        lexemes['operators'].append(tuple([o, i+1]))
                        factor = 1
                        found = True
                        break
                    # binary in a longer string
                    if letter == o and item[idx + 1] != '=' and item[idx + 1] != letter:
                        lexemes['operators'].append(tuple([o, i+1]))
                        factor = 1
                        found = True
                        break
                    # accumulators
                    if letter == o and item[idx + 1] == '=':
                        lexemes['operators'].append(tuple([o+'=', i+1]))
                        factor = 2
                        found = True
                    # unary
                    if letter == o and item[idx + 1] == letter:
                        lexemes['operators'].append(tuple([o+o, i+1]))
                        factor = 2
                        found = True
                if found:
                    idx += factor
                    continue
                for o in PUNCTUATION:
                    if letter == o:
                        lexemes['punctuation'].append(tuple([o, i+1]))
                        factor = 1
                        found = True
                        break
                if found:
                    idx += factor
                    continue
                for o in LOGIC:
                    if letter == o and item[idx + 1] == '=':
                        lexemes['logic'].append(tuple([o+'=', i+1]))
                        factor = 2
                        found = True
                        break
                    if letter == o and item[idx + 1] != '=':
                        lexemes['logic'].append(tuple([o, i+1]))
                        factor = 1
                        found = True
                        break
                idx += factor
for k in lexemes.keys():
    text_file = open(k + ".txt", "w")
    s = ""
    for id, line in lexemes[k]:
        s += f"{line} {id}\n"
    text_file.write(s)
    text_file.close()
print(lexemes)
