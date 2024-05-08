from customtkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os  # βιβλιοθήκη os ή glob για να βρώ όλα τα αρχεία με μια συγκεκριμένη επέκταση (π.χ., JSON) σε έναν φάκελο.

global checkbox_male_var, checkbox_female_var, file_name

# Συνάρτηση για να επιλέξω αρχείο από το cur dir από ένα `Listbox`
def choose_file(json_files):
    popup = tk.Toplevel()
    popup.title("Menu Επιλογής")
    # Ορίζω το μέγεθος του παραθύρου
    width = 400  # Πλάτος σε pixels
    height = 400  # Ύψος σε pixels

    # Υπολογισμός για κεντράρισμα
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # κεντράρισμα
    popup.geometry(f"{width}x{height}+{x}+{y}")

    # Δημιουργία στυλ και προσθήκη ετικέτας
    style = ttk.Style()
    style.configure("Custom.TLabel", font=("Arial", 14), foreground="black", background="light blue")

    label = ttk.Label(popup, text="Επιλογή αρχείου ή δημιουργία νέου", style="Custom.TLabel")
    label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)  # Προσθέτω padding για περισσότερο χώρο

    # Προσθέτω ενα Listbox για να επιλέξει ο χρηστης αρχείο για άνοιγμα
    listbox = tk.Listbox(popup, selectmode=tk.SINGLE, font=("Arial", 14))
    for file in json_files:
        listbox.insert(tk.END, file)

    # Προσθέτω και την επιλογή "Δημιουργία νέου αρχείου"
    listbox.insert(tk.END, "Δημιουργία νέου αρχείου")

    listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)  # Προσθέτω περισσότερο padding
    selected_file = {"file_name": None}

    # Συνάρτηση για το κουμπί "OK"
    def on_ok():
        selected = listbox.curselection()

        if selected:
            selected_item = listbox.get(selected[0])

            if selected_item == "Δημιουργία νέου αρχείου":
                new_file_name = simpledialog.askstring(
                    "Create New File",
                    "Δώστε όνομα για νέο αρχείο:"
                )
                if new_file_name:
                    # Χρησιμοποιω το os.getcwd() για να λάβω τον τρέχοντα κατάλογο
                    current_dir = os.getcwd()
                    new_file_path = os.path.join(current_dir, new_file_name + ".json")
                    with open(new_file_path, "w") as f:
                        json.dump({}, f, indent=4)
                    selected_file["file_name"] = new_file_path

            else:
            # Χρησιμοποιώ τον τρέχοντα κατάλογο για την επιλογή του υπάρχοντος αρχείου
                current_dir = os.getcwd()
                selected_file["file_name"] = os.path.join(current_dir, selected_item)

            popup.destroy() #Κλείσιμο popup

        else:
            print("No file selected")

    button_ok = tk.Button(popup, text="OK", command=on_ok)
    button_ok.pack(padx=5, pady=5)

    # Περιμένω για το κλείσιμο του παραθύρου
    popup.wait_window(popup)

    # Επιστρέφω το επιλεγμένο αρχειο
    return selected_file["file_name"]

# Επιλογή ή δημιουργία αρχείου
def select_or_create_file():
    # Χρησιμοποιώ τον τρέχοντα κατάλογο
    current_dir = os.getcwd()

   # Εύρεση όλων των αρχείων JSON στον φάκελο
    json_files = [f for f in os.listdir(current_dir) if f.endswith(".json")]

    # Προτρεπω στον χρήστη να επιλέξει αρχείο ή να δημιουργήσει νέο
    file_name = choose_file(json_files)

    if file_name:
        print(f"Selected file: {file_name}")
        return file_name
    else:
        print("No file selected or created.")  # Εμφάνιση μηνύματος αν δεν επιλεγεί αρχείο
        return None

root = tk.Tk()  # Δημιουργία παραθύρου Tkinter για τo διαλogo
root.withdraw()  # Απόκρυψη του κύριου παραθύρου

file_path = select_or_create_file()  # Επιλογή ή δημιουργία αρχείου
print(file_path)

if file_path:
    try:
        with open(file_path, "r") as f:
            family_tree = json.load(f)
            print(f"Φόρτωση family tree από {file_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON.")
