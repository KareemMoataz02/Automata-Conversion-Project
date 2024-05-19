import customtkinter as ctk
import graphviz

import mainNFA
from customtkinter import CTkLabel, CTkFrame, CTkEntry, CTkButton, CTkToplevel
import os
from PIL import Image
import tkinter.messagebox as messagebox

class NFAtoDFAConverter(ctk.CTk):
    WIDTH = 725
    HEIGHT = 465

    ctk.set_appearance_mode("dark");
    def __init__(self):
        super().__init__()
        self.title("NFA to DFA Converter")
        self.geometry(f"{NFAtoDFAConverter.WIDTH}x{NFAtoDFAConverter.HEIGHT}")
        self.center_window(self, NFAtoDFAConverter.WIDTH, NFAtoDFAConverter.HEIGHT)
        self.transitionEntries = []
        self.edges = []
        self.states = set()

        # Input Screen Elements
        self.create_input_screen()

        # Transitions Table Screen
        self.transitions_table_screen = CTkToplevel()
        self.transitions_table_screen.title("Transitions Table")
        self.transitions_table_screen.withdraw()
        self.create_transitions_table_screen()

        # DFA Screen
        self.dfa_screen = CTkToplevel()
        self.dfa_screen.title("DFA")
        self.dfa_screen.withdraw()
        self.create_dfa_screen()

    def center_window(self, window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_input_screen(self):
        title_label = CTkLabel(master=self, text="NFA Input", font=("rockwell", 40))
        title_label.pack(pady=(20, 40))

        inputs_frame = CTkFrame(master=self)
        inputs_frame.pack()

        labels = ["Start", "Final", "Alphabets", "State"]
        self.entry_fields = {}
        for label_text in labels:
            label = CTkLabel(master=inputs_frame, text=label_text, font=("rockwell", 32))
            label.grid(row=labels.index(label_text), column=0, padx=10, pady=10, sticky="w")
            entry = CTkEntry(master=inputs_frame,
                        font=("Helvetica", 14),
                        justify='center')
            entry.grid(row=labels.index(label_text), column=1, padx=10, pady=10, sticky="ew")
            self.entry_fields[label_text.lower()] = entry

        go_to_transitions_table_button = CTkButton(
            master=self, text="Go to Transitions Table", command=self.goto_transitions_table, font=("Bookman Old Style", 24),
        )
        go_to_transitions_table_button.pack(pady=45)

    def create_transitions_table_screen(self):
        transitions_label = CTkLabel(
            master=self.transitions_table_screen, text="Transitions Table", font=("rockwell", 48)
        )
        transitions_label.pack(pady=20)

        self.center_window(self.transitions_table_screen, 1190, 690)

    def create_dfa_screen(self):
        dfa_label = CTkLabel(master=self.dfa_screen, text="NFA and DFA", font=("rockwell", 48))
        dfa_label.pack(pady=20)

        self.center_window(self.dfa_screen, 1190, 660)

    def get_input_fields(self):
        inputs = {}
        for label_text in ["Start", "Final", "Alphabets", "State"]:
            inputs[label_text.lower()] = self.entry_fields[label_text.lower()].get()
        return inputs

    def place_buttons(self):
        # Create buttons
        self.back_to_first_screen_button = ctk.CTkButton(
            master=self.transitions_table_screen,
            text="Back to NFA Input",
            command=self.goto_first_screen,
            font=("Bookman Old Style", 27),  # Change font

        )
        self.go_to_dfa_screen_button = ctk.CTkButton(
            master=self.transitions_table_screen,
            text="Go to DFA Screen",
            command=self.goto_dfa_screen,
            font=("Bookman Old Style", 27),
        )

        # Pack buttons
        self.back_to_first_screen_button.pack(pady=0, side=ctk.LEFT, expand=True)
        self.go_to_dfa_screen_button.pack(pady=0, side=ctk.LEFT, expand=True)

    def place_button(self):

        # Create and pack the button within the button frame
        go_to_transitions_table_button = CTkButton(
            master=self.dfa_screen,
            text="Go to Transitions Table",
            command=self.goto_transitions_table,
            font=("rockwell", 25),
        )
        go_to_transitions_table_button.pack(pady=20)

    def handle_add_transition(self, row_index, col_index, states, alphabets):
        state1 = states[row_index]
        alphabet = alphabets[col_index]
        input_states = self.transition_entries[row_index][col_index].get().split()
        # Remove all existing edges for the given state and alphabet
        self.edges = [edge for edge in self.edges if not (edge['from'] == state1 and edge['label'] == alphabet)]
        for input_state in input_states:
            if input_state:
                # Check if the input state is in the list of states
                if input_state not in states:
                    messagebox.showwarning("Invalid input", "You can only transition into a state in the list of states.")
                    continue
                # Check if an edge with the same 'from' and 'to' already exists
                existing_edge = next((edge for edge in self.edges if edge['from'] == state1 and edge['to'] == input_state), None)
                if existing_edge:
                    # If it does, check if the new alphabet is already in the label
                    if alphabet not in existing_edge['label'].split(','):
                        # If it's not, append the new alphabet to the label
                        existing_edge['label'] += ',' + alphabet
                else:
                    # If it doesn't, add a new edge
                    self.edges.append({'from': state1, 'to': input_state, 'label': alphabet})
        # Update and re-render the graph
        self.render_and_display_graph()






    def render_and_display_graph(self):
        # Create a new Digraph object
        self.nfa_graph = graphviz.Digraph(comment='NFA')
        self.nfa_graph.attr(rankdir='LR')
        # Add all states and edges from the lists
        for state in self.states:
            if state in self.final_states:
                # If it is, draw it with a double circle
                self.nfa_graph.node(state, peripheries='2')
            else:
                # If it's not, draw it with a single circle
                self.nfa_graph.node(state)
        # Create an invisible node for the start state
        self.nfa_graph.node('', shape='none', width='0', height='0')
        # Add an edge from the invisible node to the start state
        self.nfa_graph.edge('', self.start_state)
        for edge in self.edges:
            self.nfa_graph.edge(edge['from'], edge['to'], label=edge['label'])
        # Render Graphviz image
        self.nfa_graph.format = 'png'
        self.nfa_graph.render(filename='nfa_graph', directory='.', cleanup=True)

        # Load and display Graphviz image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        nfa_image_file = Image.open(os.path.join(image_path, "nfa_graph.png"))
        nfa_width, nfa_height = nfa_image_file.size
        self.nfa_image = ctk.CTkImage(nfa_image_file, size=(nfa_width, nfa_height))

        # Destroy the old label if it exists
        if hasattr(self, 'nfa_label'):
            self.nfa_label.destroy()

        # Create a new label for the state diagram
        self.nfa_label = ctk.CTkLabel(master=self.state_diagram_frame, text="Live Visualization", font=("rockwell", 20), image=self.nfa_image, compound="bottom", pady=10)
        self.nfa_label.pack(padx=40, pady=10)  # Use pack
   

    def goto_transitions_table(self):

        # Get input values from the entry_fields dictionary
        states = self.entry_fields["state"].get().split()
        self.states = self.entry_fields["state"].get().split()
        alphabets = self.entry_fields["alphabets"].get().split()
        self.final_states = self.entry_fields["final"].get().split()
        self.start_state = self.entry_fields["start"].get()

        # Check if the user has inputted anything after a space but didn't type anything
        for field in [states, alphabets, self.final_states, self.start_state]:
            for item in field:
                if item == ' ':
                    messagebox.showwarning("Invalid input", "Please do not leave a space without typing anything.")
                    return
                
        # Check if the user has left a field empty
        if not all([states, alphabets, self.final_states, self.start_state]):
            messagebox.showwarning("Invalid input", "Please fill in all fields.")
            return

        # Check if the user has entered more than one start state
        if ' ' in self.start_state:
            messagebox.showwarning("Invalid input", "Please enter only one start state.")
            return
        
        # Check if the start state is in the list of states
        if self.start_state not in states:
            messagebox.showwarning("Invalid input", "The start state must be in the list of states.")
            return

        # Check if all final states are in the list of states
        for state in self.final_states:
            if state not in states:
                messagebox.showwarning("Invalid input", "All final states must be in the list of states.")
                return
    
        alphabets.append('ε')  # Add epsilon
        self.dfa_screen.withdraw()
        self.withdraw()
        self.transitions_table_screen.deiconify()
        self.center_window(self.transitions_table_screen, 1190, 660)

        # Find and destroy the existing table frame (if any)
        for child in self.transitions_table_screen.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                child.destroy()
            elif isinstance(child, ctk.CTkButton):
                child.destroy()

        # Create the container frame
        container_frame = ctk.CTkFrame(master=self.transitions_table_screen, fg_color='transparent')
        container_frame.pack(padx=20, pady=(30, 20))

        # Create the left frame inside the container frame
        table_frame = ctk.CTkFrame(master=container_frame, fg_color='transparent')
        table_frame.pack(side='left', padx=10, pady=(10, 5))

        # Create the right frame inside the container frame
        self.state_diagram_frame = ctk.CTkFrame(master=container_frame, fg_color='transparent')
        self.state_diagram_frame.pack(side='right', padx=10, pady=(10, 5))

        # Initialize transitions dictionary and Graphviz graph
        self.transitions_dict = {}
        # Clear the edges and states lists
        self.edges = []
        self.states = set()
        # Add initial state nodes and render the initial graph
        for state in states:
            self.states.add(state)

        self.render_and_display_graph()

        # Create alphabet header row
        for c_idx, alphabet in enumerate(alphabets):
            alphabet_label = ctk.CTkLabel(
                master=table_frame,
                text=alphabet,
                font=ctk.CTkFont(size=24, weight="bold"),
            )
            alphabet_label.grid(row=0, column=c_idx + 1, pady=10, padx=10, sticky="we")

        # Initialize self.transition_entries as a nested list
        self.transition_entries = []

        for r_idx, state in enumerate(states):
            row_entries = []  # List to store entry widgets for each row
            for c_idx, alphabet in enumerate(alphabets):
                if c_idx == 0:
                    state_label = ctk.CTkLabel(
                        master=table_frame,
                        text=state,
                        font=ctk.CTkFont(size=24, weight="bold"),

                    )
                    state_label.grid(row=r_idx + 1, column=0, pady=10, padx=10, sticky="we")
                    entry_button_frame = ctk.CTkFrame(master=table_frame, fg_color='transparent')
                    entry_button_frame.grid(row=r_idx + 1, column=1, pady=15, padx=10, sticky="we")
                    # Create entry field with centered text and full-width placeholder
                    entry = ctk.CTkEntry(
                        master=entry_button_frame,
                        width=120,
                        placeholder_text="...",
                        font=("Helvetica", 14),
                        justify='center'
                    )
                    entry.pack(side='left', padx=(0, 10))  # Use pack to place the entry in the frame
                    row_entries.append(entry)  # Store entry widget reference
                    # Create "Add Transition" button next to the entry
                    button = ctk.CTkButton(master=entry_button_frame, text="+", width=5, height=4,
                                           command=lambda r=r_idx, c=c_idx: self.handle_add_transition(r, c, states,
                                                                                                       alphabets))
                    button.pack(side='left')  # Use pack to place the button in the frame
                else:
                    entry_button_frame = ctk.CTkFrame(master=table_frame, fg_color='transparent')
                    entry_button_frame.grid(row=r_idx + 1, column=c_idx + 1, pady=15, padx=10, sticky="we")
                    entry = ctk.CTkEntry(master=entry_button_frame,
                                         width=120,
                                         height=4,
                                         font=("Helvetica", 14),
                                         justify='center',
                                         placeholder_text="...")
                    entry.pack(side='left', padx=(0, 10))  # Use pack to place the entry in the frame
                    row_entries.append(entry)  # Store entry widget reference
                    # Create "Add Transition" button next to the entry
                    button = ctk.CTkButton(master=entry_button_frame, text="+", width=5, height=4,
                                           command=lambda r=r_idx, c=c_idx: self.handle_add_transition(r, c, states,
                                                                                                       alphabets))
                    button.pack(side='left')  # Use pack to place the button in the frame

            self.transition_entries.append(row_entries)  # Store row entries in the main list

        self.place_buttons()

    def goto_first_screen(self):
        self.transitions_table_screen.withdraw()
        self.deiconify()
        self.center_window(self, NFAtoDFAConverter.WIDTH, NFAtoDFAConverter.HEIGHT)

    def goto_dfa_screen(self):

        # Check if any entry in the transition table contains a state not in the list of states
        for row_entries in self.transition_entries:
            for entry in row_entries:
                input_states = entry.get().split()
                for input_state in input_states:
                    if input_state and input_state not in self.states:
                        messagebox.showwarning("Invalid input", "All states in the transition table must be in the list of states.")
                        return
        self.transitions_table_screen.withdraw()
        self.withdraw()
        self.dfa_screen.deiconify()
        self.center_window(self.transitions_table_screen, 1190, 660)

        # Find and destroy the existing table frame (if any)
        for child in self.dfa_screen.winfo_children():
            if isinstance(child, ctk.CTkFrame):
                child.destroy()
            elif isinstance(child, ctk.CTkButton):
                child.destroy()

        # Create the container frame
        container_frame = ctk.CTkFrame(master=self.dfa_screen)
        container_frame.pack(padx=20, pady=(30, 20))

        # Create the left frame inside the container frame
        frame_left = ctk.CTkFrame(master=container_frame)
        frame_left.pack(side='left', padx=10, pady=(10, 5))

        # Create the right frame inside the container frame
        frame_right = ctk.CTkFrame(master=container_frame)
        frame_right.pack(side='right', padx=10, pady=(10, 5))

        # Get NFA information from transition table
        self.nfa = None
        states = self.entry_fields["state"].get().split()
        alphabets = self.entry_fields["alphabets"].get().split()
        start = self.entry_fields["start"].get().split()
        final = self.entry_fields["final"].get().split()
        transition = []
        alphabets.append('ε')
        for r_idx, state in enumerate(states):
            for c_idx, alphabet in enumerate(alphabets):
                # if c_idx > 0:  # Skip the first column (state labels)
                    inputs = self.transition_entries[r_idx][c_idx].get().split()  # Adjust index for entry widgets
                    # inputs = self.transitionEntries[r_idx][c_idx].get().split()
                    if len(inputs) > 0:
                        for input in inputs:
                            edge = [state, alphabet, input]
                            transition.append(edge)
        print(states, '\n', alphabets, '\n', start, '\n', final, '\n', transition)
        alphabets.remove('ε')
        self.nfa = mainNFA.NFA(states, alphabets, start[0], final, transition)

        # Render NFA and DFA
        mainNFA.render_nfa(self.nfa)
        dfa_info = mainNFA.NFA.nfa_to_dfa(self.nfa)
        mainNFA.render_dfa(dfa_info)

        # Load images
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
        nfa_image_file = Image.open(os.path.join(image_path, "nfa.png"))
        dfa_image_file = Image.open(os.path.join(image_path, "dfa.png"))
        nfa_width, nfa_height = nfa_image_file.size
        dfa_width, dfa_height = dfa_image_file.size

        # Create CTkImages
        self.nfa_image = ctk.CTkImage(nfa_image_file, size=(nfa_width, nfa_height))
        self.dfa_image = ctk.CTkImage(dfa_image_file, size=(dfa_width, dfa_height))

        nfa_label = ctk.CTkLabel(master=frame_left, text="NFA", font=("rockwell", 40), image=self.nfa_image,
                                 compound="bottom", pady=10)
        nfa_label.pack(padx=40, pady=10)  # Use pack

        dfa_label = ctk.CTkLabel(master=frame_right, text="DFA", font=("rockwell", 40), image=self.dfa_image,
                                 compound="bottom", pady=10)
        dfa_label.pack(padx=40, pady=10)  # Use pack

        self.place_button()

if __name__ == "__main__":
    app = NFAtoDFAConverter()
    app.mainloop()

