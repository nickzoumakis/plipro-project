"""Αντικειμενοστραφής υλοποίηση για το interface"""
from PygraphvizTree import Person, Graph
from pathlib import Path
import pygraphviz as pgv
from PIL import Image, ImageOps, ImageTk
import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import json
import pprint
import datetime

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        # κρύβουμε προσωρινά το main παράθυρο
        self.withdraw()

        # υλοποίηση του popup εισαγωγής (subclass του MainApp)
        self.startup = Startup_Popup(self)
        # Περιμένω για το κλείσιμο του παραθύρου
        self.startup.wait_window()

        # πέρασμα των στοιχείων του αρχείου που επέλεξε ο χρήστης στην self.files 
        self.files = self.startup.get_files()

        # επανεμφάνιση του main app παραθύρου
        self.deiconify()


        # αρχικοποίηση κενού dict που θα φιλοξενήσει όλα τα στοιχεία των ατόμων που προσθέτει ο χρήστης
        self.family_data = {}
        # αρχικοποίηση dict συντεταγμένων κόμβων
        self.coordinates = {}
        # κενή αρχικά λίστα με όλα τα Person objects που θα δημιουργηθούν από το Tree class
        self.all = []

        # μεταβλητές για αμυντικό προγραμματισμό, παρακολουθούν τα παλιά id σε περίπτωση αλλαγών από το χρήστη
        # αποκτούν τιμές όταν επιλέγεται άτομο από το treeview
        # χρησιμοποιούνται από την error_check
        # γίνονται reset σε None μετά από κάθε προσθήκη ατόμου/ενημέρωση στοιχείων/διαγραφή
        (self.old_id, self.old_mother_id, self.old_father_id, self.old_spouse_id) = (None, None, None, None)

        # Στοιχεία και γεωμετρία main παραθύρου
        self.geometry("1500x900")
        self.label_title= ctk.CTkLabel(master=self, text="Γενεαλογικό Δέντρο", font=("Arial", 25), text_color="black")
        self.label_title.place(relx=0.5, rely=0.05, anchor="center")
        ctk.set_appearance_mode("light")

        self.middle = tk.Frame(self, pady=10.5, highlightthickness=3, height=40, width=200)
        self.middle.pack(side=ctk.LEFT, fill='x', expand=True)  # επέκταση στο πλάτος)

        self.label = tk.Label(self.middle, text="Μέλη Οικογένειας", bg='lightgray')
        self.label.pack()

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
        self.entry_date= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_date.place(relx=0.64, rely=0.1, anchor="nw")

        self.label_id= ctk.CTkLabel(master=self, text="ID: ", font=("Arial", 18), text_color="black")
        self.label_id.place(relx=0.02, rely=0.15, anchor="nw")
        self.entry_id= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=230)
        self.entry_id.place(relx=0.053, rely=0.15, anchor="nw")

        self.label_death= ctk.CTkLabel(master=self, text="Ημερομηνία θανάτου: ", font=("Arial", 18), text_color="black")
        self.label_death.place(relx=0.52, rely=0.15, anchor="nw")
        self.entry_death= ctk.CTkEntry(master=self, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
        self.entry_death.place(relx=0.64, rely=0.15, anchor="nw")

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

        self.label_spouse_name = ctk.CTkLabel(master=self, text="Όνομα Συζύγου: ", font=("Arial", 18), text_color="black")
        self.label_spouse_name.place(relx=0.02, rely=0.30, anchor="nw")
        self.entry_spouse_name = ctk.CTkEntry(master=self, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white", width=206)
        self.entry_spouse_name.place(relx=0.11, rely=0.30, anchor="nw")

        self.label_spouse_surname = ctk.CTkLabel(master=self, text="Επώνυμο Συζύγου: ", font=("Arial", 18), text_color="black")
        self.label_spouse_surname.place(relx=0.25, rely=0.30, anchor="nw")
        self.entry_spouse_surname = ctk.CTkEntry(master=self, placeholder_text=" ", font=("Arial", 18),text_color="black", fg_color="white", width=210)
        self.entry_spouse_surname.place(relx=0.36, rely=0.30, anchor="nw")

        self.label_spouse = ctk.CTkLabel(master=self, text="ID Συζύγου: ", font=("Arial", 18), text_color="black")
        self.label_spouse.place(relx=0.52, rely=0.30, anchor="nw")
        self.entry_spouse = ctk.CTkEntry(master=self, placeholder_text=" ", font=("Arial", 18), text_color="black", fg_color="white", width=210)
        self.entry_spouse.place(relx=0.6, rely=0.30, anchor="nw")

        self.entry_img =  ctk.CTkEntry(master=self, placeholder_text= "File path", font=("Arial", 18), text_color="black",fg_color="white",width=300)
        self.entry_img.place(relx=0.8, rely=0.31, anchor="nw")


        # CHECKBOXES για φύλο
        self.checkbox_male = ctk.CTkCheckBox(master=self, text="Άντρας", font=("Arial", 12), hover=True, fg_color="grey", bg_color="Light grey", command=lambda:self.uncheck_other("male"))
        self.checkbox_male.place(relx=0.25, rely=0.15, anchor="nw")
        self.checkbox_female = ctk.CTkCheckBox(master=self, text="Γυναίκα", font=("Arial", 12), hover=True, fg_color="grey", bg_color="light grey", command=lambda:self.uncheck_other("female"))
        self.checkbox_female.place(relx=0.33, rely=0.15, anchor="nw")


        # Κουμπιά αλληλεπίδρασης χρήστη, κάθε command οδηγεί σε νέο function του class
        current_path = Path.cwd().parent / 'buttons'
        ok_path = current_path / "ok.png"
        ok_image = ctk.CTkImage(Image.open(ok_path), size=(30, 30))

        self.btn_add = ctk.CTkButton(master=self, text="Προσθήκη νέου ατόμου", corner_radius=32, command=self.add_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=4, width=20, height=50,
                            image=ok_image,  # Προσθήκη της εικόνας στο κουμπί
                            compound="left"
                            )
        self.btn_add.place(relx=0.15, rely=0.8, anchor="ne")

        current_path = Path.cwd().parent / 'buttons'
        image_path = current_path / "tree_img.png"

        # Δημιουργία της εικόνας
        tree_image = ctk.CTkImage(Image.open(image_path), size=(30, 30))

        # αλλαγή κουμπιού σε 'Δημιουργία Δέντρου' -> περνάει όλα τα άτομα από το family tree dict στο Graph
        # Δημιουργία του κουμπιού με εικόνα
        self.btn_treeview = ctk.CTkButton(
            master=self,
            text="Δημιουργία Δέντρου",
            corner_radius=32, command=self.create_tree,
            fg_color="light blue", hover_color="blue",
            border_color="blue", text_color="black",
            border_width=4, width=20, height=50,
            image=tree_image,  # Προσθήκη της εικόνας στο κουμπί
            compound="left"  # Τοποθέτηση της εικόνας στα αριστερά του κειμένου
        )
        self.btn_treeview.place (relx=0.31, rely=0.8, anchor="ne")

        clear_path = current_path / "clear.png"
        clear_image = ctk.CTkImage(Image.open(clear_path), size=(40, 40))
        self.btn_clear = ctk.CTkButton ( master=self, text="Καθαρισμός πεδίων", corner_radius=32,
                                        command=self.clear_fields,
                                        fg_color="light blue", hover_color="blue",
                                        border_color="blue",  text_color="black",
                                        border_width=2, width=20, height=50,
                                        image=clear_image,  # Προσθήκη της εικόνας στο κουμπί
                                        compound="left")
        self.btn_clear.place (relx=0.47, rely=0.8, anchor="ne")

        update_path = current_path / "update.png"
        update_image = ctk.CTkImage(Image.open(update_path), size=(40, 40))

        self.btn_update = ctk.CTkButton(master=self, text="Ενημέρωση στοιχείων", corner_radius=32, command=self.update_person,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=20, height=50,
                            image = update_image,
                            compound = "left")
        self.btn_update.place(relx=0.63, rely=0.8, anchor="ne")

        can_path = current_path / "carbage can.jpg"
        can_image = ctk.CTkImage(Image.open(can_path), size=(45, 45))
        self.btn_delete = ctk.CTkButton(master=self, text="Διαγραφή ατόμου", corner_radius=32,
                                        command=self.delete_person,
                                        fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                                        border_width=2, width=20, height=50,
                                        image = can_image,  # Προσθήκη της εικόνας στο κουμπί
                                        compound = "left" ) # Τοποθέτηση της εικόνας στα αριστερά του κειμένου

        self.btn_delete.place(relx=0.80, rely=0.8, anchor="ne")

        photo_path = current_path / "photo.png"
        photo_image = ctk.CTkImage(Image.open(photo_path), size=(35, 35))
        self.btn_uploadimg = ctk.CTkButton(master=self, text="Μεταφόρτωση φωτογραφίας", corner_radius=32, command=self.upload_img,
                            fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                            border_width=2, width=25, height=35,
                            image = photo_image, compound = "left" )
        self.btn_uploadimg.place(relx=0.80, rely=0.25, anchor="nw")

        # treeview
        col_titles = (
            "Κωδικός",
            "Όνομα",
            "Επώνυμο",
            "Όνομα Μητέρας",
            "Επώνυμο Μητέρας",
            "ID Μητέρας",
            "Όνομα Πατέρα",
            "Επώνυμο Πατέρα",
            "ID Πατέρα",
            "Όνομα Συζύγου",
            "Επώνυμο Συζύγου",
            "ID Συζύγου")

        self.table = ttk.Treeview(self.middle, columns=col_titles, show='headings')
        # Αλλαγή μεγέθους επικεφαλίδων
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 13))
        # Αλλαγή μεγέθους περιεχομένου
        self.style.configure("Treeview", font=('Arial', 12), anchor='center')

        # Δημιουργία στηλών στο tree view με κεντραρισμένο το κείμενο των entries
        # for title in col_titles:
        # self.table.heading(title, text=title, anchor='center')
        # self.table.column(title, stretch=True, anchor='center')
        # self.table.pack(fill='both', expand=True)

        self.table.heading("#1", text='Κωδικός', anchor='center', )
        self.table.heading("#2", text='Όνομα', anchor='center')
        self.table.heading("#3", text='Επώνυμο', anchor='center')
        self.table.heading("#4", text="Όνομα Μητέρας", anchor='center')
        self.table.heading("#5", text="Επώνυμο Μητέρας", anchor='center')
        self.table.heading("#6", text="ID Μητέρας", anchor='center')
        self.table.heading("#7", text="Όνομα Πατέρα", anchor='center')
        self.table.heading("#8", text="Επώνυμο Πατέρα", anchor='center')
        self.table.heading("#9", text="ID Πατέρα", anchor='center')
        self.table.heading("#10", text='Όνομα Συζύγου', anchor='center')
        self.table.heading("#11", text='Επώνυμο Συζύγου', anchor=tk.CENTER)
        self.table.heading("#12", text="ID Συζύγου", anchor=tk.CENTER)
        self.table.column("#1", anchor='center', stretch=True, width=80)
        self.table.column("#2", anchor='center', stretch=True, width=120)
        self.table.column("#3", anchor='center', stretch=True, width=150)
        self.table.column("#4", anchor='center', stretch=True, width=120)
        self.table.column("#5", anchor='center', stretch=True, width=150)
        self.table.column("#6", anchor='center', stretch=True, width=80)
        self.table.column("#7", anchor='center', stretch=True, width=120)
        self.table.column("#8", anchor='center', stretch=True, width=150)
        self.table.column("#9", anchor='center', stretch=True, width=80)
        self.table.column("#10", anchor='center', stretch=True, width=130)
        self.table.column("#11", anchor='center', stretch=True, width=130)
        self.table.column("#12", anchor='center', stretch=True, width=130)

        self.table.pack(fill='both', expand=True)  # το Treeview επεκτείνεται ώστε να γεμίζει το διαθέσιμο χώρο για να έχουν οι στήλες τον απαραίτητο χώρο.
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
    def show_items(self):
        # καθάρισμα αρχικά των πεδίων
        self.clear_fields()

        entries = [self.entry_name,
            self.entry_surname,
            self.entry_date,
            self.entry_id,
            self.entry_death,
            self.entry_mother_name,
            self.entry_mother_surname,
            self.entry_mother_id,
            self.entry_father_name,
            self.entry_father_surname,
            self.entry_father_id,
            self.entry_spouse,
            self.entry_spouse_name,
            self.entry_spouse_surname,
            self.entry_img]
        
        keys = ['name',
                'surname',
                'date_of_birth',
                'id',
                'date_of_death',
                'mother_name',
                'mother_surname',
                'mother_id',
                'father_name',
                'father_surname',
                'father_id',
                'spouse_id',
                'spouse_name',
                'spouse_surname',
                'photo_path']

        # εύρεση των στοιχείων του ατόμου με βάση το id από το family_data dict και όχι από τα selected items του treeview (δεν περιλαμβάνει κενά πεδία)
        selected_item = self.table.selection()
        # διακοπή της συνάρτησης αν δεν έχει επιλεγεί άτομο ή γίνει διαγραφή του επιλεγμένου
        if not selected_item:
            return
        selected_id = str(self.table.item(selected_item)['values'][0])

        # εκχώρηση του τωρινού id ατόμου και γονιών/συζύγου στις old_id για παρακολούθηση αλλαγών από το χρήστη
        self.old_id = selected_id
        self.old_mother_id = self.family_data[selected_id]['mother_id']
        self.old_father_id = self.family_data[selected_id]['father_id']
        self.old_spouse_id = self.family_data[selected_id]['spouse_id']

        # πληθωρισμός του treeview με τα στοιχεία του επιλεγμένου ατόμου
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


    def check_and_add(self, id, name, surname, gender, spouse_id="", spouse_name="", spouse_surname="", mother_id="",
                      mother_name="", mother_surname="", father_id="", father_name="", father_surname=""):
        """
        Ελέγχει αν υπάρχει το ID και αν όχι προσθέτει νέα εγγραφή για τον γονιό ή σύζυγο.
        Ενημερώνει και τα στοιχεία του συζύγου, μητέρας και πατέρα αν υπάρχουν.
        """
        # Ενημερώνει τα στοιχεία του συζύγου στην εγγραφή του spouse
        if spouse_id and spouse_id in self.family_data:
            self.family_data[spouse_id]["spouse_id"] = id
            self.family_data[spouse_id]["spouse_name"] = name
            self.family_data[spouse_id]["spouse_surname"] = surname

        # Ενημερώνει τα στοιχεία της μητέρας στην εγγραφή του πατέρα αν δεν είναι ο σύζυγος
        if father_id and father_id in self.family_data:
            self.family_data[father_id]["spouse_id"] = mother_id
            self.family_data[father_id]["spouse_name"] = mother_name
            self.family_data[father_id]["spouse_surname"] = mother_surname

        # Ενημερώνει τα στοιχεία του πατέρα στην εγγραφή της μητέρας αν δεν είναι ο σύζυγος
        if mother_id and mother_id in self.family_data:
            self.family_data[mother_id]["spouse_id"] = father_id
            self.family_data[mother_id]["spouse_name"] = father_name
            self.family_data[mother_id]["spouse_surname"] = father_surname

        if id not in self.family_data:
            self.family_data[id] = {
                "name": name,
                "surname": surname,
                "date_of_birth": "",
                "gender": gender,
                "date_of_death": "",
                "mother_name": "",
                "mother_surname": "",
                "mother_id": "",
                "father_name": "",
                "father_surname": "",
                "father_id": "",
                "spouse_name": spouse_name,
                "spouse_surname": spouse_surname,
                "spouse_id": spouse_id,
                "photo_path": ""
            }

            # Προσθέτει τον γονιό ή σύζυγο στο treeview-gui table
            self.table.insert('', 'end', values=(
                id,
                name,
                surname,
                mother_name,
                mother_surname,
                mother_id,
                father_name,
                father_surname,
                father_id,
                spouse_name,
                spouse_surname,
                spouse_id
            ))

    """add_person: Προσθέτει τα στοιχεία του ατόμου στον πίνακα του παραθύρου και ενημερώνει το dict"""
    def add_person(self):
        #TODO: Συμμέζεμα του κώδικα, υπάρχουν άλλα 2 methods που καλούν τη get για τα ίδια δεδομένα - να μπει σε ξεχωριστό method?
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
        spouse_name = self.entry_spouse_name.get()
        spouse_surname = self.entry_spouse_surname.get()
        photo_path = self.entry_img.get()

        # εκτέλεση της error_check για εύρεση λαθών και διακοπή συνέχειας αν επιστρέψει True
        if self.error_check():
            return
        # αν η error_check επιστρέψει false, τα δεδομένα μπορούν να προστεθούν στο family_data

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
            "spouse_name" : spouse_name,
            "spouse_surname" : spouse_surname,
            "photo_path": photo_path
        }

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
            father_id,
            spouse_name,
            spouse_surname,
            spouse_id)
                              )
        # Έλεγχος και προσθήκη γονιών ή συζύγου αν δεν υπάρχουν
        if mother_id:
            self.check_and_add(mother_id, mother_name, mother_surname, 'female', spouse_id=father_id,
                               spouse_name=father_name, spouse_surname=father_surname)
        if father_id:
            self.check_and_add(father_id, father_name, father_surname, 'male', spouse_id=mother_id,
                               spouse_name=mother_name,  spouse_surname=mother_surname)
        if spouse_id:
            self.check_and_add(spouse_id, spouse_name, spouse_surname, '', id, name, surname)

        # για debugging
        #pprint.pprint(self.family_data)
        # Καθάρισμα των πεδίων για το επόμενο άτομο
        self.clear_fields()
        # ενημέρωση του json
        self.save()
        # επαναφορά id change flags σε None
        self.reset_id_change_flags()



    """clear_fields: Καθαρίζει όλα τα πεδία"""
    def clear_fields(self):
        for entry in [self.entry_name,
                    self.entry_surname,
                    self.entry_date,
                    self.entry_id,
                    self.entry_death,
                    self.entry_mother_name,
                    self.entry_mother_surname,
                    self.entry_mother_id,
                    self.entry_father_name,
                    self.entry_father_surname,
                    self.entry_father_id,
                    self.entry_spouse,
                    self.entry_spouse_name,
                    self.entry_spouse_surname,
                    self.entry_img]:
            entry.delete(0, 'end')
        
        # Ξετσεκάρει τα checkboxes
        for checkbox in [self.checkbox_male, self.checkbox_female]:
            checkbox.deselect()

        # επαναφορά id change flags σε None
        self.reset_id_change_flags()

    def save(self):
        json_filepath = self.files['json_path']
        try:
            with open(json_filepath, "w") as file:
                json.dump(self.family_data, file, indent=4)

        except Exception as e:
            print("¨Πρόβλημα στην αποθήκευση του αρχείου", e)


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
        spouse_name = self.entry_spouse_name.get()
        spouse_surname = self.entry_spouse_surname.get()
        spouse_id = self.entry_spouse.get()
        photo_path = self.entry_img.get()

        # έλεγχος με την error_check ώστε να μη μπορεί ο χρήστης να κάνει update με λανθασμένα στοιχεία
        if self.error_check(update=True):
            self.reset_id_change_flags()
            self.clear_fields()
            return
        
         # Έλεγχος και προσθήκη γονιών ή συζύγου αν δεν υπάρχουν
        if mother_id:
            self.check_and_add(mother_id, mother_name, mother_surname, 'female', spouse_id=father_id,
                               spouse_name=father_name, spouse_surname=father_surname)
        if father_id:
            self.check_and_add(father_id, father_name, father_surname, 'male', spouse_id=mother_id,
                               spouse_name=mother_name, spouse_surname=mother_surname)
        if spouse_id:
            self.check_and_add(spouse_id, spouse_name, spouse_surname, '', person_id, name, surname)

        # Ενημέρωση των keys του family_data dict για το συγκεκριμένο id
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
            "spouse_name": spouse_name,
            "spouse_surname": spouse_surname,
            "photo_path": photo_path
        }
        self.save()
        # επαναφορά id change flags σε None
        self.reset_id_change_flags()

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
            father_id,
            spouse_name,
            spouse_surname,
            spouse_id))
        #self.save()
        

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
        self.save()
        # επαναφορά id change flags σε None
        self.reset_id_change_flags()
        #debug print
        #print(self.family_data)


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


    """ load_image: άνοιγμα εικόνας δέντρου σε νέο παράθυρο tkinter (καλώντας νέο subclass: Tree_Window) """
    def load_image(self, img_filename, graph):
        tree = Tree_Window(self, img_filename, graph)
        # φέρνουμε το παράθυρο του δέντρου στο προσκήνιο
        tree.attributes("-topmost", True)


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

    # αμυντικός προγραμματισμός με εμφάνιση ενημερωτικού popup και επιστροφή True, αλλιώς False
    def error_check(self, update=False):
        # λήψη του μοναδικού κωδικού του ατόμου
        id = self.entry_id.get()
        # για κάθε στοιχείο που εισήγαγε ο χρήστης
        name = self.entry_name.get()
        surname = self.entry_surname.get()
        dob = self.entry_date.get()
        dod = self.entry_death.get()
        mother_name = self.entry_mother_name.get()
        mother_surname = self.entry_mother_surname.get()
        mother_id = self.entry_mother_id.get()
        father_name = self.entry_father_name.get()
        father_surname = self.entry_father_surname.get()
        father_id = self.entry_father_id.get()
        spouse_id = self.entry_spouse.get()
        spouse_name = self.entry_spouse_name.get()
        spouse_surname = self.entry_spouse_surname.get()
        
        # έλεγχος αν τα id, εφόσον εισήχθησαν είναι ακέραιοι
        all_ids = [id, mother_id, father_id, spouse_id]
        for entry in all_ids:
            if entry:
                try:
                    int(entry)
                except ValueError:
                    messagebox.showinfo(title="info",
                                        message="Παρακαλώ εισάγετε σωστές τιμές στα πεδία\nτα id: ακέραιοι αριθμοί")
                    return True
        # έλεγχος αν υπάρχουν διπλότυπα στις φόρμες
        for _id in all_ids:
            if _id:
                for other_id in all_ids[all_ids.index(_id) + 1:]: 
                    if other_id and other_id == _id: 
                        messagebox.showinfo(title="ERROR",
                                                    message="Παρακαλώ εισάγετε σωστές τιμές στα πεδία\nΒρέθηκαν διπλότυπα id.")
                        return True      
                    
        # αν η συνάρτηση κλήθηκε με την παράμετρο update, έχει πατηθεί ενημέρωση στοιχείων
        if update:
            # boolean παράμετροι που ελέγχουν αν ο χρήστης έχει αλλάξει το id ατόμου ή/και γονιών/συζύγου
            (id_change, mother_id_change, father_id_change, spouse_id_change) = (False, False, False, False)
            # αν ο χρήστης έχει κάνει κλικ σε υπάρχον άτομο, συγκρίνω και τα παλιά id με τα καινούρια και ενεργοποιώ τα boolean για παρακολούθηση
            if self.old_id and self.old_id != id:
                id_change = True
            if self.old_father_id and self.old_father_id != father_id:
                father_id_change = True
            if self.old_mother_id and self.old_mother_id != mother_id:
                mother_id_change = True
            if self.old_spouse_id and self.old_spouse_id != spouse_id:
                spouse_id_change = True

        # Έλεγχοι ID, όνομα, επώνυμο για άτομο / γονείς
        # αν υπάρχει τουλάχιστον ένα από id, name, surname, προχωράμε σε ελέγχους εγκυρότητας
        if name or surname or id:
            for entry in [name, surname]:
                if entry:
                    # αλφαβητικός έλεγχος name/surname
                    if not entry.isalpha() :
                        messagebox.showinfo(title="info",
                                            message="Παρακαλώ συμπληρώστε τουλάχιστον ένα από τα πεδία:\n"
                                                    "Όνομα και Επώνυμο με χαρακτήρες")
                        return True
            # έλεγχος ανυπαρξίας id
            if id == "":
                messagebox.showerror(title='ERROR', message="Παρακαλώ συμπληρώστε το πεδίο ID")
                return True
            # αν πατήθηκε προσθήκη νέου ατόμου, αρκεί να ελέγξω για διπλότυπα ID 
            if not update:
                if id in self.family_data:
                    messagebox.showinfo(title='Ιnfo', message="Το ΙD υπάρχει ήδη.")
                    return True
            # διαφορετικά, δεν επιτρέπω στο χρήστη να αλλάξει id τοποθετημένου ατόμου
            elif id_change:
                messagebox.showinfo(title='Ιnfo', message="Δεν επιτρέπεται η αλλαγή ID τοποθετημένου ατόμου.")
                return True
            
        # διαφορετικά, τα πεδία είναι ελλειπή
        else:
            messagebox.showinfo(title='Info', message="Παρακαλώ συμπληρώστε όνομα ή επώνυμο και ID")
            return True
        
        # ίδιοι έλεγχοι για γονείς
        if mother_name or mother_surname or mother_id:
            for entry in [mother_name, mother_surname]:
                if entry:
                    if not entry.isalpha() :
                        messagebox.showinfo(title="info",
                                            message="Παρακαλώ συμπληρώστε τουλάχιστον ένα από τα πεδία:\n"
                                                    "Όνομα και Επώνυμο Μητέρας με χαρακτήρες")
                        return True
            if mother_id == "":
                messagebox.showerror(title='ERROR', message="Παρακαλώ συμπληρώστε το πεδίο id της Μητέρας")
                return True
            
            # διαφορετικά, δεν επιτρέπω στο χρήστη να αλλάξει id τοποθετημένου ατόμου
            if update and mother_id_change:
                messagebox.showinfo(title='Ιnfo', message="Δεν επιτρέπεται η αλλαγή ID τοποθετημένου ατόμου.")
                return True
            
        if father_name or father_surname or father_id:
            for entry in [father_name, father_surname]:
                if entry:
                    if not entry.isalpha() :
                        messagebox.showinfo(title="info",
                                            message="Παρακαλώ συμπληρώστε τουλάχιστον ένα από τα πεδία:\n"
                                                    "Όνομα και Επώνυμο Πατέρα με χαρακτήρες")
                        return True
            if father_id == "":
                messagebox.showerror(title='ERROR', message="Παρακαλώ συμπληρώστε το πεδίο id του Πατέρα")
                return True
            
            # διαφορετικά, δεν επιτρέπω στο χρήστη να αλλάξει id τοποθετημένου ατόμου
            if update and father_id_change:
                messagebox.showinfo(title='Ιnfo', message="Δεν επιτρέπεται η αλλαγή ID τοποθετημένου ατόμου.")
                return True
        
        # έλεγχος έγκυρου (υπάρχοντος ή νέου) ζεύγους id γονιών
        if father_id and mother_id:
            # λήψη όλων των υπάρχοντων ζευγαριών id γονιών ως τώρα
            existing = [(self.family_data[id]['mother_id'], self.family_data[id]['father_id']) for id in self.family_data]
            # boolean μεταβλητές για αποδοχή
            accept = False
            reverse = False
            wrong_id = False
            for momid, dadid in existing:
                # περίπτωση 1: το ζεύγος γονιών ταυτίζεται με υπάρχον - αποδοχή
                if momid == mother_id and dadid == father_id:
                    accept = True
                    break
                # περίπτωση 2: το ζεύγος έχει ανεστραμμένο 1 ή και τα 2 id - μη αποδοχή
                elif momid == father_id or dadid == mother_id:
                    reverse = True
                    break
                # περίπτωση 3: το ζεύγος έχει έχει ένα σωστό id και ένα που δεν υπάρχει - μη αποδοχή
                else:
                    if (dadid == father_id and momid != mother_id) or (momid == mother_id and dadid != father_id):
                        wrong_id = True
                        break
            # εμφάνιση error για μη αποδοχή και αντιστροφή id, διαφορετικά αποδοχή ως νέο ζεύγος (νέο άτομο με 2 νέους γονείς) ή υπάρχον (αδερφός υπάρχοντος ατόμου)
            if (not accept and reverse) or (not accept and wrong_id):
                messagebox.showerror(title='ERROR', message="Λανθασμένο ζευγάρι ID γονιών.")
                return True

        # αν έχει δοθεί σύζυγος, ελέγχουμε και αν το id έχει ήδη συσχετισθεί με άλλο άτομο
        if spouse_name or spouse_surname or spouse_id:
            for entry in [spouse_name, spouse_surname]:
                if entry:
                    if not entry.isalpha() :
                        messagebox.showinfo(title="info",
                                            message="Παρακαλώ συμπληρώστε τουλάχιστον ένα από τα πεδία:\n"
                                                    "Όνομα και Επώνυμο Συζύγου με χαρακτήρες")
                        return True
            if spouse_id == "":
                messagebox.showerror(title='ERROR', message="Παρακαλώ συμπληρώστε το πεδίο id Συζύγου")
                return True
            elif spouse_id in self.family_data and self.family_data[spouse_id]["spouse_id"] != id:
                messagebox.showerror(title='ERROR', message="Το id Συζύγου είναι ήδη δεσμευμένο.")
                return True
            if update and spouse_id_change:
                messagebox.showinfo(title='Ιnfo', message="Δεν επιτρέπεται η αλλαγή ID τοποθετημένου ατόμου.")
                return True
            
        if self.checkbox_male.get() == 0 and self.checkbox_female.get() == 0:
            messagebox.showerror(title='ERROR', message="Παρακαλώ επιλέξτε φύλο")
            return True


        if not dob == "":
            try:
                birth = datetime.datetime.strptime(dob, '%d/%m/%Y')
            except ValueError:
                messagebox.showinfo(title='info', message="Παρακαλώ εισάγετε σωστά την ημερομηνία γέννησης!")
                return True

        if not dod == "":
            try:
                dd = datetime.datetime.strptime(dod, '%d/%m/%Y')
            except ValueError:
                messagebox.showinfo(title='info', message="Παρακαλώ εισάγετε σωστά την ημερομηνία θανάτου!")
                return True
        # αν περάσει όλους τους ελέγχους, επιστροφή False
        return False

    # επαναφέρει σε None μετά από κάθε προσθήκη ατόμου/ενημέρωση στοιχείων/διαγραφή
    def reset_id_change_flags(self):
        (self.old_id, self.old_mother_id, self.old_father_id, self.old_spouse_id) = (None, None, None, None)
    


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
            string_path = str(path).split('/')
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
                    string_filepath = str(existing_filepath).split('/')
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
    