else:
    print("Δεν επιλέχθηκε αρχείο ούτε δημιουργήθηκε νέο.")

class Person:
    all = []
    unique_id_counter = 0

    def __init__(self, name, surname, date_of_birth=None, gender=None, date_of_death=None, mother_name=None,
                 mother_surname=None,
                 mother_id=None, father_name=None, father_surname=None, father_id=None, spouse_id=None):
        self.unique_id = Person.unique_id_counter
        Person.unique_id_counter += 1
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
        # self.spouse = None  **τα χρειαζόμαστε;
        # self.generation = None
        # self.own_union = None

        Person.all.append(self)



def clear_fields():
    # Καθαρίζει όλα τα πεδία
    entry_name.delete(0, 'end')
    entry_surname.delete(0, 'end')
    entry_date.delete(0, 'end')
    entry_id.delete(0, 'end')
    entry_death.delete(0, 'end')
    entry_mother_name.delete(0, 'end')
    entry_mother_surname.delete(0, 'end')
    entry_mother_id.delete(0, 'end')
    entry_father_name.delete(0, 'end')
    entry_father_surname.delete(0, 'end')
    entry_father_id.delete(0, 'end')
    entry_spouse_id.delete(0, 'end')

    checkbox_male.deselect()
    checkbox_female.deselect()


