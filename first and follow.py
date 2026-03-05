from collections import defaultdict

# Store grammar
grammar = defaultdict(list)
first = defaultdict(set)
follow = defaultdict(set)

# ---------------- INPUT ----------------

n = int(input("Enter number of productions: "))

print("Enter productions (Example: A->aB|b)")
for _ in range(n):
    prod = input()
    left, right = prod.split("->")
    grammar[left].extend(right.split("|"))

start_symbol = list(grammar.keys())[0]

# ---------------- FIRST FUNCTION ----------------

def compute_first(symbol):
    if not symbol.isupper():  # terminal
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

# Compute FIRST for all non-terminals
for non_terminal in grammar:
    compute_first(non_terminal)

# ---------------- FOLLOW FUNCTION ----------------

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

# ---------------- OUTPUT ----------------

print("\nFIRST Sets:")
for non_terminal in grammar:
    print(f"FIRST({non_terminal}) = {first[non_terminal]}")

print("\nFOLLOW Sets:")
for non_terminal in grammar:
    print(f"FOLLOW({non_terminal}) = {follow[non_terminal]}")
