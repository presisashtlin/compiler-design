from collections import defaultdict

grammar = defaultdict(list)
first = defaultdict(set)
follow = defaultdict(set)
table = defaultdict(dict)

# ----------- INPUT -------------

n = int(input("Enter number of productions: "))
print("Enter productions (Example: E->TR|a)")

for _ in range(n):
    prod = input()
    left, right = prod.split("->")
    grammar[left].extend(right.split("|"))

start_symbol = list(grammar.keys())[0]

# ----------- FIRST -------------

def compute_first(symbol):
    if not symbol.isupper():
        return {symbol}

    if first[symbol]:
        return first[symbol]

    for production in grammar[symbol]:
        if production == "ε":
            first[symbol].add("ε")
        else:
            for char in production:
                char_first = compute_first(char)
                first[symbol].update(char_first - {"ε"})
                if "ε" not in char_first:
                    break
            else:
                first[symbol].add("ε")

    return first[symbol]

for non_terminal in grammar:
    compute_first(non_terminal)

# ----------- FOLLOW -------------

follow[start_symbol].add("$")

def compute_follow():
    changed = True
    while changed:
        changed = False
        for head in grammar:
            for production in grammar[head]:
                for i in range(len(production)):
                    symbol = production[i]
                    if symbol.isupper():
                        next_part = production[i+1:]

                        if next_part:
                            temp_first = set()
                            for char in next_part:
                                char_first = compute_first(char)
                                temp_first.update(char_first - {"ε"})
                                if "ε" not in char_first:
                                    break
                            else:
                                temp_first.add("ε")

                            before = len(follow[symbol])
                            follow[symbol].update(temp_first - {"ε"})
                            if "ε" in temp_first:
                                follow[symbol].update(follow[head])

                            if len(follow[symbol]) > before:
                                changed = True
                        else:
                            before = len(follow[symbol])
                            follow[symbol].update(follow[head])
                            if len(follow[symbol]) > before:
                                changed = True

compute_follow()

# ----------- PARSING TABLE -------------

for head in grammar:
    for production in grammar[head]:
        if production == "ε":
            for f in follow[head]:
                table[head][f] = production
        else:
            first_set = set()
            for char in production:
                char_first = compute_first(char)
                first_set.update(char_first - {"ε"})
                if "ε" not in char_first:
                    break
            else:
                first_set.add("ε")

            for terminal in first_set - {"ε"}:
                table[head][terminal] = production

            if "ε" in first_set:
                for f in follow[head]:
                    table[head][f] = production

# ----------- OUTPUT -------------

print("\nFIRST Sets:")
for nt in grammar:
    print(f"FIRST({nt}) = {first[nt]}")

print("\nFOLLOW Sets:")
for nt in grammar:
    print(f"FOLLOW({nt}) = {follow[nt]}")

print("\nPredictive Parsing Table:")
for nt in table:
    for terminal in table[nt]:
        print(f"M[{nt}, {terminal}] = {nt}->{table[nt][terminal]}")
