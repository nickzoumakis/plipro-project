import json
from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Genealogy Tree")
        self.init_ui()
        self.family_tree = {}
        self.load_family_tree()

    def init_ui(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)

        self.add_button = QtWidgets.QPushButton("Add Person")
        self.add_button.clicked.connect(self.add_person)

        self.clear_button = QtWidgets.QPushButton("Clear Fields")
        self.clear_button.clicked.connect(self.clear_fields)

        self.add_entry_button = QtWidgets.QPushButton("Add Entry")
        self.add_entry_button.clicked.connect(self.add_entry)

        self.update_button = QtWidgets.QPushButton("Update Selected")
        self.update_button.clicked.connect(self.update_selected)

        self.delete_button = QtWidgets.QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected)

        self.search_button = QtWidgets.QPushButton("Search Entry")
        self.search_button.clicked.connect(self.search_entry)

        self.view_all_button = QtWidgets.QPushButton("View All")
        self.view_all_button.clicked.connect(self.view_all)

        self.grow_tree_button = QtWidgets.QPushButton("Grow a Tree")
        self.grow_tree_button.clicked.connect(self.grow_tree)

        self.unique_id_button = QtWidgets.QPushButton("Generate Unique ID")
        self.unique_id_button.clicked.connect(self.add_person)  # Connect to add_person method

        control_layout = QtWidgets.QHBoxLayout()
        control_layout.addWidget(self.add_button)
        control_layout.addWidget(self.clear_button)
        control_layout.addWidget(self.add_entry_button)
        control_layout.addWidget(self.update_button)
        control_layout.addWidget(self.delete_button)
        control_layout.addWidget(self.search_button)
        control_layout.addWidget(self.view_all_button)
        control_layout.addWidget(self.grow_tree_button)
        control_layout.addWidget(self.unique_id_button)  # Add the unique ID button to the layout

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.view)
        self.layout.addLayout(control_layout)

        self.field_layout = QtWidgets.QFormLayout()
        self.name_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Name:", self.name_edit)

        self.generation_spinbox = QtWidgets.QSpinBox()
        self.generation_spinbox.setMinimum(0)
        self.field_layout.addRow("Generation:", self.generation_spinbox)

        self.index_spinbox = QtWidgets.QSpinBox()
        self.index_spinbox.setMinimum(0)
        self.field_layout.addRow("Index:", self.index_spinbox)

        self.mom_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Mom:", self.mom_edit)

        self.dad_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Dad:", self.dad_edit)

        self.mom_mother_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Mom's Mother:", self.mom_mother_edit)

        self.mom_father_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Mom's Father:", self.mom_father_edit)

        self.dad_mother_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Dad's Mother:", self.dad_mother_edit)

        self.dad_father_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Dad's Father:", self.dad_father_edit)

        self.spouse_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Spouse:", self.spouse_edit)

        self.children_edit = QtWidgets.QLineEdit()
        self.field_layout.addRow("Children:", self.children_edit)

        self.layout.addLayout(self.field_layout)

        self.person_list = QtWidgets.QListWidget()
        self.layout.addWidget(self.person_list)

        self.person_list.itemClicked.connect(self.select_person_for_deletion)

        self.setLayout(self.layout)

    def load_family_tree(self):
        try:
            with open("family_tree.json", "r") as f:
                self.family_tree = json.load(f)
                self.populate_person_list()
                self.draw_family_tree()
        except FileNotFoundError:
            pass

    def populate_person_list(self):
        self.person_list.clear()
        for person, data in self.family_tree.items():
            full_name = person + " " + data.get('surname', '')  # Concatenate name and surname
            self.person_list.addItem(full_name)

    def save_family_tree(self):
        with open("family_tree.json", "w") as f:
            json.dump(self.family_tree, f, indent=4)

    def draw_family_tree(self):
        self.scene.clear()

        node_positions = {}
        drawn_lines = set()  # Keep track of drawn lines to avoid duplicates

        for person, data in self.family_tree.items():
            x = data['generation'] * 200
            y = data['index'] * 100
            node_positions[person] = (x, y)

        for person, data in self.family_tree.items():
            x, y = node_positions[person]
            self.scene.addEllipse(x - 25, y - 25, 50, 50, QtGui.QPen(QtGui.QColor("black")),
                                  QtGui.QBrush(QtGui.QColor("lightblue")))
            self.scene.addText(person, QtGui.QFont("Arial", 10)).setPos(x - 25, y - 25)

            mom = data.get('mom')
            dad = data.get('dad')
            if mom and mom in node_positions and dad and dad in node_positions:
                mom_x, mom_y = node_positions[mom]
                dad_x, dad_y = node_positions[dad]
                parent_line = (min(mom_x, dad_x), min(mom_y, dad_y), max(mom_x, dad_x), max(mom_y, dad_y))
                if parent_line not in drawn_lines:
                    self.scene.addLine(mom_x, mom_y, dad_x, dad_y, QtGui.QPen(QtGui.QColor("black")))
                    drawn_lines.add(parent_line)

            for spouse in data.get('spouse', []):
                if spouse in node_positions:
                    spouse_x, spouse_y = node_positions[spouse]
                    self.scene.addLine(x, y, spouse_x, spouse_y, QtGui.QPen(QtGui.QColor("black")))

            for child in data.get('children', []):
                if child in node_positions:
                    child_x, child_y = node_positions[child]
                    self.scene.addLine(x, y, child_x, child_y, QtGui.QPen(QtGui.QColor("black")))

    def add_person(self):
        dialog = PersonDialog(self)
        if dialog.exec_():
            person_data = dialog.get_data()
            person_name = person_data['name']  # Get the name entered in the dialog
            person_surname = person_data['surname']  # Get the surname entered in the dialog
            full_name = person_name + " " + person_surname  # Concatenate name and surname
            self.family_tree[full_name] = person_data  # Use the full name as the key in the family tree
            self.save_family_tree()
            self.populate_person_list()
            self.draw_family_tree()

    def clear_fields(self):
        self.name_edit.clear()
        self.generation_spinbox.setValue(0)
        self.index_spinbox.setValue(0)
        self.mom_edit.clear()
        self.dad_edit.clear()
        self.mom_mother_edit.clear()
        self.mom_father_edit.clear()
        self.dad_mother_edit.clear()
        self.dad_father_edit.clear()
        self.spouse_edit.clear()
        self.children_edit.clear()
        self.scene.clear()  # Clear the graphical representation

    def add_entry(self):
        name = self.name_edit.text()
        generation = self.generation_spinbox.value()
        index = self.index_spinbox.value()
        mom = self.mom_edit.text()
        dad = self.dad_edit.text()
        mom_mother = self.mom_mother_edit.text()
        mom_father = self.mom_father_edit.text()
        dad_mother = self.dad_mother_edit.text()
        dad_father = self.dad_father_edit.text()
        spouse = self.spouse_edit.text()
        children = self.children_edit.text()

        if name:
            self.family_tree[name] = {
                'name': name,
                'generation': generation,
                'index': index,
                'mom': mom,
                'dad': dad,
                'mom_parents': {'mom_mother': mom_mother, 'mom_father': mom_father},
                'dad_parents': {'dad_mother': dad_mother, 'dad_father': dad_father},
                'spouse': spouse.split(','),
                'children': children.split(',')
            }
            self.save_family_tree()
            self.populate_person_list()
            self.draw_family_tree()
            self.clear_fields()

    def select_person_for_deletion(self, item):
        selected_person = item.text()
        self.name_edit.setText(selected_person)

    def delete_selected(self):
        selected_person = self.name_edit.text()
        if selected_person in self.family_tree:
            del self.family_tree[selected_person]
            self.save_family_tree()
            self.populate_person_list()
            self.draw_family_tree()
            self.clear_fields()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Selected person not found in the family tree.")

    def update_selected(self):
        pass

    def search_entry(self):
        pass

    def view_all(self):
        pass

    def grow_tree(self):
        pass

