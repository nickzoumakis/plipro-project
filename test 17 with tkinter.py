from customtkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import simpledialog
import json



class Person:
    all = []
    unique_id_counter = 1

    def __init__(self, name, surname, date_of_birth=None, gender=None, date_of_death=None,  mother_name=None, mother_surname=None, father_name=None,
                 father_surname=None, mother_id=None, father_id=None, spouse_id=None):
        self.name = name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.date_of_death = date_of_death
        self.mother_name = mother_name
        self.mother_surname = mother_surname
        self.mother_id = mother_id
        self.father_name = father_name
        self.father_surname = father_surname
        self.father_id = father_id
        self.spouse_id = spouse_id
        self.children = []
        self.parents = []
        self.siblings = []
        self.spouse = None
        self.generation = None
        self.own_union = None
        self.unique_id = Person.unique_id_counter
        #Person.unique_id_counter += 1
        print("PERSON LENGTH sto init", len(Person.all))
        #Person.all.append(self)
        #print("PERSON LENGTH sto init", len(Person.all))

def clear_fields():
    # Καθαρίζει όλα τα πεδία
    entry_name.delete(0, 'end')
    entry_surname.delete(0, 'end')
    entry_date.delete(0, 'end')
    entry_id.delete(0, 'end')
    entry_mother_name.delete(0, 'end')
    entry_mother_surname.delete(0, 'end')
    entry_mother_id.delete(0, 'end')
    entry_father_name.delete(0, 'end')
    entry_father_surname.delete(0, 'end')
    entry_father_id.delete(0, 'end')
    entry_spouse.delete(0, 'end')
    entry_death.delete(0, 'end')
    # Ξετσεκάρει τα checkboxes
    global checkbox_male_var, checkbox_female_var
    checkbox_male_var.set("0")
    checkbox_female_var.set("0")

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


def add_person():
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

    # Φτιάχνω νέο άτομο από τα δεδομένα που έχω συλλέξει
    new_person = Person(name,surname)
    new_person.name=name
    new_person.surname = surname
    new_person.date_of_birth = date_of_birth
    new_person.gender = gender
    new_person.date_of_death = date_of_death
    new_person.mother_name= mother_name
    new_person.mother_surname= mother_surname
    new_person.mother_id = mother_id
    new_person.father_name=father_name
    new_person.father_surname=father_surname
    new_person.father_id = father_id
    new_person.spouse_id = spouse_id

    print("Added New Person:")
    print("Name:", new_person.name)
    print("Surname:", new_person.surname)
    print("gender:", new_person.gender)
    print("die:", new_person.date_of_death)
    print("mother Name:", new_person.mother_name)
    print("mother Surname:", new_person.mother_surname)
    print("mother id:", new_person.mother_id)
    print("father name:", new_person.father_name)
    print("father Surname:", new_person.father_surname)
    print("father id:", new_person.father_id)
    print("spouse id:", new_person.spouse_id)

    print("PERSON LENGTH before adding:", len(Person.all))
    Person.all.append(new_person)
    print("PERSON LENGTH after adding:", len(Person.all))

    # φορτωνει το αρχικο δεντρο, αν δεν υπαρχει αρχικοποιει ενα κενο
    family_tree = load_family_tree()
    if family_tree is None:
        family_tree = {}
    if family_tree:
        max_id = max(int(key) for key in family_tree.keys())
        Person.unique_id_counter = max_id + 1
        print("max_id", max_id)
        print("STO All Persons:")
        for person in Person.all:
            print(person.unique_id, person.name, person.surname)

    # Ενημέρωση δενδρου με το νέο άτομο
    family_tree[Person.unique_id_counter] = {
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

    # Eνημέρωαη σχέσης παιδιού-γονέα
    for person in Person.all:
        if person.unique_id == mother_id:
            person.children.append(new_person)
        if person.unique_id == father_id:
            person.children.append(new_person)

    # Προσθέτει το νέο άτομο στο treeview-gui table
    unique_id = Person.unique_id_counter
    table.insert('', 'end', values=(
        unique_id, name, surname, date_of_birth, date_of_death, mother_id, father_id, spouse_id, gender))

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



app = CTk()
#frame = CTkFrame(master=app,bg_color="white", border_color="grey", border_width=2, height=200, width=200)
#frame.pack()
app.geometry("1500x900")
label_title= CTkLabel(master=app, text=" Genealogy Tree", font=("Arial", 25), text_color="black")
label_title.place(relx=0.5, rely=0.05, anchor="center")
set_appearance_mode("light")

middle = tk.Frame(app, pady=10.5, highlightthickness=2, height=30, width=20)
middle.pack(side = LEFT)
checkbox_male_var = tk.StringVar()
checkbox_female_var = tk.StringVar()

# img= Image.open("photo.png")
#LABELS FOR INPUT & TEXT ENTRY
label_name= CTkLabel(master=app, text=" Name :", font=("Arial", 18), text_color="black")
label_name.place(relx=0.02, rely=0.1, anchor="nw")
entry_name= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=270)
entry_name.place(relx=0.065, rely=0.1, anchor="nw")

