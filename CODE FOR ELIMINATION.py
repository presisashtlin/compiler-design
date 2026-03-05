# Program to Eliminate Immediate Left Recursion and Perform Left Factoring

def eliminate_left_recursion(grammar):
    new_grammar = {}

    for non_terminal in grammar:
        alpha = []  # left recursive part
        beta = []   # non left recursive part

        for production in grammar[non_terminal]:
            if production.startswith(non_terminal):
                alpha.append(production[len(non_terminal):])
            else:
                beta.append(production)

        if alpha:
            new_non_terminal = non_terminal + "'"
            new_grammar[non_terminal] = []
            new_grammar[new_non_terminal] = []

            for b in beta:
                new_grammar[non_terminal].append(b + new_non_terminal)

            for a in alpha:
                new_grammar[new_non_terminal].append(a + new_non_terminal)

            new_grammar[new_non_terminal].append("ε")
        else:
            new_grammar[non_terminal] = grammar[non_terminal]

    return new_grammar


def left_factoring(grammar):
    new_grammar = {}

    for non_terminal in grammar:
        productions = grammar[non_terminal]
        prefix_dict = {}

        for prod in productions:
            prefix = prod[0]
            prefix_dict.setdefault(prefix, []).append(prod)

        if any(len(v) > 1 for v in prefix_dict.values()):
            new_grammar[non_terminal] = []
            for prefix in prefix_dict:
                group = prefix_dict[prefix]
                if len(group) > 1:
                    new_non_terminal = non_terminal + "_F"
                    new_grammar[non_terminal].append(prefix + new_non_terminal)
                    new_grammar[new_non_terminal] = [
                        g[1:] if len(g) > 1 else "ε" for g in group
                    ]
                else:
                    new_grammar[non_terminal].append(group[0])
        else:
            new_grammar[non_terminal] = productions

    return new_grammar


# ---------------- MAIN ----------------

grammar = {}

n = int(input("Enter number of productions: "))

print("Enter productions in format A->Aa|b")

for _ in range(n):
    prod = input()
    left, right = prod.split("->")
    grammar[left] = right.split("|")

print("\nOriginal Grammar:")
for nt in grammar:
    print(nt, "->", " | ".join(grammar[nt]))

# Eliminate Left Recursion
grammar = eliminate_left_recursion(grammar)

print("\nAfter Eliminating Left Recursion:")
for nt in grammar:
    print(nt, "->", " | ".join(grammar[nt]))

# Left Factoring
grammar = left_factoring(grammar)

print("\nAfter Left Factoring:")
for nt in grammar:
    print(nt, "->", " | ".join(grammar[nt]))