class PersonDialog(QtWidgets.QDialog):
    person_saved = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Person")
        self.layout = QtWidgets.QFormLayout()

        self.name_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Name:", self.name_edit)

        self.surname_edit = QtWidgets.QLineEdit()  # Add a QLineEdit for entering the surname
        self.layout.addRow("Surname:", self.surname_edit)

        self.generation_spinbox = QtWidgets.QSpinBox()
        self.generation_spinbox.setMinimum(0)
        self.layout.addRow("Generation:", self.generation_spinbox)

        self.index_spinbox = QtWidgets.QSpinBox()
        self.index_spinbox.setMinimum(0)
        self.layout.addRow("Index:", self.index_spinbox)

        self.mom_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Mom:", self.mom_edit)

        self.dad_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Dad:", self.dad_edit)

        self.mom_mother_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Mom's Mother:", self.mom_mother_edit)

        self.mom_father_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Mom's Father:", self.mom_father_edit)

        self.dad_mother_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Dad's Mother:", self.dad_mother_edit)

        self.dad_father_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Dad's Father:", self.dad_father_edit)

        self.spouse_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Spouse:", self.spouse_edit)

        self.children_edit = QtWidgets.QLineEdit()
        self.layout.addRow("Children:", self.children_edit)

        self.buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.save_person)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)

        self.setLayout(self.layout)

    def save_person(self):
        person_data = {
            'name': self.name_edit.text(),
            'surname': self.surname_edit.text(),  # Get the surname from the surname_edit field
            'generation': self.generation_spinbox.value(),
            'index': self.index_spinbox.value(),
            'mom': self.mom_edit.text(),
            'dad': self.dad_edit.text(),
            'mom_parents': {'mom_mother': self.mom_mother_edit.text(), 'mom_father': self.mom_father_edit.text()},
            'dad_parents': {'dad_mother': self.dad_mother_edit.text(), 'dad_father': self.dad_father_edit.text()},
            'spouse': [spouse.strip() for spouse in self.spouse_edit.text().split(',')],
            'children': [child.strip() for child in self.children_edit.text().split(',')]
        }
        self.person_saved.emit(person_data)
        self.accept()

    def get_data(self):
        return {
            'name': self.name_edit.text(),
            'surname': self.surname_edit.text(),  # Include surname in the returned data
            'generation': self.generation_spinbox.value(),
            'index': self.index_spinbox.value(),
            'mom': self.mom_edit.text(),
            'dad': self.dad_edit.text(),
            'mom_parents': {'mom_mother': self.mom_mother_edit.text(), 'mom_father': self.mom_father_edit.text()},
            'dad_parents': {'dad_mother': self.dad_mother_edit.text(), 'dad_father': self.dad_father_edit.text()},
            'spouse': [spouse.strip() for spouse in self.spouse_edit.text().split(',')],
            'children': [child.strip() for child in self.children_edit.text().split(',')]
        }


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