# Συνάρτηση για να εμφανίζεται ένα pop-up (μετά την αποθήκευση αλλαγών) που θα κλείνει μετά από λίγο
def show_popup(message, duration):
    # Δημιουργία ενός Toplevel παραθύρου
    popup = tk.Toplevel()
    popup.title(" ")

    # Προσθήκη ετικέτας με το μήνυμα
    label = tk.Label(popup, text=message, font=("Arial", 14))
    label.pack(pady=20, padx=20)

    # Αυτόματη καταστροφή του pop-up μετά από 'duration' χιλιοστά του δευτερολέπτου
    popup.after(duration, popup.destroy)

    # Τοποθέτηση του pop-up στο κέντρο της κύριας οθόνης
    popup.geometry("+%d+%d" % (popup.winfo_screenwidth() // 2, popup.winfo_screenheight() // 2))


def load_family_tree():
    try:
        with open(file_path, "r") as f:
            family_tree = json.load(f)
            print("Το αρχείο άνοιξε")
        return family_tree
    except FileNotFoundError:
        print("Το Family tree αρχείο δεν βρέθηκε.")
        return None


def save_family_tree(family_tree):
    try:
        with open(file_path, "w") as f:
            json.dump(family_tree, f, indent=4)
            show_popup("Επιτυχημένη αποθήκευση!", duration=2000)
    except Exception as e:
        print("¨Πρόβλημα στην αποθήκευση του αρχείου", e)


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
    spouse_id = entry_spouse_id.get()

    # Φτιάχνω νέο άτομο από τα δεδομένα που έχω συλλέξει
    new_person = Person(name, surname)
    new_person.name = name
    new_person.surname = surname
    new_person.date_of_birth = date_of_birth
    new_person.gender = gender
    new_person.date_of_death = date_of_death
    new_person.mother_name = mother_name
    new_person.mother_surname = mother_surname
    new_person.mother_id = mother_id
    new_person.father_name = father_name
    new_person.father_surname = father_surname
    new_person.father_id = father_id
    new_person.spouse_id = spouse_id

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
        "gender": gender,
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
    save_family_tree(family_tree)
    clear_fields()

    # Προσθέτει το νέο άτομο στο treeview-gui table
    unique_id = Person.unique_id_counter

    table.insert('', 'end', values=(
        unique_id,
        data["name"],
        data["surname"],
        data["mother_name"],
        data["mother_surname"],
        data["mother_id"],
        data["father_name"],
        data["father_surname"],
        data["father_id"],
        data["date_of_birth"],
        data["date_of_death"],
        data["spouse_id"]))


    """# Eνημέρωsη σχέσης παιδιού-γονέα
    for person in Person.all:
        if person.unique_id == mother_id:
            person.children.append(new_person)
        if person.unique_id == father_id:
            person.children.append(new_person)"""

#TODO
def view_family_tree():
    pass

def load_additional_data(unique_id):
    with open(file_path, "r") as file:
        family_tree = json.load(file)
        if str(unique_id) in family_tree:
            return family_tree[str(unique_id)]
    return {}


# Kαλείται κάθε φορά που γίνεται μια επιλογή στο Treeview. Η μεταβλητή event περιέχει πληροφορίες για το συμβάν
def on_treeview_select(event):
    selected_item = table.selection()  # επιστρέφει μια λίστα με τα επιλεγμένα στοιχεία στο Treeview

    item_values = table.item(selected_item[0],
                             "values")  # Λαμβάνει τις τιμές του πρώτου επιλεγμένου στοιχείου. Τα "values" είναι μια πλειάδα που περιέχει τα δεδομένα του επιλεγμένου στοιχείου
   #TODO Αμυντικός προγραμματισμός
    if len(item_values) < 3:  # Πρέπει να υπάρχει τουλάχιστον ID, Name, Surname
        print("Error: Δεν υπάρχουν τα βασικά στοιχεία !")
        return

    # Καθαρισμός πεδίων πριν την ενημέρωση
    clear_fields()
    unique_id = item_values[0]

    # Ανάκτηση πρόσθετων δεδομένων από το JSON(επειδη δε υπάρχουν ολα τα δεδομένα στο treeview)
    additional_data = load_additional_data(unique_id)

    # Για κάθε πεδίο, ελέγχω αν υπάρχει τιμή και εισάγω την προεπιλεγμένη αν χρειάζεται
    def insert_value(entry, value):
        # Εάν η τιμή δεν είναι κενή ή None, την εισάγω
        if value is not None and value != "":
            entry.insert(0, value)
        else:
            entry.insert(0, "")  # Χρησιμοποιώ το κενό ως προεπιλεγμένη τιμή

    # Γεμίζω τα 3 βασικά πεδία

    insert_value(entry_id, item_values[0])
    insert_value(entry_name, item_values[1])
    insert_value(entry_surname, item_values[2])

    # Ανακτώ τα πρόσθετα δεδομένα από το JSON
    insert_value(entry_date, additional_data.get("date_of_birth", ""))
    insert_value(entry_death, additional_data.get("date_of_death", ""))
    insert_value(entry_mother_name, additional_data.get("mother_name", ""))
    insert_value(entry_mother_surname, additional_data.get("mother_surname", ""))
    insert_value(entry_mother_id, additional_data.get("mother_id", ""))
    insert_value(entry_father_name, additional_data.get("father_name", ""))
    insert_value(entry_father_surname, additional_data.get("father_surname", ""))
    insert_value(entry_father_id, additional_data.get("father_id", ""))
    insert_value(entry_spouse_id, additional_data.get("spouse_id", ""))

    # Ενημέρωση των checkboxes με βάση το gender
    gender_value = additional_data.get("gender", "")

    # Ξετσεκάρισμα όλων των checkboxes
    checkbox_male.deselect()
    checkbox_female.deselect()

    # Τσεκάρισμα με βάση το gender
    if gender_value == "0":
        checkbox_male.select()  # Τσεκάρισμα του Male
    elif gender_value == "1":
        checkbox_female.select()  # Τσεκάρισμα του Female


def update_person():
    # Παίρνω το ID του ατόμου που θα ενημερώσω
    try:
        print(f"entry_id.get =  {entry_id.get()}")
        person_id = int(entry_id.get())
    except ValueError:
        print("Invalid ID")
        return

    # Ψαχνω το ατομο με το συγκεκριμένο ID
    found_person = None
    for person in Person.all:
        if person.unique_id == person_id:
            found_person = person
            break

    if found_person:
        # Ενημέρωση των πεδίων του αντικειμένου `Person`
        found_person.name = entry_name.get()
        found_person.surname = entry_surname.get()
        found_person.date_of_birth = entry_date.get()
        found_person.gender = "0" if checkbox_male_var.get() else "1"
        found_person.date_of_death = entry_death.get()
        found_person.mother_name = entry_mother_name.get()
        found_person.mother_surname = entry_mother_surname.get()
        found_person.mother_id = entry_mother_id.get()
        found_person.father_name = entry_father_name.get()
        found_person.father_surname = entry_father_surname.get()
        found_person.father_id = entry_father_id.get()
        found_person.spouse_id = entry_spouse_id.get()

        # Ενημέρωση του Treeview
        selected_item = table.selection()[0]
        table.item(selected_item, values=(found_person.unique_id, found_person.name, found_person.surname,
                                          found_person.mother_name, found_person.mother_surname,
                                          found_person.mother_id, found_person.father_name, found_person.father_surname,
                                          found_person.father_id, person.date_of_birth, found_person.date_of_death, found_person.spouse_id))
        # Φόρτωση του οικογενειακού δέντρου
        family_tree = load_family_tree()
        if family_tree is not None:
            # Ενημέρωση του αντίστοιχου λεξικού με τα νέα δεδομένα
            family_tree[str(found_person.unique_id)] = {
                "name": found_person.name,
                "surname": found_person.surname,
                "date_of_birth": found_person.date_of_birth,
                "gender": found_person.gender,
                "date_of_death": found_person.date_of_death,
                "mother_name": found_person.mother_name,
                "mother_surname": found_person.mother_surname,
                "mother_id": found_person.mother_id,
                "father_name": found_person.father_name,
                "father_surname": found_person.father_surname,
                "father_id": found_person.father_id,
                "spouse_id": found_person.spouse_id,
            }

            # Αποθήκευση των αλλαγών στο αρχείο JSON
            save_family_tree(family_tree)


def update_treeview():
    family_tree = load_family_tree()
    if family_tree:
        for unique_id, data in family_tree.items():
            person = Person(data["name"], data["surname"], data["mother_name"], data["mother_surname"],
                            data["mother_id"], data["father_name"], data["father_surname"], data["father_id"])
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
                data["father_id"],
                data["date_of_birth"],
                data["date_of_death"],
                data["spouse_id"]))


