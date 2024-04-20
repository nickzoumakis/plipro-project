import customtkinter as ctk

class Window:
    def __init__(self):
        ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green
        self.app = ctk.CTk()  # create CTk window like you do with the Tk window
        self.app.geometry("400x240")

        # Use CTkButton instead of tkinter Button
        self.entry_name= ctk.CTkEntry(master=self.app, font=("Arial", 18), text_color="black", fg_color="white",width=270)
        self.entry_name.place(relx=0.5, rely=0.5)

        self.button = ctk.CTkButton(master=self.app, text="CTkButton", command=self.button_function)
        self.button.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    def button_function(self):
        print(f"You entered the name {self.entry_name.get()}")

    def run(self):
        self.app.mainloop()

w = Window()
w.run()