"""Αντικειμενοστραφής υλοποίηση για το interface"""
from PygraphvizTree import Person, Graph
from pathlib import Path
import pygraphviz as pgv
from PIL import Image, ImageTk
from json import load
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import simpledialog
import json


class MainApp:
    def __init__(self):
        # TODO: να ελέγχεται ο φάκελος data στο parent directory και αν περιέχει Json αρχεία να εμφανίζεται παράθυρο που θα ζητάει από το χρήστη αν θέλει να ανοίξει κάποιο από αυτά ή να φτιάξει νέο δέντρο
        #^^ σε αυτήν την περίπτωση, αν επιλέξει json , το self.family_data δε θα είναι κενό dict αλλά path στο json και η Graph θα κληθεί με την παράμετρο is_path=True
        # βρίσκουμε αν υπάρχουν json αρχεία στο φάκελο data
        data_path = Path.cwd().parent / 'data'
        json_files = [file for file in data_path.glob("*.json")]
        # κενό αρχικά string για το όνομα των αρχείων που θα αποθηκευτούν
        self.file_name = ""
        # αρχικοποίηση κενού dict που θα φιλοξενήσει όλα τα στοιχεία των ατόμων που προσθέτει ο χρήστης
        self.family_data = {}

        # αρχικοποίηση dict συντεταγμένων κόμβων
        self.coordinates = {}
        # κενή αρχικά λίστα με όλα τα Person objects που θα δημιουργηθούν από το Tree class
        self.all = []
        # κενή αρχικά μεταβλητή για το photo object, για αποτροπή του garbage collection και διαγραφή του Image object
        self.pic = None

        # Στοιχεία και γεωμετρία παραθύρου
        self.app = ctk.CTk()
        self.app.geometry("1500x900")
        self.label_title= ctk.CTkLabel(master=self.app, text="Γενεαλογικό Δέντρο", font=("Arial", 25), text_color="black")
        self.label_title.place(relx=0.5, rely=0.05, anchor="center")
        ctk.set_appearance_mode("light")

        self.middle = tk.Frame(self.app, pady=10.5, highlightthickness=2, height=30, width=20)
        self.middle.pack(side = ctk.LEFT)

        # Πεδία εισαγωγής
        self.label_name= ctk.CTkLabel(master=self.app, text="Όνομα: ", font=("Arial", 18), text_color="black")
        self.label_name.place(relx=0.02, rely=0.1, anchor="nw")
        self.entry_name= ctk.CTkEntry(master=self.app, font=("Arial", 18), text_color="black", fg_color="white",width=270)
        self.entry_name.place(relx=0.065, rely=0.1, anchor="nw")

        self.label_surname= ctk.CTkLabel(master=self.app, text="Επώνυμο: ", font=("Arial", 18), text_color="black")
        self.label_surname.place(relx=0.25, rely=0.1, anchor="nw")
        self.entry_surname= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=270)
        self.entry_surname.place(relx=0.32, rely=0.1, anchor="nw")

        self.label_date= ctk.CTkLabel(master=self.app, text="Ημερομηνία γέννησης: ", font=("Arial", 18), text_color="black")
        self.label_date.place(relx=0.52, rely=0.1, anchor="nw")
        self.entry_date= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_date.place(relx=0.61, rely=0.1, anchor="nw")

        self.label_id= ctk.CTkLabel(master=self.app, text="ID: ", font=("Arial", 18), text_color="black")
        self.label_id.place(relx=0.02, rely=0.15, anchor="nw")
        self.entry_id= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=230)
        self.entry_id.place(relx=0.053, rely=0.15, anchor="nw")

        self.label_death= ctk.CTkLabel(master=self.app, text="Ημερομηνία θανάτου: ", font=("Arial", 18), text_color="black")
        self.label_death.place(relx=0.52, rely=0.15, anchor="nw")
        self.entry_death= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_death.place(relx=0.61, rely=0.15, anchor="nw")

        self.label_mother_name= ctk.CTkLabel(master=self.app, text="Όνομα Μητέρας: ", font=("Arial", 18), text_color="black")
        self.label_mother_name.place(relx=0.02, rely=0.20, anchor="nw")
        self.entry_mother_name= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=206)
        self.entry_mother_name.place(relx=0.11, rely=0.20, anchor="nw")

        self.label_mother_surname= ctk.CTkLabel(master=self.app, text="Επώνυμο Μητέρας: ", font=("Arial", 18), text_color="black")
        self.label_mother_surname.place(relx=0.25, rely=0.20, anchor="nw")
        self.entry_mother_surname= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_mother_surname.place(relx=0.36, rely=0.20, anchor="nw")

        self.label_mother_id= ctk.CTkLabel(master=self.app, text="ID Μητέρας: ", font=("Arial", 18), text_color="black")
        self.label_mother_id.place(relx=0.52, rely=0.20, anchor="nw")
        self.entry_mother_id= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_mother_id.place(relx=0.6, rely=0.20, anchor="nw")

        self.label_father_name= ctk.CTkLabel(master=self.app, text="Όνομα Πατέρα: ", font=("Arial", 18), text_color="black")
        self.label_father_name.place(relx=0.02, rely=0.25, anchor="nw")
        self.entry_father_name= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=206)
        self.entry_father_name.place(relx=0.11, rely=0.25, anchor="nw")

        self.label_father_surname= ctk.CTkLabel(master=self.app, text="Επώνυμο Πατέρα: ", font=("Arial", 18), text_color="black")
        self.label_father_surname.place(relx=0.25, rely=0.25, anchor="nw")
        self.entry_father_surname= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_father_surname.place(relx=0.36, rely=0.25, anchor="nw")

        self.label_father_id= ctk.CTkLabel(master=self.app, text="ID Πατέρα: ", font=("Arial", 18), text_color="black")
        self.label_father_id.place(relx=0.52, rely=0.25, anchor="nw")
        self.entry_father_id= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_father_id.place(relx=0.6, rely=0.25, anchor="nw")

        self.label_spouse= ctk.CTkLabel(master=self.app, text="ID Συζύγου: ", font=("Arial", 18), text_color="black")
        self.label_spouse.place(relx=0.02, rely=0.30, anchor="nw")
        self.entry_spouse= ctk.CTkEntry(master=self.app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_spouse.place(relx=0.11, rely=0.30, anchor="nw")

        self.entry_img =  ctk.CTkEntry(master=self.app, placeholder_text= "File path", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_img.place(relx=0.6, rely=0.31, anchor="nw")

        # CHECKBOXES για φύλο
        self.checkbox_male = ctk.CTkCheckBox(master=self.app, text="Άντρας", font=("Arial", 12), hover=True, fg_color="grey", bg_color="Light grey", command=lambda:self.uncheck_other("male"))
        self.checkbox_male.place(relx=0.25, rely=0.15, anchor="nw")
        self.checkbox_female = ctk.CTkCheckBox(master=self.app, text="Γυναίκα", font=("Arial", 12), hover=True, fg_color="grey", bg_color="light grey", command=lambda:self.uncheck_other("female"))
        self.checkbox_female.place(relx=0.33, rely=0.15, anchor="nw")


        # Κουμπιά αλληλεπίδρασης χρήστη, κάθε command οδηγεί σε νέο function του class
        self.btn_add = ctk.CTkButton(master=self.app, text="Προσθήκη νέου ατόμου", corner_radius=32, command=self.add_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=4, width=20, height=50)
        self.btn_add.place(relx=0.13, rely=0.8, anchor="ne")

        # αλλαγή κουμπιού σε 'Δημιουργία Δέντρου' -> περνάει όλα τα άτομα από το family tree dict στο Graph 
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

        self.btn_delete = ctk.CTkButton(master=self.app, text="Διαγραφή ατόμου", corner_radius=32, command=self.delete_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50)
        self.btn_delete.place(relx=0.95, rely=0.8, anchor="ne")

        self.btn_uploadimg = ctk.CTkButton(master=self.app, text="Μεταφόρτωση φωτογραφίας", corner_radius=32, command=self.upload_img,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=15, height=40)
        self.btn_uploadimg.place(relx=0.45, rely=0.30, anchor="nw")

        # treeview
        col_titles = (
            "Κωδικός", 
            "Όνομα", 
            "Επώνυμο", 
            "Όνομα Μητέρας", 
            "Επώνυμο Μητέρας", 
            "Κωδικός Μητέρας", 
            "Όνομα Πατέρα", 
            "Επώνυμο Πατέρα", 
            "Κωδικός Πατέρα")
        
        self.table = ttk.Treeview(self.middle, columns=col_titles, show='headings')
        # Change font size of the headings
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 12))
        # Change font size of the content
        #self.style.configure("Treeview", font=('Arial', 10), anchor=tk.CENTER)

        # Δημιουργία στηλών στο tree view με κεντραρισμένο το κείμενο των entries
        for title in col_titles:
            self.table.heading(title, text=title, anchor='center')
            self.table.column(title, anchor='center')
        # add event: όταν ο χρήστης κάνει κλικ σε κάποιο άτομο στο treeview, τα στοιχεία του να εμφανίζονται στις φόρμες του παραθύρου        
        # η lambda εδώ είναι απαραίτητη, το bind επιστρέφει event από μόνο του ως argument, τη χρησιμοποιούμε για να το απορροφήσουμε και να καλέσουμε τη συνάρτηση που ενδιαφέρει πραγματικά(show items) 
        self.table.bind('<<TreeviewSelect>>', lambda _event:self.show_items())

        # TODO: την πρώτη φορά και κάθε φορά που θα διαλέγει να φτιάξει νέο δέντρο, να ζητείται όνομα για το αρχείο (για την ονοματοδοσία και της εικόνας του γραφήματος και του json)
        self.choose_file(json_files)


    # Συνάρτηση για να επιλέξω αρχείο από το cur dir από ένα `Listbox`
    def choose_file(self, json_files):
        popup = tk.Toplevel(master=self.app)
        popup.attributes("-topmost", True)
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
                        self.file_name = new_file_name

                else:
                # Χρησιμοποιώ τον τρέχοντα κατάλογο για την επιλογή του υπάρχοντος αρχείου
                    self.file_name = selected_item

                popup.destroy() #Κλείσιμο popup

            else:
                print("No file selected")
            
        button_ok = tk.Button(popup, text="OK", command=on_ok)
        button_ok.pack(padx=5, pady=5)

        # Περιμένω για το κλείσιμο του παραθύρου"""
        popup.focus()
        popup.wait_window()

    """απενεργοποιεί το ένα checkbox φύλου εφόσον επιλέγεται το άλλο"""
    def uncheck_other(self, enabled):
        if enabled == "male":
            if self.checkbox_female.get() == 1:
                self.checkbox_female.deselect()
            self.checkbox_male.select()
        elif enabled == "female":
            if self.checkbox_male.get() == 1:
                self.checkbox_male.deselect()
            self.checkbox_female.select()


    """η show_items εμφανίζει στις φόρμες τα στοιχεία (values) κάθε ατόμου όταν γίνεται κλικ σε αυτό στο treeview"""
    # TODO: να μπορεί ο χρήστης να αλλάζει τα στοιχεία και πάτώντας ενημέρωση ατόμου, να ενημερώνεται το family_data dict
    def show_items(self):
        # καθάρισμα αρχικά των πεδίων
        self.clear_fields()
        entries = [self.entry_name,
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
            self.entry_death,
            self.entry_img]
        
        keys = ['name',
                'surname',
                'date_of_birth',
                'id',
                'mother_name',
                'mother_surname',
                'mother_id',
                'father_name',
                'father_surname',
                'father_id',
                'spouse_id', 
                'date_of_death',
                'photo_path']
        # εύρεση των στοιχείων του ατόμου με βάση το id από το family_data dict και όχι από τα selected items του treeview (δεν περιλαμβάνει κενά πεδία)
        selected_item = self.table.selection()
        # διακοπή της συνάρτησης αν δεν έχει επιλεγεί άτομο ή γίνει διαγραφή του επιλεγμένου
        if not selected_item:
            return
        selected_id = str(self.table.item(selected_item)['values'][0])
        for i, (entry, key) in enumerate(zip(entries, keys)):
            if  i == 3:
                # 3o στοιχείο το ID του ατομου, το παίρνουμε κατευθείαν από το selected_id αφού στο dict δεν υπάρχει μέσα στα keys
                entry.insert(0, selected_id)
            else:
                entry.insert(0, self.family_data[selected_id][key])
    

    """add_person: Προσθέτει τα στοιχεία του ατόμου στον πίνακα του παραθύρου και ενημερώνει το dict"""
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
        photo_path = self.entry_img.get()

        # TODO: αμυντικός για μοναδικότητα ID κάθε ατόμου, έγκυρους χαρακτήρες γενικά στα πεδία, να μη μπορεί να εισαχθεί κενό entry στο dict αλλιώς έχω nonetype στο Person list του Graph
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
            "spouse_id": spouse_id,
            "photo_path": photo_path
        }

        # για debugging
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
            ) 
        
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
                    self.entry_death,
                    self.entry_img]:
            entry.delete(0, 'end')
        
        # Ξετσεκάρει τα checkboxes
        for checkbox in [self.checkbox_male, self.checkbox_female]:
            checkbox.deselect()


    """διαγράφει άτομο από το treeview και από το family_data"""
    def delete_person(self):
        selected_item = self.table.selection()  # Get the selected item
        if not selected_item:
            # επιστροφή αν δεν έχει επιλεγεί άτομο
            print("No item selected.")
            return

        item_id = self.table.item(selected_item)["values"][0]  # Βρίσκω το Unique ID
        self.table.delete(selected_item)  # Διαγράφω από το Treeview

        del self.family_data[str(item_id)]  # Αφαίρεση από το family_data
        #debug print
        #print(self.family_data)


    """create_tree: Αποθήκευση γενεαλογικών δεδομένων στο δίσκο. 
    Καλεί το Graph class (απο το module GraphvizTree) και σχεδιάζει εικόνα του δέντρου"""
    def create_tree(self):
        # TODO:ΧΡΕΑΙΖΕΤΑΙ UPDATE ονοματοδοσία json και γραφήματος με βάση το string που εισήγαγε ο χρήστης στο popup
        for i, key in enumerate(self.family_data.keys()):
            if i == 0:
                json_filename = f"{self.family_data[key]['name']}_{self.family_data[key]['surname']}.json"
                # img_filename χωρίς επέκταση αφού στην show της Graph δίνεται σε άλλο όρισμα (format='png')
                img_filename =  f"{self.family_data[key]['name']}_{self.family_data[key]['surname']}"
        data_file_path = Path.cwd().parent / 'data' / json_filename
        img_file_path = Path.cwd().parent / 'graph'

        # dump json στο φάκελο data
        with open(data_file_path, "w") as file:
            json.dump(self.family_data, file, indent=4)

        # δημιουργία γραφήματος και αποθήκευση rendered εικόνας
        graph = Graph(self.family_data)
        graph.show(img_filename, img_file_path)

        # ενημέρωση του coordinates dict με τις συντεταγμένες από το Tree
        self.coordinates = graph.send_coordinates()

        # ενημέρωση της λίστας με τα Person objects
        self.all = graph.send_people()

        # πέρασμα του πλήρους ονόματος μαζί με την επέκταση στην load_image()
        full_img_filename = img_filename + '.png'
        self.load_image(full_img_filename, graph)


    """ load_image: άνοιγμα εικόνας δέντρου σε νέο παράθυρο tkinter """
    def load_image(self, img_filename, graph):
            # ανάθεση στο path
            img_path = Path.cwd().parent / 'graph' / img_filename
            # άνοιγμα εικόνας με PIL
            img = Image.open(img_path)
            # ακριβές μέγεθος εικόνας για τις διαστάσεις του παραθύρου
            dimensions = f'{img.width}x{img.height}'
            # άνοιγμα εικόνας σε νέο παράθυρο tkinter
            # όταν φτιάχνω νέο παράθυρο, ποτέ δεν το ορίζω ως καινούριο tk.Τk() αντικείμενο αλλά σαν TopLevel του master window
            tree_img = ctk.CTkToplevel(self.app)
            tree_img.title("Γενεαλογικό Δέντρο")
            tree_img.geometry(dimensions)
            img = tk.PhotoImage(file=img_path)
            img_label = tk.Label(tree_img, image=img)
            # για όσο τρέχει το παράθυρο του δέντρου, κάνουμε bind το click event στο get_node_info
            tree_img.bind("<Button-1>", lambda event:self.get_node_info(event))
            tree_img.bind("<Motion>", lambda event:self.update_cursor(event, tree_img))
            img_label.pack()
            # όταν κλείσει παράθυρο , διαγράφουμε τη λίστα με τα persons από το graph 
            tree_img.protocol("WM_DELETE_WINDOW", lambda: self.kill_window(tree_img, graph))
            tree_img.mainloop()


    def update_cursor(self, event, tree_img):
        width = 40
        height = 20
        for node_id, (x, y) in self.coordinates.items():
            if event.x in range(x - width, x  + width) and event.y in range(y - height, y + height):
                tree_img.config(cursor="hand1")
                break
            else:
                tree_img.config(cursor="")

                
    """αξιοποιεί τις συντεταγμένες x, y του click event για να εντοπίσει τον κόμβο που πάτησε ο χρήστης στο παράθυρο του δέντρου"""
    def get_node_info(self, event):
        # αυθαίρετα προσδιορισμένα όρια κόμβων
        width = 40
        height = 20
        for node_id, (x, y) in self.coordinates.items():
            if event.x in range(x - width, x  + width) and event.y in range(y - height, y + height):
                # άνοιγμα νέου παραθύρου με τις πληροφορίες του ατόμου
                self.open_info_win(self.get_person(node_id, self.all))


    """επιστρέφει το Person object με τα στοιχεία του κόμβου που πάτησε ο χρήστης"""
    def get_person(self, id, all):
        id_list = [person.id for person in all]
        for i, person_id in enumerate(id_list):
            if person_id == id:
                return  all[i]


    """ανοίγει νέο παράθυρο με τις πληροφορίες του ατόμου που έγινε κλικ"""
    def open_info_win(self, current_clicked):
        popup = ctk.CTkToplevel(self.app)
        popup.configure(bg="lightgray")
        fontsize = 16
        popup.title("Πληροφορίες ατόμου")

        label_name = ctk.CTkLabel(popup, text="Όνομα: " + current_clicked.name, font=("Arial", fontsize))
        label_name.pack()
        # εμφάνιση φωτογραφίας, αν υπάρχει
        if current_clicked.photo_path:
            photo = Image.open(current_clicked.photo_path)
            photo = photo.resize((200, 200))
            self.pic = ImageTk.PhotoImage(photo)
            pic_label = tk.Label(popup, image=self.pic)
            pic_label.pack()

        parents = ""
        ancestors = ""
        date_of_birth = ""
        date_of_death = ""
        # αν υπάρχουν γονείς, τους προσθέτουμε στο string parents χωρίζοντας με κόμμα
        if current_clicked.parents:
            parents = f"{current_clicked.parents[0].name}, {current_clicked.parents[1].name}"
        # αν το άτομο έχει παλιότερους προγόνους, προσθέτουμε τα ονόματά τους στο string ancestors χωρισμένα με κόμμα
        if current_clicked.oldest_ancestors:
            for i, ancestor in enumerate(current_clicked.oldest_ancestors):
                if i != len(current_clicked.oldest_ancestors) - 1:
                    ancestors += ancestor.name + ", "
                else:
                    ancestors += ancestor.name
        # προσθήκη επιπλέον πληροφοριών (ημερομηνία γέννησης/θανάτου)
        if current_clicked.dob:
            date_of_birth = current_clicked.dob
        if current_clicked.dod:
            date_of_death = current_clicked.dod
        
        # δημιουργία πεδίων "Παλαιότεροι πρόγονοι" και "Γονείς", εφόσον υπάρχουν
        if ancestors:
            label_ancestor = ctk.CTkLabel(popup, text="Παλαιότεροι πρόγονοι: " + ancestors, font=("Arial", fontsize))
            label_ancestor.pack()
        if parents:
            label_parents = ctk.CTkLabel(popup, text="Γονείς: " + parents, font=("Arial", fontsize))
            label_parents.pack()
        if date_of_birth:
            label_dob = ctk.CTkLabel(popup, text="Ημερομηνία Γέννησης: " + date_of_birth, font=("Arial", fontsize))
            label_dob.pack()
        if date_of_death:
            label_dod = ctk.CTkLabel(popup, text="Ημερομηνία Θανάτου: " + date_of_death, font=("Arial", fontsize))
            label_dod.pack()
        # κουμπί κλεισίματος παραθύρου
        close_button = ctk.CTkButton(popup, text="Κλείσιμο", command=popup.destroy)
        close_button.pack()


    """διαγράφει τη λίστα με τα Person objects στο Tree class"""
    def kill_window(self, tree_img, graph):
        graph.delete_people()
        tree_img.destroy()
    

    def upload_img(self):
        #  αποδεκτοί τύποι αρχείων εικόνας
        fileTypes = [("Image files", ["*.jpg", "*.jpeg"])]
        path = tk.filedialog.askopenfilename(master=self.app, filetypes=fileTypes)
 
        # αν επιλέχθηκε φωτογραφία, προσθέτουμε το path στο αντίστοιχο entry για ανάκτηση μετά
        if path:
            # καθάρισμα του πεδίου entry_img αν δεν είναι άδειο
            self.entry_img.delete(0, 'end')
            self.entry_img.insert(0, path)
    
        # διακοπή αν δεν επελέγη φωτογραφία
        else:
            print("No file chosen.")
            return


    """run: Υλοποιεί και εμφανίζει το παράθυρο της εφαρμογής"""
    def run(self):
        self.table.pack(fill='both', expand=True)
        self.app.mainloop()

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

def is_list_empty(lst):
    if len(lst) == 0:
        print("The list is empty")
    else:
        print("The list is not empty")

    # Save το δενδρο στο αρχειο json
    try:
        save_family_tree(family_tree)
        print("Family tree saved successfully.")
    except Exception as e:
        print("An error occurred while saving the family tree:", e)

        
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

"""

if __name__ == "__main__":
    main()