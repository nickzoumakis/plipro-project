from pathlib import Path
import pygraphviz as pgv
from PIL import Image

"""Class Person: Μέλος του γενεαλογικού δέντρου με τις ορισμένες σχέσεις συγγένειας. Το σύνολο των Person() αντικειμένων που έχουν δημιουργηθεί είναι 
    προσβάσιμο από οποιοδήποτε instance μέσω του person.all"""
class Person:
    all = []
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.gender = None
        self.dob = None
        self.dod = None
        self.children = []
        self.parents = []
        self.siblings = []
        self.spouse = None
        self.photo_path = ""
        self.generation = None
        self.own_union = None
        self.sibling_unions = []
        self.oldest_ancestors = None
        Person.all.append(self)


"""Class Graph: Σχεδιάζει το γενεαλογικό δέντρο"""
class Graph:
    """init παίρνει το family_data dict που δόθηκε από το MainApp"""
    def __init__(self, family_data):
        # depths και youngest_descendants είναι global και χρησιμοποιούνται για να αποθηκεύουν τις τιμές των αναδρομικών συναρτήσεων διατηρώντας σταθερό το περιεχόμενό τους 
        self.depths = []
        self.youngest_descendants = []
        # node_coordinates: dict με τις συντεταγμένες κάθε κόμβου
        self.node_coordinates = {}

        # φόρτωση δεδομένων μέσω της load_data
        self.all_people = self.load_data(family_data)

        # χρήση της traverse_down για την εύρεση όλων των πιθανών διαδρομών αναδρομικά από κάθε άτομο στα παιδιά του   
        for person in self.all_people:
            self.traverse_down(person, 0)

        # η μέγιστη τιμή του πίνακα depths δίνει το συνολικό ύψος του δέντρου (συνολικό πλήθος γενεών)
        self.max_depth = max(self.depths)

        # ανάθεση γενιάς σε κάθε άτομο - ορίζει το επίπεδο του δέντρου που θα τοποθετηθεί
        self.assign_generations(self.all_people, self.max_depth)
        
        # εύρεση παλαιότερων προγόνων κάθε ατόμου, με χρήση της global ancestors λίστας
        # TODO: να μπει σε ξεχωριστό method ?
        self.ancestors = []
        for person in self.all_people:
            self.oldest_ancestor(person)
            oldest = sorted(self.ancestors, key=lambda person:person.generation)
            # αποφυγή διπλοτύπων αν ο παλιότερος πρόγονος είναι το ίδιο το εξεταζόμενο άτομο
            if person != oldest[0] and person.spouse != oldest[0]:
                person.oldest_ancestors = [ancestor for ancestor in oldest if ancestor.generation == oldest[0].generation]
            self.ancestors.clear()
        
        #debug print for ancestors
        """for person in self.all_people:
            if person.oldest_ancestors:
                print(f'{person.name}, oldest ancestors:')
                for ancestor in person.oldest_ancestors:
                    print(f'{ancestor.name}')
                print("===============")
        print("====END====")"""
                

    """Φορτώνει το αρχείο json ή το dict με τις πληροφορίες συγγένειας από το χρήστη, φτιάχνει τα Person objects και επιστρέφει τη λίστα για τη σχεδίαση"""
    def load_data(self, family_data):
        # φορτώνει απευθείας το dict των νέων γενεαλογικών δεδομένων από το MainApp στο data
        data = family_data
        
        # pass 1: Δημιουργία Person αντικειμένων
        existing = []
        current = None
        for id in data:
            # αν δεν υπάρχει το id , δημιουργείται νέο Person
            if id not in existing:
                current = Person(id, f"{data[id]['name']} {data[id]['surname']}")
            else:
                # διαφορετικά βρίσκουμε το υπάρχον και το θέτουμε ως current
                all = current.all
                current = self.get_person(id, all)
            # συμπλήρωση δεδομένων από το dict data
            current.gender = data[id]['gender']
            current.dob = data[id]['date_of_birth']
            current.dod = data[id]['date_of_death']
            current.photo_path = data[id]['photo_path']
            # δημιουργία γονιών με έλεγχο αν έχουμε single mom / single dad
            parent_ids = (data[id]['mother_id'] if data[id]['mother_id'] else None, 
                          data[id]['father_id'] if  data[id]['father_id'] else None)
            parent_names = (f"{data[id]['mother_name']} {data[id]['mother_surname']}" if data[id]['mother_id'] else None, 
                            f"{data[id]['father_name']} {data[id]['father_surname']}" if  data[id]['father_id'] else None)
            parent_genders = ('female' if data[id]['mother_id'] else None, 
                              'male' if  data[id]['father_id'] else None)
            if parent_ids[0] or parent_ids[1]:
                for parent_id, parent_name, parent_gender in zip(parent_ids, parent_names, parent_genders):
                    if parent_id and parent_name and parent_gender:
                        if parent_id not in existing:
                            parent = Person(parent_id, parent_name)
                        else:
                            parent = self.get_person(parent_id, current.all)
                        # σύνδεση γονιού με παιδί και αντίστροφα
                        parent.gender = parent_gender
                        parent.children.append(current)
                        current.parents.append(parent)
            # ενημέρωση της existing με τα id όλων των αρχικοποιημένων Persons
            existing = [person.id for person in current.all]

        # pass 2: με γνωστούς τους γονείς και τα παιδιά κάθε ατόμου, απομένει η ανάθεση αδελφιών και συζύγων
        # περνάμε όλα τα επικαιροποιημένα Person αντικείμενα στην all μέσω της τελευταίας τιμής που πήρε η current στο πρώτο pass
        all = current.all
        for person in all:
            # αν δεν υπάρχουν γονείς, δεν έχει νόημα η αναζήτηση αδερφιών
            if person.parents:
                # για κάθε άλλο άτομο πέραν του εξεταζόμενου
                for other_person in all:
                    if other_person != person:
                        # αν έχουν κοινούς γονείς, είναι αδέρφια
                        if self.are_siblings(person, other_person):
                            person.siblings.append(other_person)
                # σε κάθε περίπτωση, αν υπάρχουν 2 γονείς, τους θέτουμε συζύγους
                if len(person.parents) == 2:
                    person.parents[0].spouse = person.parents[1]
                    person.parents[1].spouse = person.parents[0]

        # 3o pass για την εύρεση συζύγων χωρίς παιδιά
        for id in data:
            current = self.get_person(id, all)
            # αν δεν υπάρχει σύζυγος από γονεϊκή σχέση αλλά υπάρχει spouse_id στο json, έχουμε σύζυγο χωρίς τέκνα
            if not current.spouse and data[id]["spouse_id"]:
                spouse = self.get_person(data[id]["spouse_id"], all)
                if spouse:
                    current.spouse = spouse
                    spouse.spouse = current

        # επιστροφή της λίστας όλων των ατόμων στη main
        return all


    """ Επιστρέφει το instance του ατόμου με το δεδομένο id """
    def get_person(self, id, all):
        id_list = [person.id for person in all]
        for i, person_id in enumerate(id_list):
            if person_id == id:
                return all[i]
        return None
            

    """ Επιστρέφει True αν τα Person1 και 2 είναι αδέρφια """        
    def are_siblings(self, person1, person2):
        for parent in person1.parents:
            if parent not in person2.parents:
                return False
        return True


    """traverse_down: βρίσκει σε πόσα βήματα ξεκινώντας από το 0 μπορούμε να φτάσουμε στη νεότερη
    γενιά (αυτή που δεν έχει παιδιά) από κάθε άτομο. Αποθηκεύει κάθε τιμή στη global λίστα depths.
    Στο τέλος, η μέγιστη τιμή της λίστας αυτής θα δώσει το ύψος του δέντρου (το πλήθος των γενεών)"""
    def traverse_down(self, person, count):
        # εφόσον υπάρχουν παιδιά
        for child in person.children:
            # πρόσθεση +1 βήματος προς τα κάτω
            self.depths.append(count + 1)
            # αναδρομική κλήση για κάθε παιδί με προσαυξημένο το μετρητή βημάτων
            self.traverse_down(child, count + 1)
        self.depths.append(count)


    """assign_generations: αποδίδει αριθμό γενιάς σε κάθε άτομο που έχει δηλωθεί. Ορίσματα η λίστα με όλα
    τα άτομα και το συνολικό πλήθος των γενεών"""
    def assign_generations(self, people, max_depth):  
        # εύρεση πρώτα των νεότερων απογόνων
        # αρκεί να ψάξουμε τις διαδρομές από αυτούς που δεν έχουν γονείς
        oldest = [person for person in people if not person.parents]
        for person in oldest:
            self.youngest(person, 0, max_depth)

        # ορίζουμε τη γενιά των νεότερων απογόνων ως τη μέγιστη
        for person in set(self.youngest_descendants):     # χρήση set, το descendants έχει πολλές φορές τον κάθε νεότερο απόγονο αφού προσεγγίζονται και από τους 2 γονείς τους
            person.generation = max_depth

        # πηγαίνουμε προς τα πάνω από τους νεότερους απογόνους, μειώνοντας τη γενιά κατα 1 κάθε φορά
        current_generation = max_depth
        while current_generation >= 0:
            for person in people:
                if person.generation:
                    for sibling in person.siblings:
                        sibling.generation = person.generation
                    if person.spouse:
                        person.spouse.generation = person.generation
                    for parent in person.parents:
                        parent.generation = person.generation - 1
                    for child in person.children:
                        child.generation = person.generation + 1
            current_generation -= 1
    

    """youngest: εύρεση των νεότερων απογόνων=>τα άτομα για τα οποία υπάρχει 
        μονοπάτι προς αυτά προς τα κάτω (μονοπάτι children) με τόσα βήματα 
        όσα και το σύνολο των γενεών""" 
    def youngest(self, person, count, generations, is_spouse=False, is_sibling=False):
        if count == generations:
            self.youngest_descendants.append(person)
        else:
            # μετακινούμαστε προς τα αδέρφια χωρίς να αυξήσουμε το μετρητή αλλά θέτοντας is_sibling=True για αποφυγή infinite recursion loop
            if not is_sibling:
                for sibling in person.siblings:
                    self.youngest(sibling, count, generations, is_sibling=True)
                    
            # ομοίως για συζύγους
            if person.spouse and not is_spouse:
                self.youngest(person.spouse, count, generations, is_spouse=True)

            for child in person.children:
                # κίνηση προς παιδί (προς τα κάτω), ο μετρητής αυξάνεται
                self.youngest(child, count + 1, generations)


    """βρίσκει τον αρχαιότερο πρόγονο ενός ατόμου"""
    def oldest_ancestor(self, person):
        if person.parents:
            for parent in person.parents:
                self.oldest_ancestor(parent)
        else:
            self.ancestors.append(person)
            return


    """Σχεδιάζει το δέντρο μέσω του graphviz"""
    def show(self, filename, filepath):
        # αρχικοποιίηση του γραφήματος
        graph = pgv.AGraph(splines="ortho", ranksep="0.75", nodesep="2.0")
        graph.node_attr.update(shape="box", penwidth=2.0, fontsize="20")
        graph.edge_attr.update(penwidth=5.0)
        # κλήση draw με τη sorted_all λίστα
        filename = filename + '.png'
        _filepath = Path.cwd().parent / 'graph' / filename
        self.draw(graph, self.all_people, self.max_depth, _filepath)
        graph.layout(prog="dot")


    """draw: σχεδιάζει το δέντρο σε επίπεδα γενεών ξεκινώντας από το παλιότερο, διάφορες παράμετροι εδώ έχουν
        τεθεί με βάση το dot layout του graphviz"""
    # παραλλαγή με επιπλέον κόμβο για τους γονείς
    def draw(self, graph, people, max_generation, filepath):
        # p_nodes μετρητής σημείων ένωσης συζύγων/γονιών
        p_nodes = 0
        # sib_nodes μετρητής αόρατων κόμβων για τις ενώσεις
        sib_nodes = 0
        # ξεκινάμε από την παλιότερη γενιά
        current_gen = 0
        node_fill = ["cadetblue1", "lightpink"]
        # 2 χρώματα για κάθε γάμο
        marriage_colors = ["red", "blue", "purple"]
        for person in people:
            graph.add_node(person.id, label=f"{person.name}", style="filled", fillcolor=node_fill[0] if person.gender=="male" else node_fill[1])
        # για κάθε γενιά
        color_set = 3
        while current_gen <= max_generation:
            # completed links λίστες εξαιρούν αδέρφια και συζύγους για να μη γίνονται πολλαπλές ενώσεις
            completed_spouse_links = []
            completed_sibling_links = []
            # για κάθε άτομο 
            for person in people:
                if person.generation == current_gen:
                    # δημιουργία γονιών
                    if person.spouse and person.spouse not in completed_spouse_links:
                        # ανάθεση σημείου ένωσης γάμου
                        person.own_union = p_nodes
                        person.spouse.own_union = p_nodes
                        # λήψη στοιχείων
                        id = person.id
                        spouse_id = person.spouse.id
                        # δημιουργία κόμβων και ακμών ένωσης γονιών
                        point = "point" + str(p_nodes)
                        link_left = "link" + str(id)
                        link_right = "link" + str(spouse_id)
                        # κόμβοι
                        
                        # αλλαγή χρώματος σύνδεσης αν τύχει να είναι το ίδιο με το επιλεγμένο από τη λίστα (μόνο αν έχει ήδη κάποια ακμή κάποιος ή και οι 2 σύζυγοι)
                        if person.parents:
                            (person_parents_color, spouse_parents_color) = (None, None)
                            # εύρεση σημείου ένωσης γονιών του
                            person_parent_union = "point" + str(person.parents[0].own_union)
                            # εύρεση χρώματος σύνδεσης γονιών
                            for edge_tuple in graph.edges(person_parent_union):
                                person_parents_color = graph.get_edge(*edge_tuple).attr['color']
                            # αλλαγή του χρώματος της νέα σύνδεσης αν ταυτίζεται
                            if person_parents_color == marriage_colors[color_set % 3]:
                                color_set += 1
                            # εύρεση χρώματος σύνδεσης γονιών και για τη σύζυγο, αν υπάρχει
                            if person.spouse.parents:
                                spouse_parent_union = "point" + str(person.spouse.parents[0].own_union)
                                for edge_tuple in graph.edges(spouse_parent_union):
                                    spouse_parents_color = graph.get_edge(*edge_tuple).attr['color']
                                if spouse_parents_color == marriage_colors[color_set % 3]:
                                    color_set += 1

                            # αν και οι δύο σύζυγοι έχουν χρωματική σύνδεση, αλλάζω το χρώμα της μεταξύ τους ώστε να μην ταυτίζεται με κανένα από τα 2 προηγούμενα
                            if person_parents_color and spouse_parents_color:
                                while marriage_colors[color_set % 3] == person_parents_color or marriage_colors[color_set % 3] == spouse_parents_color:
                                    color_set += 1

                        graph.add_node(point, label="", height=0.05, width=0.05, style="filled", fillcolor=marriage_colors[color_set % 3], color=marriage_colors[color_set % 3])
                        graph.add_node(link_left, label="", height=0.05, width=0.05, style="filled", fillcolor=marriage_colors[color_set % 3], color=marriage_colors[color_set % 3])
                        graph.add_node(link_right, label="", height=0.05, width=0.05, style="filled", fillcolor=marriage_colors[color_set % 3], color=marriage_colors[color_set % 3])
                        # ακμές
                        graph.add_edges_from([(link_left, point), (point, link_right)], color=marriage_colors[color_set % 3])
                        graph.add_subgraph([link_left, point, link_right], rank="same")
                        # σύνδεση link left & link right με κάθε σύζυγο
                        graph.add_edges_from([(id, link_left),(spouse_id, link_right)],  color=marriage_colors[color_set % 3], weight="10")         
                        # προσθήκη στη λίστα εξαιρέσεων
                        completed_spouse_links.append(person)
                        # αύξηση μετρητή σημείων ένωσης
                        p_nodes += 1
                        # αλλαγή χρώματος για την επόμενη ένωση
                        color_set += 1
                        #graph.layout(prog="dot")
                        #graph.draw(filepath)
                    # περίπτωση single mom ή single dad
                    if person.children and not person.spouse:
                        person.own_union = p_nodes
                        id = person.id
                        point = "point" + str(p_nodes)
                        graph.add_node(point, label="", height=0.05, width=0.05, style="filled", fillcolor=marriage_colors[color_set % 3], color=marriage_colors[color_set % 3])
                        graph.add_edge(id, point,  color=marriage_colors[color_set % 3])
                        p_nodes += 1
                        color_set += 1
                    # δημιουργία παιδιών
                    if person.parents and person not in completed_sibling_links:
                        # στοιχεία ατόμου που εξετάζεται
                        id = person.id
                        # εύρεση σημείου ένωσης γονιών του
                        parent_union = "point" + str(person.parents[0].own_union)
                        # εύρεση χρώματος σύνδεσης γονιών
                        for edge_tuple in graph.edges(parent_union):
                            color = graph.get_edge(*edge_tuple).attr['color']
                        # αν 1 παιδί, ένωση αμέσως
                        if not person.siblings:
                            # δημιουργία node σύνδεσης
                            sib = "sib" + str(sib_nodes)
                            person.sibling_unions.append(sib_nodes)
                            graph.add_node(sib, label="", height=0.05, width=0.05, style="filled", fillcolor=color, color=color)
                            graph.add_edge(parent_union, sib, color=color)
                            graph.add_edge(sib, id, color=color)
                            sib_nodes += 1
                        # αν υπάρχουν αδέρφια
                        else:
                            even = False
                            inv_nodes = []
                            # λίστα με όλα τα αδέρφια συνολικά (+το εξεταζόμενο πρόσωπο)
                            all = [sibling.id for sibling in person.siblings]
                            all.append(id)
                            total = len(all)
                            if total % 2 == 0:
                                even = True
                                total = total + 1
                            # κόμβοι σύνδεσης
                            for _ in range(total):
                                sib = "sib" + str(sib_nodes)
                                graph.add_node(sib, label="", height=0.05, width=0.05, style="filled", fillcolor=color, color=color)
                                person.sibling_unions.append(sib_nodes)
                                for sibling in person.siblings:
                                    sibling.sibling_unions.append(sib_nodes)
                                inv_nodes.append(sib)
                                sib_nodes += 1
                            # σύνδεση κόμβων μεταξύ τους
                            for i in range(total - 1):
                                graph.add_edge(inv_nodes[i], inv_nodes[i + 1], color=color)
                            graph.add_subgraph(inv_nodes, rank="same")
                            if even:
                                # εξαίρεση μεσαίου στοιχείου από την ένωση αν έχουμε ζυγό πλήθος αδελφών (το μέσον της δομής μένει κενό)
                                bridge = inv_nodes.pop(total // 2)
                            # ένωση των κόμβων με κάθε αδερφό
                            for link, sibling in zip(inv_nodes, all):
                                graph.add_edge(link, sibling, color=color, weight="10")
                            # ένωση δομής με γονείς
                            if even:
                                graph.add_edge(parent_union, bridge, color=color, weight="10")
                            else:
                                graph.add_edge(parent_union, inv_nodes[len(inv_nodes) // 2], color=color, weight="10")
                            # εξαίρεση αδερφιών από μελλοντικές συνδέσεις
                            for sibling in person.siblings:
                                completed_sibling_links.append(sibling)
                        #graph.layout(prog="dot")
                        #graph.draw(filepath)
            graph.layout(prog="dot")
            # προχωράμε στην επόμενη γενιά
            current_gen += 1

        # μετά την πρώτη σχεδίαση, κλήση της optimize_edges για διόρθωση κακών διασταυρώσεων
        self.optimize_edges(graph, people, realign_spouses=True)
        #graph.layout(prog="dot")
        self.optimize_edges(graph, people, center=True)
        #graph.layout(prog="dot")
        self.optimize_edges(graph, people, realign_siblings=True)
        # τελικό layout και σχεδίαση εικόνας
        self.cleanup(graph)
        graph.layout(prog="dot")
        graph.draw(filepath)
        
        # με την εικόνα σχεδιασμένη, προχωράμε στην ανάκτηση των συντεταγμένων των κόμβων
        img = Image.open(filepath)
        # TODO: resize σε συγκεκριμένο μέγεθος ?
        height = img.height
        for node in graph.nodes():
            # δεν ενδιαφέρουν τα αόρατα nodes
            if graph.get_node(node).attr['label']:
                # αφαιρούμε την y από το ύψος της εικόνας αφού το graphviz μετράει ανάποδα τον άξονα y 
                self.node_coordinates[node] = (int(1.33 * (float(graph.get_node(node).attr['pos'].split(',')[0]))), height -  int(1.33 * (float(graph.get_node(node).attr['pos'].split(',')[1]))))
       

    """ελέγχει την ύπαρξη κακών διασταυρώσεων και τις επιλύνει"""
    def optimize_edges(self, graph, people, realign_spouses=False, center=False, realign_siblings=False):
        if realign_spouses:
            for person in people:
            # για κάθε σχεδιασμένο κόμβο συζύγων, λήψη συντεταγμένων κέντρου και σημείων ένωσης με αγκύλη
                if person.spouse:
                    current = graph.get_node(person.id)
                    current_spouse = graph.get_node(person.spouse.id)
                    # εύρεση link κόμβου
                    for node in (current, current_spouse):
                        for edge_tuple in graph.edges(node):
                            for edge_node in edge_tuple:
                                if 'link' in edge_node and node == current:
                                    current_link = edge_node
                                    # λήψη του χρώματος
                                    color = graph.get_edge(*edge_tuple).attr['color']
                                elif 'link' in edge_node and node == current_spouse:
                                    current_spouse_link = edge_node
                    # συντεταγμένες x κάθε κόμβου
                    x_link_curr = float(graph.get_node(current_link).attr['pos'].split(',')[0])
                    x_link_curr_spouse = float(graph.get_node(current_spouse_link).attr['pos'].split(',')[0])
                    x_curr =  float(graph.get_node(current).attr['pos'].split(',')[0])
                    # αν η ανίσωση ισχύει, υπάρχει διασταύρωση των ακμών και γίνεται αντιστροφή τους
                    if  abs(x_curr - x_link_curr) > abs(x_curr - x_link_curr_spouse):
                        try:
                            # διαγραφή υπάρχουσας ένωσης
                            graph.remove_edges_from([(current, current_link), (current_spouse, current_spouse_link)])
                            # προσθήκη σωστών ενώσεων
                            graph.add_edges_from([(current, current_spouse_link), (current_spouse, current_link)], color=color)
                            graph.layout(prog="dot")
                        except KeyError:
                            continue
        elif center:
            for person in people:
            # για κάθε σχεδιασμένο κόμβο συζύγων, λήψη συντεταγμένων κέντρου και σημείων ένωσης με αγκύλη
                if person.spouse:
                    current = graph.get_node(person.id)
                    current_spouse = graph.get_node(person.spouse.id)
                    current_point = graph.get_node("point" + str(person.own_union))
                    # εύρεση link κόμβου
                    for node in (current, current_spouse):
                        for edge_tuple in graph.edges(node):
                            for edge_node in edge_tuple:
                                if 'link' in edge_node and node == current:
                                    current_link = edge_node
                                    # λήψη του χρώματος
                                    color = graph.get_edge(*edge_tuple).attr['color']
                                elif 'link' in edge_node and node == current_spouse:
                                    current_spouse_link = edge_node
                    # συντεταγμένες x κάθε κόμβου
                    x_curr =  float(graph.get_node(current).attr['pos'].split(',')[0])
                    x_curr_spouse = float(graph.get_node(current_spouse).attr['pos'].split(',')[0])
                    x_current_point = float(graph.get_node(current_point).attr['pos'].split(',')[0])
                    # αν το κέντρο της αγκύλης έχει μετατοπιστεί δεξιότερα ή αριστερότερα , προσθέτουμε μια αόρατη ακμή για να το επαναφέρουμε στη θέση του
                    if x_current_point > x_curr and x_current_point > x_curr_spouse or x_current_point < x_curr and x_current_point < x_curr_spouse:
                        graph.add_edges_from([(current, current_point), (current_spouse, current_point)], color=color, style="invis")
                        graph.layout(prog="dot")
        elif realign_siblings:
            for person in people:
                if person.siblings:
                    # συντεταγμένη Χ κόμβου ατόμου
                    current = graph.get_node(person.id)
                    current_x = float(graph.get_node(current).attr['pos'].split(',')[0])
                    # εύρεση και λήψη του κόμβου sib (αγκύλη αδερφιών) που είναι τώρα ενωμένο το άτομο
                    for edge_tuple in graph.edges(current):
                        for edge_node in edge_tuple:
                            if 'sib' in edge_node:
                                curr_sib_link = edge_node
                                # λήψη του χρώματος
                                color = graph.get_edge(*edge_tuple).attr['color']
                    # συντεταγμένη Χ κόμβου sib
                    curr_sib_link_x = float(graph.get_node(curr_sib_link).attr['pos'].split(',')[0])
                    # λήψη όλων των κόμβων ένωσης με αδέρφια και τον αποστάσεων καθενός από το τωρινό
                    sib_nodes = [
                                    {
                                    'id': graph.get_node("sib" + str(sibling_union)),
                                    'dist': abs(float((graph.get_node("sib" + str(sibling_union)).attr['pos'].split(',')[0])) - current_x)
                                    }
                                  for sibling_union in person.sibling_unions
                                ]
                    # ταξινόμηση όλων των κόμβων sib με βάση την απόστασή τους Χ από το εξεταζόμενο
                    sib_nodes = sorted(sib_nodes, key=lambda node: node['dist'])
                    # εύρεση Χ συντεταγμένης του πλησιέστερου κόμβου sib στο current
                    if sib_nodes:
                        closest_sib_x = float(graph.get_node(sib_nodes[0]['id']).attr['pos'].split(',')[0])
                        # αν η απόσταση από τον τωρινά συνδεδεμένο κόμβο sib είναι μεγαλύτερη από την απόσταση του πιο κοντινού sib, έχει γίνει διασταύρωση
                        if abs(curr_sib_link_x - current_x) > abs(closest_sib_x - current_x):
                            try:
                                graph.remove_edge(curr_sib_link, current)
                                graph.add_edge(sib_nodes[0]['id'], current, color=color)
                                graph.layout(prog="dot")
                            except KeyError:
                                continue


    """καλείται μετά την optimize_edges για διαγραφή ορφανών συνδέσεων και κόμβων sib/link"""
    def cleanup(self, graph):
        for node_tuple in graph.edges():
            for edge_node in node_tuple:
                if 'link' in edge_node or 'sib' in edge_node:
                    if len(graph.edges(edge_node)) == 1:
                        graph.remove_edge(node_tuple)
                        graph.delete_node(edge_node)
                        graph.layout(prog="dot")


    """Methods για επικοινωνία με το MainApp"""
    """επιστρέφει τις συντεταγμένες κάθε κόμβου όταν κληθεί"""
    def send_coordinates(self):
        return self.node_coordinates


    """επιστρέφει τη λίστα με όλα τα Person objects"""
    def send_people(self):
        return self.all_people
    

    """καθαρίζει τη λίστα με τα Person objects, πρέπει να καλείται σε κάθε επανασχεδίαση δέντρου, αλλιώς έχουμε edge overlaps"""
    def delete_people(self):
        self.all_people.clear()


def main():
    g = Graph()
    g.show()
    
    
if __name__ == "__main__":
    main()