#TODO Ελεγχος όταν διαγραφεται ατομο από τη μεση του δενδρου ** Μενει αχρησιμοποιητο το ID
def delete_person():
    selected_item = table.selection()  # Παίρνω το επιλεγμένο άτομο
    if not selected_item:
        print("Δεν εχει επιλεγεί άτομο.")
        return

    item_id = table.item(selected_item)["values"][0]  # Βρίσκω το Unique ID
    table.delete(selected_item)  # Διαγράφω από το Treeview

    # Αφαιρώ το person από τη λιστα
    Person.all = [p for p in Person.all if p.unique_id != item_id]

    # Φορτώνω το τρέχον family tree
    family_tree = load_family_tree()
    if family_tree and str(item_id) in family_tree:
        del family_tree[str(item_id)]  # Αφαίρεση από το δενδρο

    # Σώζω το ανανεωμένο family tree
    save_family_tree(family_tree)
    clear_fields()


app = CTk()

app.geometry("1500x900")
label_title = CTkLabel(master=app, text=" Genealogy Tree", font=("Arial", 25), text_color="black")
label_title.place(relx=0.5, rely=0.05, anchor="center")
set_appearance_mode("light")

middle = tk.Frame(app, pady=5, highlightthickness=3, height=40, width=200)
middle.pack(side=tk.LEFT, fill='x', expand=True)  # επέκταση στο πλάτος

# Προσθέστε ένα στοιχείο στο `middle` για δοκιμή
label = tk.Label(middle, text="Μέλη Οικογένειας", bg='lightgray')
label.pack()

checkbox_male_var = tk.StringVar()
checkbox_female_var = tk.StringVar()

# ΠΑΝΩ ΜΕΡΟΣ - LABELS για INPUT & TEXT ENTRY
label_name = CTkLabel(master=app, text=" Name :", font=("Arial", 18), text_color="black")
label_name.place(relx=0.02, rely=0.1, anchor="nw")
entry_name = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                      width=270)
entry_name.place(relx=0.065, rely=0.1, anchor="nw")

label_surname = CTkLabel(master=app, text=" Surname :", font=("Arial", 18), text_color="black")
label_surname.place(relx=0.25, rely=0.1, anchor="nw")
entry_surname = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                         width=270)
entry_surname.place(relx=0.32, rely=0.1, anchor="nw")