"""Κλάση Tree_Window: Άνοιγμα της εικόνας του δέντρου σε νέο παράθυρο"""
class Tree_Window(ctk.CTkToplevel):
    def __init__(self, master, img_filename, graph):
        super().__init__(master)
        self.tree_img = None
        # πέρασμα στην self.coordinates των συντεταγμένων που έλαβε η MainApp από το PygraphvizTree
        self.coordinates = master.coordinates
        # πέρασμα στην self.all των Person objects από τη MainApp
        self.all = master.all
        # ανάθεση στο path
        img_path = Path.cwd().parent / 'graph' / img_filename
        # άνοιγμα εικόνας με PIL
        self.tree_img = Image.open(img_path)
        self.img = ImageTk.PhotoImage(self.tree_img)
        pic_label = tk.Label(self, image=self.img)
        pic_label.pack()
        # για όσο τρέχει το παράθυρο του δέντρου, κάνουμε bind το click event στο get_node_info
        self.bind("<Button-1>", lambda event:self.get_node_info(event))
        self.bind("<Motion>", lambda event:self.update_cursor(event))
        # όταν κλείσει παράθυρο , διαγράφουμε τη λίστα με τα persons από το graph 
        self.protocol("WM_DELETE_WINDOW", lambda: self.kill_window(graph))


    def update_cursor(self, event):
        width = 40
        height = 20
        for node_id, (x, y) in self.coordinates.items():
            if event.x in range(x - width, x  + width) and event.y in range(y - height, y + height):
                self.config(cursor="hand1")
                break
            else:
                self.config(cursor="")


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


    def open_info_win(self, current_clicked):
        info_popup = Info_Popup(self, current_clicked)
        # κάνουμε focus στο νέο παράθυρο
        self.attributes("-topmost", False)
        info_popup.attributes("-topmost", True)


    """διαγράφει τη λίστα με τα Person objects στο Tree class"""
    def kill_window(self, graph):
        graph.delete_people()
        self.destroy()
        

