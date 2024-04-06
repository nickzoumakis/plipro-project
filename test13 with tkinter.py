from cProfile import label
from PIL._tkinter_finder import tk
from customtkinter import *
from tkinter import  ttk
import tkinter as tk
from PIL import Image

app = CTk()
#frame = CTkFrame(master=app,bg_color="white", border_color="grey", border_width=2, height=200, width=200)
#frame.pack()
app.geometry("1500x1100")
label_title= CTkLabel(master=app, text=" Genealogy Tree", font=("Arial", 25), text_color="black")
label_title.place(relx=0.5, rely=0.05, anchor="center")
set_appearance_mode("light")

app2 = tk.Tk()
app2.geometry('600x400')
app2.title('Treeview')
#app2.place(relx=0.2, rely=10.8, anchor="ne")

# img= Image.open("photo.png")
#LABELS FOR INPUT & TEXT ENTRY
label_name= CTkLabel(master=app, text=" Name :", font=("Arial", 18), text_color="black")
label_name.place(relx=0.02, rely=0.1, anchor="nw")
entry_name= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=270)
entry_name.place(relx=0.065, rely=0.1, anchor="nw")

label_surname= CTkLabel(master=app, text=" Surname :", font=("Arial", 18), text_color="black")
label_surname.place(relx=0.25, rely=0.1, anchor="nw")
entry_surname= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=270)
entry_surname.place(relx=0.31, rely=0.1, anchor="nw")

label_date= CTkLabel(master=app, text=" Date of Birth :", font=("Arial", 18), text_color="black")
label_date.place(relx=0.5, rely=0.1, anchor="nw")
entry_date= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_date.place(relx=0.6, rely=0.1, anchor="nw")

label_id= CTkLabel(master=app, text=" ID :", font=("Arial", 18), text_color="black")
label_id.place(relx=0.8, rely=0.1, anchor="nw")
entry_id= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_id.place(relx=0.83, rely=0.1, anchor="nw")

label_mother_id= CTkLabel(master=app, text=" Mother (ID) :", font=("Arial", 18), text_color="black")
label_mother_id.place(relx=0.02, rely=0.2, anchor="nw")
entry_mother_id= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_mother_id.place(relx=0.09, rely=0.2, anchor="nw")

label_father_id= CTkLabel(master=app, text=" Father (ID) :", font=("Arial", 18), text_color="black")
label_father_id.place(relx=0.25, rely=0.2, anchor="nw")
entry_father_id= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_father_id.place(relx=0.33, rely=0.2, anchor="nw")

label_spouse= CTkLabel(master=app, text=" Spouse (ID) :", font=("Arial", 18), text_color="black")
label_spouse.place(relx=0.02, rely=0.3, anchor="nw")
entry_spouse= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_spouse.place(relx=0.095, rely=0.3, anchor="nw")

label_death= CTkLabel(master=app, text=" Date of Death :", font=("Arial", 18), text_color="black")
label_death.place(relx=0.5, rely=0.3, anchor="nw")
entry_death= CTkEntry(master=app, placeholder_text= " ", font=("Arial", 18), text_color="black",fg_color="white",width=190)
entry_death.place(relx=0.6, rely=0.3, anchor="nw")

#CHECKBOXES
checkbox_male = CTkCheckBox(master=app, text="Male", font=("Arial", 12), fg_color="grey", bg_color="Light grey")
checkbox_male.place(relx=0.23, rely=0.3, anchor="nw")
checkbox_female = CTkCheckBox(master=app, text="Female", font=("Arial", 12), fg_color="grey", bg_color="light grey")
checkbox_female.place(relx=0.3, rely=0.3, anchor="nw")





btn_add = CTkButton(master=app, text="Προσθήκη νέου ατόμου", corner_radius=32,
                    fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                    border_width=2, width=20, height=50)
btn_add.place(relx=0.2, rely=0.8, anchor="ne")

btn_search = CTkButton(master=app, text="Aναζήτηση ατόμου", corner_radius=32,
                       fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                       border_width=2, width=20, height=50)
btn_search.place(relx=0.4, rely=0.8, anchor="ne")

btn_delete = CTkButton(master=app, text="Ενημέρωση στοιχείων ατόμου", corner_radius=32,
                       fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                       border_width=2, width=20, height=50)
btn_delete.place(relx=0.6, rely=0.8, anchor="ne")

btn_delete = CTkButton(master=app, text="Διαγραφή ατόμου", corner_radius=32,
                       fg_color="light blue", hover_color="blue", border_color="blue",  text_color="black",
                       border_width=2, width=20, height=50)
btn_delete.place(relx=0.8, rely=0.8, anchor="ne")



# treeview
table = ttk.Treeview(app2, columns = ('first', 'last', 'birth', 'death', 'mid', 'fid', 'spid','gen'), show = 'headings')
table.heading('first', text = 'First name')
table.heading('last', text = 'Surname')
table.heading('birth', text = 'Date Of Birth')
table.heading('death', text = 'Date Of Death')
table.heading('mid', text = 'Mother_Id')
table.heading('fid', text = 'Father_Id')
table.heading('spid', text = 'Spouse_Id')
table.heading('gen', text = 'Gender')
table.pack(fill = 'both', expand = True)

app.mainloop()