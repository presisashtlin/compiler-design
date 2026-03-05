class State:
    def __init__(self, id):
        self.id = id
        self.transitions = {}  # {symbol: [states]}


class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept


state_count = 0


def new_state():
    global state_count
    s = State(state_count)
    state_count += 1
    return s


def basic_nfa(symbol):
    start = new_state()
    accept = new_state()
    start.transitions[symbol] = [accept]
    return NFA(start, accept)


def concatenate(nfa1, nfa2):
    nfa1.accept.transitions['ε'] = [nfa2.start]
    return NFA(nfa1.start, nfa2.accept)


def union(nfa1, nfa2):
    start = new_state()
    accept = new_state()

    start.transitions['ε'] = [nfa1.start, nfa2.start]
    nfa1.accept.transitions['ε'] = [accept]
    nfa2.accept.transitions['ε'] = [accept]

    return NFA(start, accept)


def kleene_star(nfa):
    start = new_state()
    accept = new_state()

    start.transitions['ε'] = [nfa.start, accept]
    nfa.accept.transitions['ε'] = [nfa.start, accept]

    return NFA(start, accept)


def print_nfa(state, visited):
    if state.id in visited:
        return
    visited.add(state.id)

    for symbol in state.transitions:
        for next_state in state.transitions[symbol]:
            print(f"State {state.id} -- {symbol} --> State {next_state.id}")
            print_nfa(next_state, visited)


# ---------------- MAIN ----------------

regex = input("Enter Postfix Regular Expression: ")

stack = []

for ch in regex:
    if ch == '*':
        nfa = stack.pop()
        stack.append(kleene_star(nfa))
    elif ch == '.':
        nfa2 = stack.pop()
        nfa1 = stack.pop()
        stack.append(concatenate(nfa1, nfa2))
    elif ch == '|':
        nfa2 = stack.pop()
        nfa1 = stack.pop()
        stack.append(union(nfa1, nfa2))
    else:
        stack.append(basic_nfa(ch))

final_nfa = stack.pop()

print("\nNFA Transitions:")
visited = set()
print_nfa(final_nfa.start, visited)

print("\nStart State:", final_nfa.start.id)
print("Accept State:", final_nfa.accept.id)