"""Subclass νέου παραθύρου με τις πληροφορίες του ατόμου που έγινε κλικ"""
class Info_Popup(ctk.CTkToplevel):
    def __init__(self, master, current_clicked):
        super().__init__(master)
        self.pic = None
        self.configure(bg="lightgray")
        fontsize = 16
        self.title("Πληροφορίες ατόμου")

        label_name = ctk.CTkLabel(self, text="Όνομα: " + current_clicked.name, font=("Arial", fontsize))
        label_name.pack()
        # εμφάνιση φωτογραφίας, αν υπάρχει
        if current_clicked.photo_path:
            photo = Image.open(current_clicked.photo_path)
            # χρήση της cover από το ImageOps του PIL για διατήρηση του λόγου πλευρών
            photo = ImageOps.cover(photo, (200, 200))
            self.pic = ImageTk.PhotoImage(photo)
            pic_label = tk.Label(self, image=self.pic)
            pic_label.pack()

        parents = ""
        ancestors = ""
        date_of_birth = ""
        date_of_death = ""
        # αν υπάρχουν γονείς, τους προσθέτουμε στο string parents χωρίζοντας με κόμμα
        if current_clicked.parents:
            if len(current_clicked.parents) == 2:
                parents = f"{current_clicked.parents[0].name}, {current_clicked.parents[1].name}"
            else:
                parents = f"{current_clicked.parents[0].name}"
        # αν το άτομο έχει παλιότερους προγόνους, προσθέτουμε τα ονόματά τους στο string ancestors χωρισμένα με κόμμα
        if current_clicked.oldest_ancestors:
            for i, ancestor in enumerate(current_clicked.oldest_ancestors):
                if i != len(current_clicked.oldest_ancestors) - 1:
                    if i % 2 == 0:
                        ancestors += ancestor.name + ", "
                    else:
                        ancestors += ancestor.name + '\n'
                else:
                    ancestors += ancestor.name
        # προσθήκη επιπλέον πληροφοριών (ημερομηνία γέννησης/θανάτου)
        if current_clicked.dob:
            date_of_birth = current_clicked.dob
        if current_clicked.dod:
            date_of_death = current_clicked.dod
        
        # δημιουργία πεδίων "Παλαιότεροι πρόγονοι" και "Γονείς", εφόσον υπάρχουν
        if ancestors:
            label_ancestor = ctk.CTkLabel(self, text="Παλαιότεροι πρόγονοι: " + ancestors, font=("Arial", fontsize))
            label_ancestor.pack()
        if parents:
            label_parents = ctk.CTkLabel(self, text="Γονείς: " + parents, font=("Arial", fontsize))
            label_parents.pack()
        if date_of_birth:
            label_dob = ctk.CTkLabel(self, text="Ημερομηνία Γέννησης: " + date_of_birth, font=("Arial", fontsize))
            label_dob.pack()
        if date_of_death:
            label_dod = ctk.CTkLabel(self, text="Ημερομηνία Θανάτου: " + date_of_death, font=("Arial", fontsize))
            label_dod.pack()
        # κουμπί κλεισίματος παραθύρου
        close_button = ctk.CTkButton(self, text="Κλείσιμο", command=self.destroy)
        close_button.pack()
    



"""Συνάρτηση main"""
def main():
    # υλοποίηση του παραθύρου
    family_tree = MainApp()
    family_tree.mainloop()


if __name__ == "__main__":
    main()