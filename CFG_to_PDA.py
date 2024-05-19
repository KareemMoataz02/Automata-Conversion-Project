import re
from graphviz import Digraph
from tkinter import messagebox


class CFG:
    def __init__(self, non_terminals, terminals, start_symbol, productions):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.start_symbol = start_symbol
        self.productions = productions


class PDA:
    def __init__(self, states, input_alphabet, stack_alphabet, transition_function, initial_state, stack_start_symbol,
                 final_states):
        self.states = states
        self.input_alphabet = input_alphabet
        self.stack_alphabet = stack_alphabet
        self.transition_function = transition_function
        self.initial_state = initial_state
        self.stack_start_symbol = stack_start_symbol
        self.final_states = final_states


class transition:
    def __init__(self, initial_state, char_to_read, char_to_pop, final_state, str_to_push):
        self.initial_state = initial_state
        self.char_to_read = char_to_read
        self.char_to_pop = char_to_pop
        self.final_state = final_state
        self.str_to_push = str_to_push




def get_user_cfg(variables, terminals, start_symbol, productions_str):
    productions = {}

    if start_symbol not in variables:
        messagebox.showerror("Error", "ERROR IN THE INPUT OF CFG!!!\nSTART SYMBOL MUST BE A NON-TERMINAL")
        return None

    for production_str in productions_str:
        non_terminal, production = re.split(r'\s*->\s*', production_str)

        if non_terminal not in variables:
            messagebox.showerror("Error", "ERROR IN THE INPUT OF CFG!!!\nLHS OF PRODUCTION RULE MUST BE A NON-TERMINAL")
            return None

        for prod in production.strip():
            if prod not in terminals and prod not in variables:
                messagebox.showerror("Error",
                                     "ERROR IN THE INPUT OF CFG!!!\nRHS OF PRODUCTION RULE MUST BE A NON-TERMINAL OR TERMINAL")
                return None

        if non_terminal not in productions:
            productions[non_terminal] = []
        productions[non_terminal].append(production.strip())

    # If everything is fine, return CFG object
    return CFG(variables, terminals, start_symbol, productions)


def cfg_to_pda(cfg):
    # Step 1: Define states
    states = {'q0', 'q1', 'qf'}

    # Step 2: Determine input alphabet and stack alphabet
    input_alphabet = set(cfg.terminals)
    stack_alphabet = set(cfg.non_terminals) | set(cfg.terminals)

    # Step 3: Define transition function
    transition_function = []

    # Add transition for pushing start symbol onto stack
    transition_function.append(transition('q0', 'ε', 'ε', 'q1', cfg.start_symbol + '$'))

    # Add transitions for productions
    for non_terminal, productions in cfg.productions.items():
        for production in productions:
            if production == '':
                transition_function.append(transition('q1', 'ε', non_terminal, 'q1', 'ε'))

            else:
                transition_function.append(transition('q1', 'ε', non_terminal, 'q1', production))

    for terminals in cfg.terminals:
        transition_function.append(transition('q1', terminals, terminals, 'q1', 'ε'))

    # Add transition for popping stack start symbol at the end
    transition_function.append(transition('q1', 'ε', '$', 'qf', 'ε'))

    # Step 4: Define initial state, stack start symbol, and final states
    initial_state = 'q0'
    stack_start_symbol = cfg.start_symbol
    final_states = {'qf'}

    # Create and return the PDA object
    return PDA(states, input_alphabet, stack_alphabet, transition_function, initial_state, stack_start_symbol,
               final_states)


def render_pda(pda_info: PDA):
    pda = Digraph()
    pda.attr(rankdir='LR')
    # Adding states/nodes in PDA diagram
    for state in pda_info.states:
        if state != pda_info.final_states:
            pda.attr('node', shape='circle')
        else:
            pda.attr('node', shape='doublecircle')
        pda.node(''.join(state))  # Join the elements of the state tuple without any separator

    # Adding start state arrow in PDA diagram
    pda.attr('node', shape='none')
    pda.node('')

    # Assuming the first key in PDA is the start state
    pda.edge('', pda_info.initial_state)

    # Adding edge between states in DFA
    edge_labels = {}  # Dictionary to store labels for each edge

    for transition in pda_info.transition_function:
        edge_key = (transition.initial_state, transition.final_state)
        if edge_key not in edge_labels:
            edge_labels[edge_key] = []
        edge_labels[edge_key].append(f'{transition.char_to_read}, {transition.char_to_pop} -> {transition.str_to_push} \n')

    for (current_state, next_state), labels in edge_labels.items():
        pda.edge(current_state, next_state, label=','.join(labels))

    # # Adding edge between states in DFA
    # for current_state, transitions in dfa_info['dfa'].items():
    #     for alphabet, next_state in transitions.items():
    #         dfa.edge(current_state,next_state, label=alphabet)

    # Makes a pdf with name dfa.graph.pdf and views the pdf
    pda.format = 'png'
    pda.render('pda', view=False)
