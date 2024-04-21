"""Αντικειμενοστραφής υλοποίηση για το interface"""
from tree_oop import Person, Graph
from pathlib import Path
import pygraphviz as pgv
from json import load
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import simpledialog
import json

class MainApp:

    def __init__(self):
        # αρχικοποίηση κενού dict που θα φιλοξενήσει όλα τα στοιχεία των ατόμων που προσθέτει ο χρήστης
        self.family_data = {}

        # Στοιχεία και γεωμετρία παραθύρου
        self.app = ctk.CTk()
        self.app.geometry("1500x900")
        self.label_title= ctk.CTkLabel(master=self.app, text="Genealogy Tree", font=("Arial", 25), text_color="black")
        self.label_title.place(relx=0.5, rely=0.05, anchor="center")
        ctk.set_appearance_mode("light")

        self.middle = tk.Frame(self.app, pady=10.5, highlightthickness=2, height=30, width=20)
        self.middle.pack(side = ctk.LEFT)
        self.checkbox_male_var = tk.StringVar()
        self.checkbox_female_var = tk.StringVar()

        #LABELS FOR INPUT & TEXT ENTRY
        self.label_name= ctk.CTkLabel(master=self.app, text=" Name :", font=("Arial", 18), text_color="black")
        self.label_name.place(relx=0.02, rely=0.1, anchor="nw")
        self.entry_name= ctk.CTkEntry(master=self.app, font=("Arial", 18), text_color="black", fg_color="white",width=270)
        self.entry_name.place(relx=0.065, rely=0.1, anchor="nw")

        self.label_surname= ctk.CTkLabel(master=self.app, text=" Surname :", font=("Arial", 18), text_color="black")
        self.label_surname.place(relx=0.25, rely=0.1, anchor="nw")
        self.entry_surname= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=270)
        self.entry_surname.place(relx=0.32, rely=0.1, anchor="nw")

        self.label_date= ctk.CTkLabel(master=self.app, text=" Date of Birth :", font=("Arial", 18), text_color="black")
        self.label_date.place(relx=0.52, rely=0.1, anchor="nw")
        self.entry_date= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_date.place(relx=0.61, rely=0.1, anchor="nw")

        self.label_id= ctk.CTkLabel(master=self.app, text=" ID :", font=("Arial", 18), text_color="black")
        self.label_id.place(relx=0.02, rely=0.15, anchor="nw")
        self.entry_id= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=230)
        self.entry_id.place(relx=0.053, rely=0.15, anchor="nw")

        self.label_mother_name= ctk.CTkLabel(master=self.app, text=" Mother's name :", font=("Arial", 18), text_color="black")
        self.label_mother_name.place(relx=0.02, rely=0.20, anchor="nw")
        self.entry_mother_name= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=206)
        self.entry_mother_name.place(relx=0.11, rely=0.20, anchor="nw")

        self.label_mother_surname= ctk.CTkLabel(master=self.app, text=" Mother's surname :", font=("Arial", 18), text_color="black")
        self.label_mother_surname.place(relx=0.25, rely=0.20, anchor="nw")
        self.entry_mother_surname= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_mother_surname.place(relx=0.36, rely=0.20, anchor="nw")

        self.label_mother_id= ctk.CTkLabel(master=self.app, text=" Mother's (ID) :", font=("Arial", 18), text_color="black")
        self.label_mother_id.place(relx=0.52, rely=0.20, anchor="nw")
        self.entry_mother_id= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_mother_id.place(relx=0.6, rely=0.20, anchor="nw")

        self.label_death= ctk.CTkLabel(master=self.app, text=" Date of Death :", font=("Arial", 18), text_color="black")
        self.label_death.place(relx=0.52, rely=0.15, anchor="nw")
        self.entry_death= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_death.place(relx=0.61, rely=0.15, anchor="nw")

        self.label_father_name= ctk.CTkLabel(master=self.app, text=" Father's name :", font=("Arial", 18), text_color="black")
        self.label_father_name.place(relx=0.02, rely=0.25, anchor="nw")
        self.entry_father_name= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=206)
        self.entry_father_name.place(relx=0.11, rely=0.25, anchor="nw")

        self.label_father_surname= ctk.CTkLabel(master=self.app, text=" Father's surname :", font=("Arial", 18), text_color="black")
        self.label_father_surname.place(relx=0.25, rely=0.25, anchor="nw")
        self.entry_father_surname= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_father_surname.place(relx=0.36, rely=0.25, anchor="nw")

        self.label_father_id= ctk.CTkLabel(master=self.app, text=" Father's (ID) :", font=("Arial", 18), text_color="black")
        self.label_father_id.place(relx=0.52, rely=0.25, anchor="nw")
        self.entry_father_id= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_father_id.place(relx=0.6, rely=0.25, anchor="nw")

        self.label_spouse= ctk.CTkLabel(master=self.app, text=" Spouse (ID) :", font=("Arial", 18), text_color="black")
        self.label_spouse.place(relx=0.02, rely=0.30, anchor="nw")
        self.entry_spouse= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_spouse.place(relx=0.11, rely=0.30, anchor="nw")



        # CHECKBOXES
        # TODO: Προσθήκη command ώστε όταν επιλέγεται το ένα κουτί, να απενεργοποιείται το άλλο
        self.checkbox_male = ctk.CTkCheckBox(master=self.app, text="Male", font=("Arial", 12), hover=True, fg_color="grey", bg_color="Light grey")
        self.checkbox_male.place(relx=0.25, rely=0.15, anchor="nw")
        self.checkbox_female = ctk.CTkCheckBox(master=self.app, text="Female", font=("Arial", 12), hover=True, fg_color="grey", bg_color="light grey")
        self.checkbox_female.place(relx=0.33, rely=0.15, anchor="nw")


        # Κουμπιά αλληλεπίδρασης χρήστη, κάθε command οδηγεί σε νέο function του class
        self.btn_add = ctk.CTkButton(master=self.app, text="Προσθήκη νέου ατόμου", corner_radius=32, command=self.add_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=4, width=20, height=50)
        self.btn_add.place(relx=0.13, rely=0.8, anchor="ne")

        # αλλαγή κουμπιού σε 'Καταχώρηση' -> περνάει όλα τα άτομα από το family tree dict στο json και καλεί το Graph 
        # TODO: υλοποίηση της create_tree με κλήση των Person και Graph από το tree_oop.py
        self.btn_treeview = ctk.CTkButton(master=self.app, text="Δημιουργία Δέντρου", corner_radius=32, command=self.create_tree,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=4, width=20, height=50)
        self.btn_treeview.place (relx=0.30, rely=0.8, anchor="ne")

        self.btn_clear = ctk.CTkButton(master=self.app, text="Καθαρισμός πεδίων", corner_radius=32, command=self.clear_fields,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50)
        self.btn_clear.place (relx=0.45, rely=0.8, anchor="ne")

        self.btn_search = ctk.CTkButton(master=self.app, text="Aναζήτηση ατόμου", corner_radius=32, #command=search_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50)
        self.btn_search.place(relx=0.6, rely=0.8, anchor="ne")

        self.btn_update = ctk.CTkButton(master=self.app, text="Ενημέρωση στοιχείων ατόμου", corner_radius=32, #command=update_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50)
        self.btn_update.place(relx=0.80, rely=0.8, anchor="ne")

        self.btn_delete = ctk.CTkButton(master=self.app, text="Διαγραφή ατόμου", corner_radius=32,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50)
        self.btn_delete.place(relx=0.95, rely=0.8, anchor="ne")



        # treeview
        self.table = ttk.Treeview(self.middle, columns=("Unique ID", "Name", "Surname", "Mother_Name", "Mother_Surname", "Mother ID", "Father_Name", "Father_Surname", "Father ID"),
                            show='headings')
        # Change font size of the headings
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 12))

        # TODO: το κείμενο στο treeview να στοιχιστεί στο κέντρο κάθε στήλης
        # Change font size of the content
        self.style.configure("Treeview", font=('Arial', 10), anchor=tk.CENTER)

        self.table.heading("#1", text='Unique_id',  anchor=tk.CENTER)
        #self.table.column("#1", width=140)
        self.table.heading("#2", text='First name', anchor=tk.CENTER)
        self.table.heading("#3", text='Surname', anchor=tk.CENTER)
        #self.table.column("#3", width=190)
        self.table.heading("#4", text="Mother's Name", anchor=tk.CENTER)
        self.table.heading("#5", text="Mother's Surname", anchor=tk.CENTER)
        self.table.heading("#6", text="Mother's ID", anchor=tk.CENTER)
        self.table.heading("#7", text="Father's Name", anchor=tk.CENTER)
        self.table.heading("#8", text="Father's Surname", anchor=tk.CENTER)
        self.table.heading("#9", text="Father's ID", anchor=tk.CENTER)
    

    """add_person: Προσθέτει τα στοιχεία του ατόμου στον πίνακα του παραθύρου και ενημερώνει το dict"""
    # TODO: αμυντικός για μοναδικότητα ID κάθε ατόμου, έγκυρους χαρακτήρες γενικά στα πεδία
    def add_person(self):
        # λήψη του μοναδικού κωδικού του ατόμου
        id = self.entry_id.get()

        # για κάθε στοιχείο που εισήγαγε ο χρήστης
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        dob = self.entry_date.get()
        gender = self.checkbox_male.get()
        dod = self.entry_death.get()
        mother_name = self.entry_mother_name.get()
        mother_surname = self.entry_mother_surname.get()
        mother_id = self.entry_mother_id.get()
        father_name = self.entry_father_name.get()
        father_surname = self.entry_father_surname.get()
        father_id = self.entry_father_id.get()
        spouse_id = self.entry_spouse.get()

        # προσθήκη στο λεξικό family_data
        self.family_data[id] = {
            "name": name,
            "surname": surname,
            "date_of_birth": dob,
            "gender" : 'male' if gender == 1 else 'female',
            "date_of_death": dod,
            "mother_name": mother_name,
            "mother_surname": mother_surname,
            "mother_id": mother_id,
            "father_name": father_name,
            "father_surname": father_surname,
            "father_id": father_id,
            "spouse_id": spouse_id
        }
        #print(self.family_data)

        # Προσθέτει το νέο άτομο στο treeview-gui table
        self.table.insert('', 'end', values=(
            id, 
            name, 
            surname, 
            mother_name, 
            mother_surname, 
            mother_id,
            father_name,
            father_surname, 
            father_id)
            ), 
        
        # Καθάρισμα των πεδίων για το επόμενο άτομο
        self.clear_fields()
        

    """clear_fields: Καθαρίζει όλα τα πεδία"""
    def clear_fields(self):
        for entry in [self.entry_name,
                    self.entry_surname,
                    self.entry_date,
                    self.entry_id,
                    self.entry_mother_name,
                    self.entry_mother_surname,
                    self.entry_mother_id,
                    self.entry_father_name,
                    self.entry_father_surname,
                    self.entry_father_id,
                    self.entry_spouse,
                    self.entry_death]:
            entry.delete(0, 'end')
        
        # Ξετσεκάρει τα checkboxes
        for checkbox in [self.checkbox_male, self.checkbox_female]:
            if checkbox.get() == 1:
                checkbox.toggle()

    """run: Υλοποιεί και εμφανίζει το παράθυρο της εφαρμογής"""
    def run(self):
        self.table.pack(fill='both', expand=True)
        self.app.mainloop()


    """create_tree: Καλεί το Graph class (απο το module tree_oop) και σχεδιάζει εικόνα του δέντρου"""
    def create_tree(self):
        graph = Graph(self.family_data)
        graph.show()


