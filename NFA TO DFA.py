from collections import defaultdict, deque

def epsilon_closure(states, transitions):
    stack = list(states)
    closure = set(states)

    while stack:
        state = stack.pop()
        for next_state in transitions[state]['ε']:
            if next_state not in closure:
                closure.add(next_state)
                stack.append(next_state)

    return closure


def move(states, symbol, transitions):
    result = set()
    for state in states:
        result.update(transitions[state][symbol])
    return result


# ---------------- MAIN ----------------

n = int(input("Enter number of NFA states: "))
symbols = input("Enter input symbols (no space, e.g. ab): ")

transitions = defaultdict(lambda: defaultdict(list))

print("\nEnter transitions (comma separated states, - for none):")

for state in range(n):
    for symbol in symbols:
        value = input(f"δ({state},{symbol}) = ")
        if value != '-':
            transitions[state][symbol] = list(map(int, value.split(',')))
    # epsilon transitions
    value = input(f"δ({state},ε) = ")
    if value != '-':
        transitions[state]['ε'] = list(map(int, value.split(',')))

start_state = int(input("\nEnter start state: "))
final_states = set(map(int, input("Enter final states (comma separated): ").split(',')))

# Subset Construction
dfa_states = []
dfa_transitions = {}
queue = deque()

start_closure = epsilon_closure({start_state}, transitions)
queue.append(frozenset(start_closure))
dfa_states.append(frozenset(start_closure))

while queue:
    current = queue.popleft()
    dfa_transitions[current] = {}

    for symbol in symbols:
        moved = move(current, symbol, transitions)
        closure = epsilon_closure(moved, transitions)
        closure = frozenset(closure)

        if closure:
            dfa_transitions[current][symbol] = closure
            if closure not in dfa_states:
                dfa_states.append(closure)
                queue.append(closure)

# ---------------- OUTPUT ----------------

print("\nDFA States:")
for state in dfa_states:
    print(set(state))

print("\nDFA Transition Table:")
for state in dfa_transitions:
    for symbol in dfa_transitions[state]:
        print(f"{set(state)} -- {symbol} --> {set(dfa_transitions[state][symbol])}")

print("\nDFA Final States:")
for state in dfa_states:
    if state & final_states:
        print(set(state))