label_date = CTkLabel(master=app, text=" Date of Birth :", font=("Arial", 18), text_color="black")
label_date.place(relx=0.52, rely=0.1, anchor="nw")
entry_date = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                      width=190)
entry_date.place(relx=0.61, rely=0.1, anchor="nw")

label_id = CTkLabel(master=app, text=" ID :", font=("Arial", 18), text_color="grey")
label_id.place(relx=0.02, rely=0.15, anchor="nw")
entry_id = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                    width=230)
entry_id.place(relx=0.053, rely=0.15, anchor="nw")

label_mother_name = CTkLabel(master=app, text=" Mother's name :", font=("Arial", 18), text_color="black")
label_mother_name.place(relx=0.02, rely=0.20, anchor="nw")
entry_mother_name = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                             width=206)
entry_mother_name.place(relx=0.11, rely=0.20, anchor="nw")

label_mother_surname = CTkLabel(master=app, text=" Mother's surname :", font=("Arial", 18), text_color="black")
label_mother_surname.place(relx=0.25, rely=0.20, anchor="nw")
entry_mother_surname = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black",
                                fg_color="white", width=210)
entry_mother_surname.place(relx=0.36, rely=0.20, anchor="nw")

label_mother_id = CTkLabel(master=app, text=" Mother's (ID) :", font=("Arial", 18), text_color="black")
label_mother_id.place(relx=0.52, rely=0.20, anchor="nw")
entry_mother_id = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                           width=190)
entry_mother_id.place(relx=0.6, rely=0.20, anchor="nw")

label_death = CTkLabel(master=app, text=" Date of Death :", font=("Arial", 18), text_color="black")
label_death.place(relx=0.52, rely=0.15, anchor="nw")
entry_death = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                       width=190)
entry_death.place(relx=0.61, rely=0.15, anchor="nw")

label_father_name = CTkLabel(master=app, text=" Father's name :", font=("Arial", 18), text_color="black")
label_father_name.place(relx=0.02, rely=0.25, anchor="nw")
entry_father_name = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                             width=206)
entry_father_name.place(relx=0.11, rely=0.25, anchor="nw")

label_father_surname = CTkLabel(master=app, text=" Father's surname :", font=("Arial", 18), text_color="black")
label_father_surname.place(relx=0.25, rely=0.25, anchor="nw")
entry_father_surname = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black",
                                fg_color="white", width=210)
entry_father_surname.place(relx=0.36, rely=0.25, anchor="nw")

label_father_id = CTkLabel(master=app, text=" Father's (ID) :", font=("Arial", 18), text_color="black")
label_father_id.place(relx=0.52, rely=0.25, anchor="nw")
entry_father_id = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                           width=190)
entry_father_id.place(relx=0.6, rely=0.25, anchor="nw")

label_spouse_id = CTkLabel(master=app, text=" Spouse (ID) :", font=("Arial", 18), text_color="black")
label_spouse_id.place(relx=0.02, rely=0.30, anchor="nw")
entry_spouse_id = CTkEntry(master=app, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white",
                           width=210)
entry_spouse_id.place(relx=0.11, rely=0.30, anchor="nw")

# CHECKBOXES
checkbox_male = CTkCheckBox(master=app, text="Male", font=("Arial", 12), fg_color="grey", bg_color="Light grey",
                            variable=checkbox_male_var)
checkbox_male.place(relx=0.25, rely=0.15, anchor="nw")
checkbox_female = CTkCheckBox(master=app, text="Female", font=("Arial", 12), fg_color="grey", bg_color="light grey",
                              variable=checkbox_female_var)
checkbox_female.place(relx=0.33, rely=0.15, anchor="nw")

# Buttons
btn_add = CTkButton(master=app, text="Προσθήκη νέου ατόμου", corner_radius=32, command=add_person,
                    fg_color="light blue", hover_color="blue", border_color="blue", text_color="black",
                    border_width=4, width=20, height=50)
btn_add.place(relx=0.13, rely=0.8, anchor="ne")

btn_treeview = CTkButton(master=app, text="Εμφάνιση δεδομένων", corner_radius=32, command=update_treeview,
                         fg_color="light blue", hover_color="blue", border_color="blue", text_color="black",
                         border_width=4, width=20, height=50)