"""Συνάρτηση main"""
def main():
    # υλοποίηση του παραθύρου
    family_tree = MainApp()
    family_tree.run()


"""

def load_family_tree():
    try:
        with open("familia_tree.json", "r") as f:
            family_tree = json.load(f)
            print("file opened")
        return family_tree
    except FileNotFoundError:
        print("Family tree file not found.")
        return None

def save_family_tree(family_tree):
    with open("familia_tree.json", "w") as f:
        json.dump(family_tree, f, indent=4)


def is_list_empty(lst):
    if len(lst) == 0:
        print("The list is empty")
    else:
        print("The list is not empty")

# TODO: add_person: Aρκεί να φτιάξει το json με τα στοιχεία από το λεξικό family_tree. Χρήση του Person class εδώ μάλλον περιττή
def add_person():
    # TODO: αμυντικός για μοναδικότητα ID κάθε ατόμου, έγκυρους χαρακτήρες γενικά στα πεδία
    
    #  προσθήκη μοναδικού κωδικού που έδωσε ο χρήστης (unique_id του Person class καταργήθηκε) 
    id = entry_id.get()

    name = entry_name.get()
    surname = entry_surname.get()
    date_of_birth = entry_date.get()
    gender = 0 if checkbox_male_var.get() else 1
    date_of_death = entry_death.get()
    mother_name = entry_mother_name.get()
    mother_surname = entry_mother_surname.get()
    father_name = entry_father_name.get()
    father_surname = entry_father_surname.get()
    mother_id = entry_mother_id.get()
    father_id = entry_father_id.get()
    spouse_id = entry_spouse.get()

    # αρχικοποιει ενα κενο dict με τα στοιχεία του ατόμου
    family_tree = {}

    # Ενημέρωση δενδρου με το νέο άτομο
    family_tree[id] = {
        "name": name,
        "surname": surname,
        "date_of_birth": date_of_birth,
        "gender" : gender,
        "date_of_death": date_of_death,
        "mother_name": mother_name,
        "mother_surname": mother_surname,
        "mother_id": mother_id,
        "father_name": father_name,
        "father_surname": father_surname,
        "father_id": father_id,
        "spouse_id": spouse_id
    }

    # Save το δενδρο στο αρχειο json
    try:
        save_family_tree(family_tree)
        print("Family tree saved successfully.")
    except Exception as e:
        print("An error occurred while saving the family tree:", e)

    # Προσθέτει το νέο άτομο στο treeview-gui table
    table.insert('', 'end', values=(
        id, name, surname, date_of_birth, date_of_death, mother_id, father_id, spouse_id, gender))

    # Clear all input fields
    clear_fields()
class SearchDialog(tk.simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="ID:").grid(row=0)
        tk.Label(master, text="Name:").grid(row=1)
        tk.Label(master, text="Surname:").grid(row=2)
        tk.Label(master, text="Mother's Surname:").grid(row=3)
        tk.Label(master, text="Mother's ID:").grid(row=4)
        tk.Label(master, text="Father's Surname:").grid(row=5)
        tk.Label(master, text="Father's ID:").grid(row=6)

        #  Να προσθέσω και άλλα πεδία

        self.id_entry = tk.Entry(master)
        self.name_entry = tk.Entry(master)
        self.surname_entry = tk.Entry(master)
        self.mother_surname_entry = tk.Entry(master)
        self.mother_id_entry = tk.Entry(master)
        self.father_surname_entry = tk.Entry(master)
        self.father_id_entry = tk.Entry(master)

        # Να προσθέσω και άλλα πεδία

        self.id_entry.grid(row=0, column=1)
        self.name_entry.grid(row=1, column=1)
        self.surname_entry.grid(row=2, column=1)
        self.mother_surname_entry.grid(row=3, column=1)
        self.mother_id_entry.grid(row=4, column=1)
        self.father_surname_entry.grid(row=5, column=1)
        self.father_id_entry.grid(row=6, column=1)
        #  Να προσθέσω και άλλα πεδία

    def apply(self):
        unique_id = self.id_entry.get()
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        mother_surname = self.mother_surname_entry.get()
        mother_id = self.mother_id_entry.get()
        father_surname = self.father_surname_entry.get()
        father_id = self.father_id_entry.get()
        #  Να προσθέσω και άλλα πεδία
        self.result = (unique_id, name, surname, mother_surname, mother_id, father_surname, father_id)
        is_list_empty(Person.all)
def search_person():
    dialog = SearchDialog(app)
    is_list_empty(Person.all)

    if dialog.result:
        unique_id, name, surname, mother_surname, mother_id, father_surname, father_id = dialog.result

        # Filter persons based on search criteria
        print("Search Criteria:")
        print("Unique ID:", unique_id)
        print("Name (lowercase):", name.lower())
        print("Surname (lowercase):", surname.lower())

        filtered_persons = [
            person for person in Person.all
                if (str(person.unique_id) == unique_id or not unique_id) and
                   (person.name.lower() == name.lower() or not name) and
                   (person.surname.lower() == surname.lower() or not surname) and
                   (person.mother_surname.lower() == mother_surname.lower() or not mother_surname) and
                   (str(person.mother_id) == mother_id or not mother_id) and
                   (person.father_surname.lower() == father_surname.lower() or not father_surname) and
                   (str(person.father_id) == father_id or not father_id)
        ]
        print("All Persons:")
        for person in Person.all:
            print(person.unique_id, person.name, person.surname)

        print("Filtered Persons:", filtered_persons)
        if filtered_persons:
            found_person = filtered_persons[0]  # Take the first matching person
            return found_person
        else:
            return None

        if found_person:
            # Fill the fields
            entry_name.delete(0, 'end')
            entry_name.insert(0, found_person.name)

            entry_surname.delete(0, 'end')
            entry_surname.insert(0, found_person.surname)

            entry_date.delete(0, 'end')
            entry_date.insert(0, found_person.date_of_birth)

            entry_id.delete(0, 'end')
            entry_id.insert(0, found_person.unique_id)

            entry_mother_surname.delete(0, 'end')
            entry_mother_surname.insert(0, found_person.mother_surname)

            entry_mother_id.delete(0, 'end')
            entry_mother_id.insert(0, found_person.mother_id)

            entry_father_surname.delete(0, 'end')
            entry_father_surname.insert(0, found_person.father_surname)

            entry_father_id.delete(0, 'end')
            entry_father_id.insert(0, found_person.father_id)

            entry_spouse.delete(0, 'end')
            entry_spouse.insert(0, found_person.spouse_id)

            entry_death.delete(0, 'end')
            entry_death.insert(0, found_person.date_of_death)
                    # Τικάρει το ανάλογο checkbox male or female
            if found_person.gender == 'Male':
                checkbox_male_var.set("1")
            else:
                checkbox_female_var.set("1")
        else:
            table.insert('', 'end', values=("Person not found", "", "", "", "", "", "", ""))
    else:
            # # Αν δεν δώσει δεδομένα ο χρήστης
        pass
# Αποθηκευει το δενδρο στο JSON file

def update_person():
    # Get the ID of the person to update
    person_id = entry_id.get()

     # Search for the person with the given ID
    found_person = None
    for person in Person.all:
        if person.unique_id == person_id:
            found_person = person
            break

    if found_person:
            # Update fields
        found_person.name = entry_name.get()
        found_person.surname = entry_surname.get()
        found_person.date_of_birth = entry_date.get()
        found_person.gender = "Male" if checkbox_male_var.get() else "Female"
        found_person.mother_id = entry_mother_id.get()
        found_person.father_id = entry_father_id.get()
        found_person.spouse_id = entry_spouse.get()
        found_person.date_of_death = entry_death.get()

        # Update the treeview
        table.item(table.selection(), values=(found_person.name, found_person.surname, found_person.date_of_birth,
                                              found_person.date_of_death, found_person.mother_name, found_person.mother_surname, found_person.mother_id,
                                              found_person.father_name, found_person.father_surname,found_person.father_id, found_person.spouse_id, found_person.gender))
        clear_fields()  # Clear
    else:
        print("Person with ID {} not found.".format(person_id))

def update_treeview():
    family_tree = load_family_tree()
    if family_tree:
        for unique_id, data in family_tree.items():
            person = Person(unique_id, data["name"], data["surname"], data["mother_name"], data["mother_surname"],
                            data["mother_id"], data["father_name"], data["father_surname"], data["father_id"], 0)
            Person.all.append(person)
            table.insert('', 'end', values=(
                unique_id,
                data["name"],
                data["surname"],
                data["mother_name"],
                data["mother_surname"],
                data["mother_id"],
                data["father_name"],
                data["father_surname"],
                data["father_id"]
            ))
"""

if __name__ == "__main__":
    main()