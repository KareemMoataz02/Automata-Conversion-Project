import os
from PIL import Image
from customtkinter import CTkLabel, CTkFrame, CTkEntry, CTkButton, CTk, CTkToplevel
from CFG_to_PDA import get_user_cfg, cfg_to_pda, render_pda
import customtkinter as ctk

class CFGtoPDAScreen(CTk):
    WIDTH = 600
    HEIGHT = 400

    def __init__(self):
        super().__init__()
        self.title("CFG to PDA Converter")
        self.geometry(f"{CFGtoPDAScreen.WIDTH}x{CFGtoPDAScreen.HEIGHT}")
        self.center_window(self, CFGtoPDAScreen.WIDTH, CFGtoPDAScreen.HEIGHT)
        self.create_input_screen()

    def center_window(self, window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_input_screen(self):
        title_label = CTkLabel(master=self, text="CFG Input", font=("rockwell", 30))
        title_label.pack(pady=(20, 40))

        inputs_frame = CTkFrame(master=self)
        inputs_frame.pack()

        labels = ["Variables", "Terminals", "Start Symbol", "Productions"]
        entry_texts = ["Variables (non-terminal symbols, comma-separated)", "Terminals (comma-separated)",
                       "Start Symbol", "Productions (<non-terminal> -> <production>, comma-separated)"]
        self.entry_fields = {}
        for label_text, entry_text in zip(labels, entry_texts):
            label = CTkLabel(master=inputs_frame, text=label_text, font=("rockwell", 18))
            label.grid(row=labels.index(label_text), column=0, padx=10, pady=10, sticky="w")
            entry = CTkEntry(master=inputs_frame, placeholder_text=entry_text)
            entry.grid(row=labels.index(label_text), column=1, padx=10, pady=10, sticky="ew")
            self.entry_fields[label_text.lower().replace(' ', '_')] = entry

        go_button = CTkButton(master=self, text="Convert", command=self.convert_cfg_to_pda)
        go_button.pack(pady=20)

    def convert_cfg_to_pda(self):

        # Retrieve inputs from entry fields
        variables = self.entry_fields["variables"].get().strip().replace(' ', '').split(',')
        terminals = self.entry_fields["terminals"].get().strip().replace(' ', '').split(',')
        start_symbol = self.entry_fields["start_symbol"].get().strip().replace(' ', '')
        productions = self.entry_fields["productions"].get().strip().replace(' ', '').split(',')

        print(productions)
        # Call the get_user_cfg() function
        cfg = get_user_cfg(variables, terminals, start_symbol, productions)

        if cfg != None:
            # Call the cfg_to_pda() function to convert CFG to PDA
            pda = cfg_to_pda(cfg)

            print("\nCreated PDA:")
            print("States:", pda.states)
            print("Input Alphabet:", pda.input_alphabet)
            print("Stack Alphabet:", pda.stack_alphabet)
            print("Initial State:", pda.initial_state)
            print("Stack Start Symbol:", pda.stack_start_symbol)
            print("Final States:", pda.final_states)

            print("\nTransition Function: ")
            counter = 1
            for transition in pda.transition_function:
                print(
                    f'{counter} - (\'{transition.initial_state}\', \'{transition.char_to_read}\', \'{transition.char_to_pop}\') -> (\'{transition.final_state}\', \'{transition.str_to_push}\')')
                counter += 1

            render_pda(pda)

            # Load images
            image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "")
            pda_image_file = Image.open(os.path.join(image_path, "pda.png"))
            pda_width, pda_height = pda_image_file.size

            # Close the previous PDA window if it exists
            if hasattr(self, "pda_window"):
                self.pda_window.destroy()

            # Create a new window to display the PDA image
            self.pda_window = PDAScreen(pda_image_file)
            self.pda_window.center_window(self.pda_window, pda_width, pda_height)
            self.pda_window.mainloop()


class PDAScreen(CTkToplevel):
    def __init__(self, pda_image):
        super().__init__()
        self.title("PDA Image")
        self.pda_image = ctk.CTkImage(pda_image, size=(pda_image.width, pda_image.height))
        pda_label = ctk.CTkLabel(master=self, image=self.pda_image)
        pda_label.pack()

    def center_window(self, window, width, height):
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


if __name__ == "__main__":
    app = CFGtoPDAScreen()
    app.mainloop()
