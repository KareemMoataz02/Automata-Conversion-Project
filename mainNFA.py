# Conversion of epsilon-NFA to DFA and visualization using Graphviz

from graphviz import Digraph


class NFA:
    def __init__(self, states, alphabets, start,
               finals, transitions):
        self.states = states
        self.alphabets = alphabets
        # Adding epsilon alphabet to the list
        self.alphabets.append('ε')
        self.start = start
        self.finals = finals
        self.transitions = transitions

        # transition table is of the form
        # [From State + Alphabet pair] -> [Set of To States]
        self.transition_table = dict()
        for state in self.states:
            for alphabet in self.alphabets:
                self.transition_table[state + alphabet] = set()  # Initialize with empty set
        for from_state, alphabet, to_state in self.transitions:
            self.transition_table[from_state + alphabet].add(to_state)  # Add 'to_state' to the set

        self.alphabets.remove('ε')

    # Method to represent quintuple

    def __repr__(self):
        return "Q : " + str(self.states) + "\nΣ : " \
            + str(self.alphabets) + "\nq0 : " + str(self.start) + "\nF : " \
            + str(self.finals) \
            + "\nδ : \n" + str(self.transition_table)

    def getEpsilonClosure(self, states):
        closure = set(states)
        worklist = list(states)
        while worklist:
            state = worklist.pop()
            # print("transition table",self.transition_table)
            for next_state in self.transition_table.get(state + 'ε', set()):  # Access transition_table directly
                if next_state not in closure:
                    closure.add(next_state)
                    worklist.append(next_state)
        return tuple(sorted(closure))

    def nfa_to_dfa(self):
        # 1. Initialization
        initial_state = self.getEpsilonClosure({self.start})  # Start state with epsilon closure
        dfa_transitions = {}  # Dictionary to store transitions in the resulting DFA
        dfa_final_states = set()  # Set to store final states in the resulting DFA

        # 2. Subset Construction
        unprocessed_dfa_states = [tuple(initial_state)]  # List of unprocessed DFA states (tuples)
        while unprocessed_dfa_states:
            current_state = unprocessed_dfa_states.pop()
            dfa_transitions[current_state] = {}  # Initialize transitions for current state
            for input_symbol in self.alphabets:
                next_states = set()
                for state in current_state:

                    for transition in self.transitions:
                        from_state, alphabet, to_state = transition
                        if from_state == state and alphabet == input_symbol:
                            next_states.add(to_state)
                next_states = tuple(self.getEpsilonClosure(next_states))  # Convert to tuple

                # # Handle Dead States
                if not next_states:  # If next_states is empty (dead state)
                    next_states = 'Dead'  # Create a 'Dead' state tuple
                    if next_states not in dfa_transitions:
                        dfa_transitions[next_states] = {}  # Add transitions for the 'Dead' state
                        for symbol in self.alphabets:
                            dfa_transitions[next_states][symbol] = next_states

                dfa_transitions[current_state][input_symbol] = next_states

                # Add New State and Transition if Necessary
                if next_states not in dfa_transitions:
                    unprocessed_dfa_states.append(next_states)
                    dfa_transitions[next_states] = {}

        # 3. Remove Unreachable States (using string comparisons)
        reachable_states = {tuple(initial_state)}
        new_reachable = True
        while new_reachable:
            new_reachable = False
            for state in list(reachable_states):  # Iterate over a copy to avoid modification issues
                for symbol in dfa_transitions[state]:
                    next_state = dfa_transitions[state][symbol]
                    if next_state not in reachable_states:
                        reachable_states.add(next_state)
                        new_reachable = True

        dfa_transitions = {state: transitions for state, transitions in dfa_transitions.items() if
                           state in reachable_states}

        # 4. Identify Final States
        dfa_final_states = {state for state in dfa_transitions if any(s in self.finals for s in state)}

        # Convert tuples to strings for DFA states
        dfa_transitions = {''.join(state): {symbol: ''.join(next_state) for symbol, next_state in transitions.items()}
                           for state, transitions in dfa_transitions.items()}
        dfa_final_states = {''.join(state) for state in dfa_final_states}

        return {"dfa": dfa_transitions, "final_states": dfa_final_states}


# Making an object of Digraph to visualize NFA diagram
def render_nfa(nfa):
    nfa.graph = Digraph()
    nfa.graph.attr(rankdir='LR')

    # Adding states/nodes in NFA diagram
    for x in nfa.states:
        # If state is not a final state, then border shape is single circle
        # Else it is double circle
        if (x not in nfa.finals):
            nfa.graph.attr('node', shape='circle')
            nfa.graph.node(x)
        else:
            nfa.graph.attr('node', shape='doublecircle')
            nfa.graph.node(x)

    # Adding start state arrow in NFA diagram
    nfa.graph.attr('node', shape='none')
    nfa.graph.node('')
    nfa.graph.edge('', nfa.start)

    # Adding edge between states in NFA from the transitions array
    edge_labels = {}  # Dictionary to store labels for each edge
    for from_state, alphabet, to_state in nfa.transitions:
        edge_key = (from_state, to_state)
        if edge_key not in edge_labels:
            edge_labels[edge_key] = []
        edge_labels[edge_key].append(alphabet)

    for (from_state, to_state), labels in edge_labels.items():
        nfa.graph.edge(from_state, to_state, label=','.join(labels))

    # Makes a pdf with name nfa.graph.pdf and views the pdf
    nfa.graph.format = 'png'
    nfa.graph.render('nfa', view=False)


def render_dfa(dfa_info):
    dfa = Digraph()
    dfa.attr(rankdir='LR')
    # Adding states/nodes in DFA diagram
    for state in dfa_info['dfa']:
        if state not in dfa_info['final_states']:
            dfa.attr('node', shape='circle')
        else:
            dfa.attr('node', shape='doublecircle')
        dfa.node(''.join(state))  # Join the elements of the state tuple without any separator

    # Adding start state arrow in DFA diagram
    dfa.attr('node', shape='none')
    dfa.node('')
    # Assuming the first key in dfa is the start state
    dfa.edge('', list(dfa_info['dfa'].keys())[0])

    # Adding edge between states in DFA
    edge_labels = {}  # Dictionary to store labels for each edge
    for current_state, transitions in dfa_info['dfa'].items():
        for alphabet, next_state in transitions.items():
            edge_key = (current_state, next_state)
            if edge_key not in edge_labels:
                edge_labels[edge_key] = []
            edge_labels[edge_key].append(alphabet)

    for (current_state, next_state), labels in edge_labels.items():
        dfa.edge(current_state, next_state, label=','.join(labels))

    # Makes a pdf with name dfa.graph.pdf and views the pdf
    dfa.format = 'png'
    dfa.render('dfa', view=False)