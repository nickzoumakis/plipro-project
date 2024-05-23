"""Αντικειμενοστραφής υλοποίηση για το interface"""
"""Windows version"""

from pathlib import Path
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import simpledialog
import json
import pprint
from tkinter import messagebox
import datetime


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # υλοποίηση του popup εισαγωγής (subclass του MainApp)
        self.startup = Startup_Popup(self)
        # Περιμένω για το κλείσιμο του παραθύρου
        self.startup.wait_window()

        # πέρασμα των στοιχείων του αρχείου που επέλεξε ο χρήστης στην self.files 
        self.files = self.startup.get_files()

        # αρχικοποίηση κενού dict που θα φιλοξενήσει όλα τα στοιχεία των ατόμων που προσθέτει ο χρήστης
        self.family_data = {}
        # αρχικοποίηση dict συντεταγμένων κόμβων
        self.coordinates = {}
        # κενή αρχικά λίστα με όλα τα Person objects που θα δημιουργηθούν από το Tree class
        self.all = []
        # κενή αρχικά μεταβλητή για το photo object, για αποτροπή του garbage collection και διαγραφή του
        self.pic = None

        # Στοιχεία και γεωμετρία main παραθύρου
        self.geometry("1500x900")
        self.label_title= ctk.CTkLabel(master=self, text="Γενεαλογικό Δέντρο", font=("Arial", 25), text_color="black")
        self.label_title.place(relx=0.5, rely=0.05, anchor="center")
        ctk.set_appearance_mode("light")

        self.middle = tk.Frame(self, pady=10.5, highlightthickness=2, height=30, width=20)
        self.middle.pack(side = ctk.LEFT)

        # Πεδία εισαγωγής
        self.label_name= ctk.CTkLabel(master=self, text="Όνομα: ", font=("Arial", 18), text_color="black")
        self.label_name.place(relx=0.02, rely=0.1, anchor="nw")
        self.entry_name= ctk.CTkEntry(master=self, font=("Arial", 18), text_color="black", fg_color="white",width=270)
        self.entry_name.place(relx=0.065, rely=0.1, anchor="nw")

        self.label_surname= ctk.CTkLabel(master=self, text="Επώνυμο: ", font=("Arial", 18), text_color="black")
        self.label_surname.place(relx=0.25, rely=0.1, anchor="nw")
        self.entry_surname= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=270)
        self.entry_surname.place(relx=0.32, rely=0.1, anchor="nw")

        self.label_date= ctk.CTkLabel(master=self, text="Ημερομηνία γέννησης: ", font=("Arial", 18), text_color="black")
        self.label_date.place(relx=0.52, rely=0.1, anchor="nw")
        self.entry_date= ctk.CTkEntry(master=self, placeholder_text= "yyyy/mm/dd ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_date.place(relx=0.61, rely=0.1, anchor="nw")

        self.label_id= ctk.CTkLabel(master=self, text="ID: ", font=("Arial", 18), text_color="black")
        self.label_id.place(relx=0.02, rely=0.15, anchor="nw")
        self.entry_id= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=230)
        self.entry_id.place(relx=0.053, rely=0.15, anchor="nw")

        self.label_death= ctk.CTkLabel(master=self, text="Ημερομηνία θανάτου: ", font=("Arial", 18), text_color="black")
        self.label_death.place(relx=0.52, rely=0.15, anchor="nw")
        self.entry_death= ctk.CTkEntry(master=self, placeholder_text= "yyyy/mm/dd ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_death.place(relx=0.61, rely=0.15, anchor="nw")

        self.label_mother_name= ctk.CTkLabel(master=self, text="Όνομα Μητέρας: ", font=("Arial", 18), text_color="black")
        self.label_mother_name.place(relx=0.02, rely=0.20, anchor="nw")
        self.entry_mother_name= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=206)
        self.entry_mother_name.place(relx=0.11, rely=0.20, anchor="nw")

        self.label_mother_surname= ctk.CTkLabel(master=self, text="Επώνυμο Μητέρας: ", font=("Arial", 18), text_color="black")
        self.label_mother_surname.place(relx=0.25, rely=0.20, anchor="nw")
        self.entry_mother_surname= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_mother_surname.place(relx=0.36, rely=0.20, anchor="nw")

        self.label_mother_id= ctk.CTkLabel(master=self, text="ID Μητέρας: ", font=("Arial", 18), text_color="black")
        self.label_mother_id.place(relx=0.52, rely=0.20, anchor="nw")
        self.entry_mother_id= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_mother_id.place(relx=0.6, rely=0.20, anchor="nw")

        self.label_father_name= ctk.CTkLabel(master=self, text="Όνομα Πατέρα: ", font=("Arial", 18), text_color="black")
        self.label_father_name.place(relx=0.02, rely=0.25, anchor="nw")
        self.entry_father_name= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=206)
        self.entry_father_name.place(relx=0.11, rely=0.25, anchor="nw")

        self.label_father_surname= ctk.CTkLabel(master=self, text="Επώνυμο Πατέρα: ", font=("Arial", 18), text_color="black")
        self.label_father_surname.place(relx=0.25, rely=0.25, anchor="nw")
        self.entry_father_surname= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_father_surname.place(relx=0.36, rely=0.25, anchor="nw")

        self.label_father_id= ctk.CTkLabel(master=self, text="ID Πατέρα: ", font=("Arial", 18), text_color="black")
        self.label_father_id.place(relx=0.52, rely=0.25, anchor="nw")
        self.entry_father_id= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_father_id.place(relx=0.6, rely=0.25, anchor="nw")

        self.label_spouse= ctk.CTkLabel(master=self, text="ID Συζύγου: ", font=("Arial", 18), text_color="black")
        self.label_spouse.place(relx=0.02, rely=0.30, anchor="nw")
        self.entry_spouse= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_spouse.place(relx=0.11, rely=0.30, anchor="nw")

        self.entry_img =  ctk.CTkEntry(master=self, placeholder_text= "File path", font=("Arial", 18), text_color="black",fg_color="white",width=210)
        self.entry_img.place(relx=0.6, rely=0.31, anchor="nw")

        # CHECKBOXES για φύλο
        self.checkbox_male = ctk.CTkCheckBox(master=self, text="Άντρας", font=("Arial", 12), hover=True, fg_color="grey", bg_color="Light grey", command=lambda:self.uncheck_other("male"))
        self.checkbox_male.place(relx=0.25, rely=0.15, anchor="nw")
        self.checkbox_female = ctk.CTkCheckBox(master=self, text="Γυναίκα", font=("Arial", 12), hover=True, fg_color="grey", bg_color="light grey", command=lambda:self.uncheck_other("female"))
        self.checkbox_female.place(relx=0.33, rely=0.15, anchor="nw")


        # Κουμπιά αλληλεπίδρασης χρήστη, κάθε command οδηγεί σε νέο function του class
        self.btn_add = ctk.CTkButton(master=self, text="Προσθήκη νέου ατόμου", corner_radius=32, command=self.add_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=4, width=20, height=50)
        self.btn_add.place(relx=0.13, rely=0.8, anchor="ne")

        # αλλαγή κουμπιού σε 'Δημιουργία Δέντρου' -> περνάει όλα τα άτομα από το family tree dict στο Graph 
        self.btn_treeview = ctk.CTkButton(master=self, text="Δημιουργία Δέντρου", corner_radius=32, command=self.create_tree,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=4, width=20, height=50)
        self.btn_treeview.place (relx=0.30, rely=0.8, anchor="ne")

        self.btn_clear = ctk.CTkButton(master=self, text="Καθαρισμός πεδίων", corner_radius=32, command=self.clear_fields,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50)
        self.btn_clear.place (relx=0.45, rely=0.8, anchor="ne")

        self.btn_update = ctk.CTkButton(master=self, text="Ενημέρωση στοιχείων", corner_radius=32, command=self.update_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50)
        self.btn_update.place(relx=0.63, rely=0.8, anchor="ne")

        self.btn_delete = ctk.CTkButton(master=self, text="Διαγραφή ατόμου", corner_radius=32, command=self.delete_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50)
        self.btn_delete.place(relx=0.80, rely=0.8, anchor="ne")

        self.btn_uploadimg = ctk.CTkButton(master=self, text="Μεταφόρτωση φωτογραφίας", corner_radius=32, command=self.upload_img,
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
        self.table.pack(fill='both', expand=True)

        # αν στο popup o χρήστης επέλεξε υπάρχον json, ενημερώνουμε το family_data και εμφανίζουμε τα στοιχεία των ατόμων στο treeview
        if not self.startup.is_new_file:
            self.load_existing(self.files['json_path'])


    """φορτώνει dict από το json που διάλεξε ο χρήστης και εμφανίζει τα περιεχόμενά του στο treeview"""
    def load_existing(self, file):  
        # φόρτωση json
        with open(file) as input_json:
            self.family_data = json.load(input_json)

        # debug print
        print("++++++++++++++++\nfamily_data contents\n++++++++++++++++")
        pprint.pprint(self.family_data)
        
        # Προσθέτει το νέο άτομο στο treeview-gui table
        for id, person_info in self.family_data.items():
            # παίρνουμε τα στοιχεία που ενδιαφέρουν για το treeview μέσω της get με default τιμή άδειο string αν δεν έχουν δοθεί από το χρήστη
            person_id = id
            name = person_info.get("name", "")
            surname = person_info.get("surname", "")
            mother_name = person_info.get("mother_name", "")
            mother_surname = person_info.get("mother_surname", "")
            mother_id = person_info.get("mother_id", "")
            father_name = person_info.get("father_name", "")
            father_surname = person_info.get("father_surname", "")
            father_id = person_info.get("father_id", "")
            # εισαγωγή στο treeview
            self.table.insert('', 'end', values=(
                person_id, 
                name, 
                surname, 
                mother_name, 
                mother_surname, 
                mother_id,
                father_name,
                father_surname, 
                father_id)
                ) 
            

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
        for entry, key in zip(entries, keys):
            if  entry == self.entry_id:
                # 3o στοιχείο το ID του ατομου, το παίρνουμε κατευθείαν από το selected_id αφού στο dict δεν υπάρχει μέσα στα keys
                entry.insert(0, selected_id)
            else:
                entry.insert(0, self.family_data[selected_id][key])
        # ενημέρωση του κουτιού για το φύλο
        if self.family_data[selected_id]['gender'] == 'female':
            self.checkbox_female.select()
        else:
            self.checkbox_male.select()


    """add_person: Προσθέτει τα στοιχεία του 
    ατόμου στον πίνακα του παραθύρου και ενημερώνει το dict"""
    def add_person(self):
        try:

        #TODO: Συμμέζεμα του κώδικα, υπάρχουν άλλα 2 methods που καλούν τη get για τα ίδια δεδομένα - να μπει σε ξεχωριστό method
        # λήψη του μοναδικού κωδικού του ατόμου
            id = int(self.entry_id.get())
            # για κάθε στοιχείο που εισήγαγε ο χρήστης
            name = self.entry_name.get()
            surname = self.entry_surname.get()
            dob = self.entry_date.get()
            gender = self.checkbox_male.get()
            dod = self.entry_death.get()
            mother_name = self.entry_mother_name.get()
            mother_surname = self.entry_mother_surname.get()
            mother_id = int(self.entry_mother_id.get())
            father_name = self.entry_father_name.get()
            father_surname = self.entry_father_surname.get()
            father_id = int(self.entry_father_id.get())
            spouse_id = self.entry_spouse.get()
            photo_path = self.entry_img.get()
        except ValueError:
            messagebox.showinfo(title="info",
                                message="Παρακαλώ εισάγετε σωστές τιμές στα πεδία\nτα id: ακέραιοι αριθμοί"
                                        "\nΤα υπόλοιπα πεδία με χαρακτήρες")
            return

        if not name.isalpha() or not surname.isalpha():
            messagebox.showinfo(title="info",
                                message="Παρακαλώ συμπληρώστε τα πεδία : Όνομα και Επώνυμο με χαρακτήρες")
            return

        if not mother_name.isalpha() or not mother_surname.isalpha():
            messagebox.showinfo(title="info",
                                message="Παρακαλώ συμπληρώστε τα πεδία :"
                                        "Όνομα και Επώνυμο Μητέρας με χαρακτήρες")
            return

        if not father_name.isalpha() or not father_surname.isalpha():
            messagebox.showinfo(title="info",
                                message="Παρακαλώ συμπληρώστε τα πεδία :"
                                        "Όνομα και Επώνυμο Πατέρα με χαρακτήρες")
            return







        # Έλεγχοι ID, όνομα, επώνυμο
        if self.entry_name.get() == "" or self.entry_surname.get() == "":
            messagebox.showinfo(title='Info', message="Παρακαλώ συμπληρώστε όνομα και επώνυμο")
            return
        if self.entry_id.get() == "":
            messagebox.showerror(title='ERROR', message="Παρακαλώ συμπληρώστε το πεδίο id")
            return
        if self.checkbox_male.get() == 0 and self.checkbox_female.get() == 0:
            messagebox.showerror(title='ERROR', message="Παρακαλώ επιλέξτε φύλλο")
            return

        if self.entry_mother_name.get() == "" or self.entry_mother_surname.get() == "":
            messagebox.showinfo(title='Info', message="Παρακαλώ συμπληρώστε όνομα και επώνυμο Μητέρας")
            return
        if self.entry_mother_id.get() == "":
            messagebox.showerror(title='ERROR', message="Παρακαλώ συμπληρώστε το πεδίο id της Μητέρας")
            return

        if self.entry_father_name.get() == "" or self.entry_father_surname.get() == "":
            messagebox.showinfo(title='Info', message="Παρακαλώ συμπληρώστε όνομα και επώνυμο Πατέρα")
            return
        if self.entry_father_id.get() == "":
            messagebox.showerror(title='ERROR', message="Παρακαλώ συμπληρώστε το πεδίο id του Πατέρα")
            return

        id = self.entry_id.get()
        if id in self.family_data:
            messagebox.showinfo(title='Ιnfo', message="Το ΙD υπάρχει ήδη.")
            return

        date = self.entry_date.get()

        if not date == "":
            try:
                birth = datetime.datetime.strptime(date, '%Y/%m/%d')
            except ValueError:
                messagebox.showinfo(title='info', message="Παρακαλώ εισάγετε σωστά την ημερονομηνία!")
                return

        death = self.entry_death.get()

        if not death == "":
            try:
                dd = datetime.datetime.strptime(death, '%Y/%m/%d')
            except ValueError:
                messagebox.showinfo(title='info', message="Παρακαλώ εισάγετε σωστά την ημερονομηνία θανάτου!")
                return

        

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
        print("++++++++++++++++\nfamily_data contents\n++++++++++++++++")
        pprint.pprint(self.family_data)

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


    def update_person(self):
        # Παίρνω το ID του ατόμου που θα ενημερώσω και όλα τα στοιχεία απο τις φόρμες
        #print(type(self.entry_id.get()))
        #TODO: Συμμέζεμα του κώδικα, υπάρχουν άλλα 2 methods που καλούν τη get για τα ίδια δεδομένα - να μπει σε ξεχωριστό method
        person_id = self.entry_id.get()
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

        # Ενημέρωση των keys του family_data dict για το συγκεκριμένο id
        try:
            self.family_data[person_id] = {
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
        except KeyError:
            print("Invalid ID")
            return

        selected_item = self.table.selection()
        if not selected_item:
            # επιστροφή αν δεν έχει επιλεγεί άτομο
            messagebox.showinfo(title='info',message='Δεν έχει επιλεχθει καμία εγγραφή')
            return

        # Ενημέρωση του Treeview
        selected_item = self.table.selection()[0]
        self.table.item(selected_item, values=(
                        person_id, 
                        name, 
                        surname, 
                        mother_name, 
                        mother_surname, 
                        mother_id,
                        father_name,
                        father_surname, 
                        father_id)
            )
        # debug print
        print("++++++++++++++++\nfamily_data contents\n++++++++++++++++")
        pprint.pprint(self.family_data)
        
    """διαγράφει άτομο από το treeview και από το family_data"""
    def delete_person(self):
        selected_item = self.table.selection()  # Get the selected item
        if not selected_item:
            # επιστροφή αν δεν έχει επιλεγεί άτομο
            messagebox.showinfo(title='info',message='Δεν έχει επιλεχθει καμία εγγραφή')
            print("No item selected.")
            return

        item_id = self.table.item(selected_item)["values"][0]  # Βρίσκω το Unique ID
        self.table.delete(selected_item)  # Διαγράφω από το Treeview

        del self.family_data[str(item_id)]  # Αφαίρεση από το family_data
        #debug print
        print("++++++++++++++++\nfamily_data contents\n++++++++++++++++")
        pprint.pprint(self.family_data)


    """create_tree: Αποθήκευση γενεαλογικών δεδομένων στο δίσκο. 
    Καλεί το Graph class (απο το module GraphvizTree) και σχεδιάζει εικόνα του δέντρου"""
    def create_tree(self):
        # ανάκτηση των paths και filenames από το files dict
        json_filepath = self.files['json_path']
        # img_filename χωρίς επέκταση αφού στην show της Graph δίνεται σε άλλο όρισμα (format='png')
        img_filename =  self.files['filename']
        img_file_path = self.files['img_path']

        # dump json στο φάκελο data
        with open(json_filepath, "w") as file:
            json.dump(self.family_data, file, indent=4)


    def upload_img(self):
        #  αποδεκτοί τύποι αρχείων εικόνας
        fileTypes = [("Image files", ["*.jpg", "*.jpeg", "*.png"])]
        path = tk.filedialog.askopenfilename(master=self, filetypes=fileTypes)
 
        # αν επιλέχθηκε φωτογραφία, προσθέτουμε το path στο αντίστοιχο entry για ανάκτηση μετά
        if path:
            # καθάρισμα του πεδίου entry_img αν δεν είναι άδειο
            self.entry_img.delete(0, 'end')
            self.entry_img.insert(0, path)
    
        # διακοπή αν δεν επελέγη φωτογραφία
        else:
            print("No file chosen.")
            return
        # debug print
        print("++++++++++++++++\nfamily_data contents\n++++++++++++++++")
        pprint.pprint(self.family_data)


"""Κλάση Popup: Υλοποιεί το εισαγωγικό παράθυρο επιλογής υπάρχοντος json ή δημηιουργίας νέου.ge
    είναι subclass του MainApp, κατηγορίας Toplevel"""
class Startup_Popup(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        # η παράμετρος is_new_file ενημερώνεται αν ο χρήστης επέλεξε δημιουργία νέου αρχείου
        self.is_new_file = False
        # το dict files ενημερώνεται με τα ονόματα και τα paths των σχετικών αρχείων json και png και επιστρέφεται στο MainApp
        self.files = {}
        # Συνάρτηση για να επιλέξω αρχείο από το cur dir από ένα `Listbox`
        self.title("Menu Επιλογής")
        # Ορίζω το μέγεθος του παραθύρου
        width = 400  # Πλάτος σε pixels
        height = 400  # Ύψος σε pixels

        # Υπολογισμός για κεντράρισμα
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # κεντράρισμα
        self.geometry(f"{width}x{height}+{x}+{y}")

        # Δημιουργία στυλ και προσθήκη ετικέτας
        style = ttk.Style()
        style.configure("Custom.TLabel", font=("Arial", 14), foreground="black", background="light blue")

        label = ttk.Label(self, text="Επιλογή αρχείου ή δημιουργία νέου", style="Custom.TLabel")
        label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)  # Προσθέτω padding για περισσότερο χώρο

        # Προσθέτω ενα Listbox για να επιλέξει ο χρηστης αρχείο για άνοιγμα
        listbox = tk.Listbox(self, selectmode=tk.SINGLE, font=("Arial", 14))
        # βρίσκουμε αν υπάρχουν json αρχεία στο φάκελο data
        data_path = Path.cwd().parent / 'data'
        # έλεγχος ανυπαρξίας του φακέλου data και δημιουργία του
        if not data_path.exists():
            data_path.mkdir(parents=True)

        # για διευκόλυνση εμφανίζεται στη λίστα το όνομα κάθε αρχείου μόνο αντί για το πλήρες path
        json_files = [file for file in data_path.glob("*.json")]
        filenames = []
        for path in json_files:
            string_path = str(path).split('\\')
            filenames.append(string_path[len(string_path) - 1].replace('.json', '')) 

        for file in filenames:
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
                        self.files['filename'] = new_file_name
                        json_filename = new_file_name + '.json'
                        self.files['json_path'] = data_path / json_filename
                        self.files['img_path'] = Path.cwd().parent / 'graph' 
                        self.is_new_file = True

                else:
                    # Χρησιμοποιώ τον τρέχοντα κατάλογο για την επιλογή του υπάρχοντος αρχείου
                    existing_filepath = json_files[filenames.index(selected_item)]
                    # για τη συμπλήρωση του files dict, ανακτώ τα στοιχεία που χρειάζομαι
                    string_filepath = str(existing_filepath).split('\\')
                    filename = string_filepath[len(string_filepath) - 1]
                    self.files['filename'] = filename.replace('.json', '')
                    self.files['json_path'] = existing_filepath
                    self.files['img_path'] = Path.cwd().parent / 'graph'

                if not self.files['img_path'].exists():
                    self.files['img_path'].mkdir()
                self.destroy() #Κλείσιμο self

            else:
                print("No file selected")
            
        button_ok = tk.Button(self, text="OK", command=on_ok)
        button_ok.pack(padx=5, pady=5)


    # γνωστοποιεί αν πρέπει να δημιουργηθεί νέο json ή να ανακτηθεί υπάρχον
    def new_file(self):
        if self.is_new_file:
            return True
        return False
    
    # επιστρέφει στο MainApp το dict με τα ονόματα και τα paths των αρχείων 
    def get_files(self):
        return self.files
 

"""Συνάρτηση main"""
def main():
    # υλοποίηση του παραθύρου
    family_tree = MainApp()
    family_tree.mainloop()


if __name__ == "__main__":
    main()