label_surname= CTkLabel(master=app, text=" Surname :", font=("Arial", 18), text_color="black")
label_surname.place(relx=0.25, rely=0.1, anchor="nw")
entry_surname= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=270)
entry_surname.place(relx=0.32, rely=0.1, anchor="nw")

label_date= CTkLabel(master=app, text=" Date of Birth :", font=("Arial", 18), text_color="black")
label_date.place(relx=0.52, rely=0.1, anchor="nw")
entry_date= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_date.place(relx=0.61, rely=0.1, anchor="nw")

label_id= CTkLabel(master=app, text=" ID :", font=("Arial", 18), text_color="grey")
label_id.place(relx=0.02, rely=0.15, anchor="nw")
entry_id= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=230)
entry_id.place(relx=0.053, rely=0.15, anchor="nw")

label_mother_name= CTkLabel(master=app, text=" Mother's name :", font=("Arial", 18), text_color="black")
label_mother_name.place(relx=0.02, rely=0.20, anchor="nw")
entry_mother_name= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=206)
entry_mother_name.place(relx=0.11, rely=0.20, anchor="nw")

label_mother_surname= CTkLabel(master=app, text=" Mother's surname :", font=("Arial", 18), text_color="black")
label_mother_surname.place(relx=0.25, rely=0.20, anchor="nw")
entry_mother_surname= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
entry_mother_surname.place(relx=0.36, rely=0.20, anchor="nw")

label_mother_id= CTkLabel(master=app, text=" Mother's (ID) :", font=("Arial", 18), text_color="black")
label_mother_id.place(relx=0.52, rely=0.20, anchor="nw")
entry_mother_id= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_mother_id.place(relx=0.6, rely=0.20, anchor="nw")

label_death= CTkLabel(master=app, text=" Date of Death :", font=("Arial", 18), text_color="black")
label_death.place(relx=0.52, rely=0.15, anchor="nw")
entry_death= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_death.place(relx=0.61, rely=0.15, anchor="nw")

label_father_name= CTkLabel(master=app, text=" Father's name :", font=("Arial", 18), text_color="black")
label_father_name.place(relx=0.02, rely=0.25, anchor="nw")
entry_father_name= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=206)
entry_father_name.place(relx=0.11, rely=0.25, anchor="nw")

label_father_surname= CTkLabel(master=app, text=" Father's surname :", font=("Arial", 18), text_color="black")
label_father_surname.place(relx=0.25, rely=0.25, anchor="nw")
entry_father_surname= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
entry_father_surname.place(relx=0.36, rely=0.25, anchor="nw")

