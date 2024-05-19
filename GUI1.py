import tkinter as tk
import customtkinter
from customtkinter import CTkButton
from PIL import ImageTk, Image
from GUI2 import NFAtoDFAConverter
from GUI import CFGtoPDAScreen

class MainGUI(tk.Tk):

    def __init__(self):
        super().__init__()

        # Set the appearance mode to dark
        customtkinter.set_appearance_mode("Dark")

        # Configure the main window
        self.title("Choose Your Operation")
        self.geometry("700x500")
        self.configure(bg="white")  # Set background color to white

        # Center the window
        self.center_window( self, 750, 500)


        # Create a title label
        title_label = tk.Label(self, text="Choose Your Operation", font=("rockwell", 32), bg="white")
        title_label.pack(pady=10)

        # Create a frame for buttons on the left
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(side=tk.LEFT, padx=20, pady=20)

        # Create buttons for navigation
        self.nfa_button = CTkButton(button_frame, text="NFA/DFA", command=self.open_nfa_screen,
                                    font=("Book Antiqua", 30))
        self.nfa_button.pack(pady=10)

        self.pda_button = CTkButton(button_frame, text="CFG/PDA", command=self.open_pda_screen,
                                    font=("Book Antiqua", 30))
        self.pda_button.pack(pady=25,padx=40)

        # Load and display the resized photo on the right
        photo_path = "back1.png"  # Replace with the actual path to your photo
        self.photo = Image.open(photo_path)
        self.photo = self.photo.resize((550, 410))  # Resize the image
        self.photo = ImageTk.PhotoImage(self.photo)
        photo_label = tk.Label(self, image=self.photo, bg="white")
        photo_label.pack(side=tk.RIGHT, padx=20, pady=20)

    def open_nfa_screen(self):
        # Hide the main menu and open the NFA screen
        self.withdraw()
        nfa_screen = NFAtoDFAConverter()
        nfa_screen.mainloop()

    def open_pda_screen(self):
        # Hide the main menu and open the PDA screen
        self.withdraw()
        pda_screen = CFGtoPDAScreen()
        pda_screen.mainloop()

    def center_window(self, window, width, height):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()