btn_treeview.place(relx=0.30, rely=0.8, anchor="ne")

btn_view_family_tree = CTkButton(master=app, text="Εμφάνιση δένδρου", corner_radius=32, command=view_family_tree,
                                 fg_color="light blue", hover_color="blue", border_color="blue", text_color="black",
                                 border_width=5, width=20, height=50)
btn_view_family_tree.place(relx=0.45, rely=0.8, anchor="ne")

btn_clear = CTkButton(master=app, text="Καθαρισμός πεδίων", corner_radius=32, command=clear_fields,
                      fg_color="light blue", hover_color="blue", border_color="blue", text_color="black",
                      border_width=2, width=20, height=50)
btn_clear.place(relx=0.6, rely=0.8, anchor="ne")

btn_update = CTkButton(master=app, text="Ενημέρωση στοιχείων ατόμου", corner_radius=32, command=update_person,
                       fg_color="light blue", hover_color="blue", border_color="blue", text_color="black",
                       border_width=2, width=20, height=50)
btn_update.place(relx=0.80, rely=0.8, anchor="ne")

btn_delete = CTkButton(master=app, text="Διαγραφή ατόμου", corner_radius=32, command=delete_person,
                       fg_color="light blue", hover_color="blue", border_color="blue", text_color="black",
                       border_width=2, width=20, height=50)
btn_delete.place(relx=0.95, rely=0.8, anchor="ne")

# treeview
table = ttk.Treeview(middle, columns=(
"Unique ID", "Name", "Surname", "Mother_Name", "Mother_Surname", "Mother ID", "Father_Name", "Father_Surname",
"Father ID", "Date Of Birth", "Date Of Death", "Spouse's ID"), show='headings')
# Αλλαγή μεγέθους γραμματοσειράς στην επικεφαλίδα
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 12))

# Αλλαγή μεγέθους γραμματοσειράς στα περιεχόμενα
style.configure("Treeview", font=('Arial', 11), anchor=tk.CENTER)

table.heading("#1", text='Unique_id', anchor=tk.CENTER,)
table.heading("#2", text='First name', anchor=tk.CENTER)
table.heading("#3", text='Surname', anchor=tk.CENTER)
table.heading("#4", text="Mother's Name", anchor=tk.CENTER)
table.heading("#5", text="Mother's Surname", anchor=tk.CENTER)
table.heading("#6", text="Mother's ID", anchor=tk.CENTER)
table.heading("#7", text="Father's Name", anchor=tk.CENTER)
table.heading("#8", text="Father's Surname", anchor=tk.CENTER)
table.heading("#9", text="Father's ID", anchor=tk.CENTER)

table.heading("#10", text='Date Of Birth', anchor=tk.CENTER)
table.column("#10", anchor=tk.CENTER, stretch=True, width=130)
table.heading("#11", text='Date Of Death', anchor=tk.CENTER)
table.column("#11", anchor=tk.CENTER, stretch=True, width=130)
table.heading("#12", text="Spouse's ID", anchor=tk.CENTER)
table.column("#12", anchor=tk.CENTER, stretch=True, width=130)

table.column("#1", anchor=tk.CENTER, stretch=True, width=80)
table.column("#2", anchor=tk.CENTER, stretch=True, width=120)
table.column("#3", anchor=tk.CENTER, stretch=True, width=150)
table.column("#4", anchor=tk.CENTER, stretch=True, width=120)
table.column("#5", anchor=tk.CENTER, stretch=True, width=150)
table.column("#6", anchor=tk.CENTER, stretch=True, width=80)
table.column("#7", anchor=tk.CENTER, stretch=True, width=120)
table.column("#8", anchor=tk.CENTER, stretch=True, width=150)
table.column("#9", anchor=tk.CENTER, stretch=True, width=80)
table.pack(fill='both', expand=True) #το Treeview επεκτείνεται ώστε να γεμίζει το διαθέσιμο χώρο για να έχουν οι στήλες τον απαραίτητο χώρο.

# Η συνάρτηση on_treeview_select συνδέεται με το συμβάν επιλογής του Treeview
table.bind("<<TreeviewSelect>>", on_treeview_select)

app.mainloop()