label_father_id= CTkLabel(master=app, text=" Father's (ID) :", font=("Arial", 18), text_color="black")
label_father_id.place(relx=0.52, rely=0.25, anchor="nw")
entry_father_id= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_father_id.place(relx=0.6, rely=0.25, anchor="nw")

label_spouse= CTkLabel(master=app, text=" Spouse (ID) :", font=("Arial", 18), text_color="black")
label_spouse.place(relx=0.02, rely=0.30, anchor="nw")
entry_spouse= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
entry_spouse.place(relx=0.11, rely=0.30, anchor="nw")



#CHECKBOXES
checkbox_male = CTkCheckBox(master=app, text="Male", font=("Arial", 12), fg_color="grey", bg_color="Light grey", variable=checkbox_male_var)
checkbox_male.place(relx=0.25, rely=0.15, anchor="nw")
checkbox_female = CTkCheckBox(master=app, text="Female", font=("Arial", 12), fg_color="grey", bg_color="light grey", variable=checkbox_female_var)
checkbox_female.place(relx=0.33, rely=0.15, anchor="nw")


#Buttons
btn_add = CTkButton(master=app, text="Προσθήκη νέου ατόμου", corner_radius=32, command=add_person,
                    fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                    border_width=4, width=20, height=50)
btn_add.place(relx=0.13, rely=0.8, anchor="ne")

btn_treeview = CTkButton(master=app, text="Εμφάνιση δεδομένων", corner_radius=32, command=update_treeview,
                       fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                       border_width=4, width=20, height=50)
btn_treeview.place (relx=0.30, rely=0.8, anchor="ne")

btn_clear = CTkButton(master=app, text="Καθαρισμός πεδίων", corner_radius=32, command=clear_fields,
                       fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                       border_width=2, width=20, height=50)
btn_clear.place (relx=0.45, rely=0.8, anchor="ne")

btn_search = CTkButton(master=app, text="Aναζήτηση ατόμου", corner_radius=32, command=search_person,
                       fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                       border_width=2, width=20, height=50)
btn_search.place(relx=0.6, rely=0.8, anchor="ne")

btn_update = CTkButton(master=app, text="Ενημέρωση στοιχείων ατόμου", corner_radius=32, command=update_person,
                       fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                       border_width=2, width=20, height=50)
btn_update.place(relx=0.80, rely=0.8, anchor="ne")

btn_delete = CTkButton(master=app, text="Διαγραφή ατόμου", corner_radius=32,
                       fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                       border_width=2, width=20, height=50)
btn_delete.place(relx=0.95, rely=0.8, anchor="ne")



# treeview
table = ttk.Treeview(middle, columns=("Unique ID", "Name", "Surname", "Mother_Name", "Mother_Surname", "Mother ID", "Father_Name", "Father_Surname", "Father ID"),
                     show='headings')
# Change font size of the headings
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12))

# Change font size of the content
style.configure("Treeview", font=('Arial', 10), anchor=tk.CENTER)

table.heading("#1", text='Unique_id',  anchor=tk.CENTER)
table.column("#1", width=140)
table.heading("#2", text='First name', anchor=tk.CENTER)
table.heading("#3", text='Surname', anchor=tk.CENTER)
table.column("#3", width=190)
table.heading("#4", text="Mother's Name", anchor=tk.CENTER)
table.heading("#5", text="Mother's Surname", anchor=tk.CENTER)
table.heading("#6", text="Mother's ID", anchor=tk.CENTER)
table.heading("#7", text="Father's Name", anchor=tk.CENTER)
table.heading("#8", text="Father's Surname", anchor=tk.CENTER)
table.heading("#9", text="Father's ID", anchor=tk.CENTER)
#table.heading("#5", text='Date Of Birth', anchor=tk.W)
#table.heading("#6", text='Date Of Death', anchor=tk.W)
#table.heading("#10", text="Spouse's ID", anchor=tk.W)

table.pack(fill='both', expand=True)
app.mainloop()
