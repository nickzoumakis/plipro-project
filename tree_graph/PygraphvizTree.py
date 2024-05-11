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
        self.oldest_ancestors = None
        Person.all.append(self)


"""Class Graph: Σχεδιάζει το γενεαλογικό δέντρο"""
# TODO: να διαχωριστούν κάποιες δράσεις από την init για περισσότερο έλεγχο από το χρήστη κατά την αρχικοποίηση
class Graph:
    """init παίρνει το family_data, ανάλογα με την παράμετρο is_path που δόθηκε από το MainApp αναγνωρίζει 
    εάν πρόκειται για αρχείο json υπάρχοντος ή dict νέου γενεαλογικού δέντρου"""
    def __init__(self, family_data):
        # depths και youngest_descendants είναι global και χρησιμοποιούνται για να αποθηκεύουν τις τιμές των αναδρομικών συναρτήσεων διατηρώντας σταθερό το περιεχόμενό τους 
        self.depths = []
        self.youngest_descendants = []
        self.path = False
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
                
        # ταξινόμηση ανα γενιά
        self.sorted_all = self.all_people

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
                current.gender = data[id]['gender']
                current.dob = data[id]['date_of_birth']
                current.dod = data[id]['date_of_death']
                current.photo_path = data[id]['photo_path']
            else:
                # διαφορετικά βρίσκουμε το υπάρχον και το θέτουμε ως current
                all = current.all
                current = self.get_person(id, all)
            # δημιουργία γονιών
            # TODO: χάνεται το Photo path για τους γονείς
            parent_ids = (data[id]['mother_id'], data[id]['father_id'])
            parent_names = (f"{data[id]['mother_name']} {data[id]['mother_surname']}", 
                            f"{data[id]['father_name']} {data[id]['father_surname']}")
            parent_genders = ('female', 'male')
            for parent_id, parent_name, parent_gender in zip(parent_ids, parent_names, parent_genders):
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
                # σε κάθε περίπτωση, αν υπάρχουν γονείς, τους θέτουμε συζύγους
                person.parents[0].spouse = person.parents[1]
                person.parents[1].spouse = person.parents[0]

        # επιστροφή της λίστας όλων των ατόμων στη main
        return all


    """ Επιστρέφει το instance του ατόμου με το δεδομένο id """
    def get_person(self, id, all):
        id_list = [person.id for person in all]
        for i, person_id in enumerate(id_list):
            if person_id == id:
                return all[i]
            

    """ Επιστρέφει True αν τα Person1 και 2 είναι αδέρφια """        
    def are_siblings(self, person1, person2):
        for parent in person1.parents:
            if parent not in person2.parents:
                return False
        return True


    """traverse_down: βρίσκει σε πόσα βήματα ξεκινώντας από το 0 μπορούμε να φτάσουμε στη νεότερη
    γενιά (αυτή που δεν έχει παιδιά) από κάθε άτομο. Αποθηκεύει κάθε τιμή στη global λίστα depths.
    Στο τέλος, η μέγιστη τιμή της λίστας αυτής θα δώσει το ύψος του δέντρου (το πλήθος των γενεών)"""
    #TODO: να βελτιωθεί -> η αναδρομή μπορεί να παραλείπεται αν έχει ήδη εξερευνηθεί το μονοπάτι
    def traverse_down(self, person, count):
        # εφόσον υπάρχουν παιδιά
        for child in person.children:
            # πρόσθεση +1 βήματος προς τα κάτω
            self.depths.append(count + 1)
            # αναδρομική κλήση για κάθε παιδί με προσαυξημένο το μετρητή βημάτων
            self.traverse_down(child, count + 1)


    """assign_generations: αποδίδει αριθμό γενιάς σε κάθε άτομο που έχει δηλωθεί. Ορίσματα η λίστα με όλα
    τα άτομα και το συνολικό πλήθος των γενεών"""
    def assign_generations(self, people, max_depth):  
        # εύρεση πρώτα των νεότερων απογόνων
        # αρκεί να ψάξουμε τις διαδρομές από τους γηραιότερους, αυτούς που δεν έχουν γονείς
        oldest = [person for person in people if not person.parents]
        for person in oldest:
            self.youngest(person, 0, max_depth)

        # ορίζουμε τη γενιά των νεότερων απογόνων ως τη μέγιστη
        for person in set(self.youngest_descendants):     # χρήση set, το descendants έχει πολλές φορές τον κάθε νεότερο απόγονο αφού προσεγγίζονται και από τους 2 γονείς τους
            person.generation = max_depth

        # πηγαίνουμε προς τα πάνω από τους νεότερους απογόνους, μειώνοντας τη γενιά κατα 1 κάθε φορά 
        for person in set(self.youngest_descendants):
            for parent in person.parents:
                self.assign_generations_up(parent, max_depth - 1)
    

    """youngest: εύρεση των νεότερων απογόνων=>τα άτομα για τα οποία υπάρχει 
        μονοπάτι προς αυτά προς τα κάτω (μονοπάτι children) με τόσα βήματα 
        όσα και το σύνολο των γενεών""" 
    def youngest(self, person, count, generations):
        if count == generations:
            self.youngest_descendants.append(person)
        else:
            for child in person.children:
                # κίνηση προς παιδί (προς τα κάτω), ο μετρητής αυξάνεται
                self.youngest(child, count + 1, generations)


    """assign_generations_up: ανάθεση αριθμού γενιάς ξεκινώντας από τους νεότερους απογόνους που βρήκε η youngest 
        και πηγαίνοντας προς τα πάνω (μονοπάτι parents)"""
    def assign_generations_up(self, person, current_generation, is_sibling=False, is_spouse=False):
        if current_generation >= 0:
            person.generation = current_generation
            
        # ίδια γενιά για κάθε αδερφό 
        if not is_sibling:
            for sibling in person.siblings:
                sibling.generation = current_generation
                # θέτω την is_sibling προαιρετική παράμετρο True εφόσον βρίσκομαι σε αδερφό
                # διαφορετικά πέφτουμε σε infinite recursion loop (συνεχές μπρος πίσω μεταξύ αδερφών)
                self.assign_generations_up(sibling, current_generation, is_sibling=True)

        # ομοίως για συζύγους
        if person.spouse and not is_spouse:
            person.spouse.generation = current_generation
            self.assign_generations_up(person.spouse, current_generation, is_spouse=True)
        
        # περνάω στους γονείς μειώνοντας τη γενιά κατά 1
        for parent in person.parents:
            parent.generation = current_generation - 1
            self.assign_generations_up(parent, current_generation - 1)


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
        graph = pgv.AGraph(splines="true", ranksep="0.75", nodesep="2.0")
        graph.node_attr.update(shape="box", penwidth=2.0, fontsize="20")
        graph.edge_attr.update(penwidth=5.0)
        # κλήση draw με τη sorted_all λίστα
        filename = filename + '.png'
        _filepath = Path.cwd().parent / 'graph' / filename
        self.draw(graph, self.sorted_all, self.max_depth, _filepath)
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
        marriage_colors = ["red", "blue"]
        for person in people:
            graph.add_node(person.id, label=f"{person.name}", style="filled", fillcolor=node_fill[0] if person.gender=="male" else node_fill[1])
        # για κάθε γενιά
        while current_gen <= max_generation:
            # completed links λίστες εξαιρούν αδέρφια και συζύγους για να μη γίνονται πολλαπλές ενώσεις
            completed_spouse_links = []
            completed_sibling_links = []
            color_set = 0
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
                        name = person.name
                        spouse_id = person.spouse.id
                        spouse_name = person.spouse.name
                        # δημιουργία κόμβων και ακμών ένωσης γονιών
                        point = "point" + str(p_nodes)
                        link_left = "link" + str(id)
                        link_right = "link" + str(spouse_id)
                        # κόμβοι
                        graph.add_node(point, shape="circle", label="", height=0.01)
                        graph.add_node(link_left, shape="circle", label="", height=0.01)
                        graph.add_node(link_right, shape="circle", label="", height=0.01)
                        # ακμές
                        graph.add_edges_from([(link_left, point), (point, link_right)], color=marriage_colors[color_set % 2])
                        graph.add_subgraph([link_left, point, link_right], rank="same")
                        # σύνδεση link left & link right με κάθε σύζυγο
                        graph.add_edges_from([(id, link_left),(spouse_id, link_right)],  color=marriage_colors[color_set % 2], weight="10")         
                        # προσθήκη στη λίστα εξαιρέσεων
                        completed_spouse_links.append(person)
                        # αύξηση μετρητή σημείων ένωσης
                        p_nodes += 1
                        # αλλαγή χρώματος για την επόμενη ένωση
                        color_set +=1
                    # δημιουργία παιδιών
                    if person.parents and person not in completed_sibling_links:
                        # στοιχεία ατόμου που εξετάζεται
                        id = person.id
                        name = person.name
                        # εύρεση σημείου ένωσης γονιών του
                        parent_union = "point" + str(person.parents[0].own_union)
                        # εύρεση χρώματος σύνδεσης γονιών
                        for edge_tuple in graph.edges(parent_union):
                            color = graph.get_edge(*edge_tuple).attr['color']
                        # αν 1 παιδί, ένωση αμέσως
                        if not person.siblings:
                            # δημιουργία node σύνδεσης
                            sib = "sib" + str(sib_nodes)
                            graph.add_node(sib, shape="circle", label="", height=0.01)
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
                                graph.add_node(sib, shape="circle", label="", height=0.01)
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
            graph.layout(prog="dot")
            # προχωράμε στην επόμενη γενιά
            current_gen += 1

        # μετά την πρώτη σχεδίαση, κλήση της optimize_edges για διόρθωση κακών διασταυρώσεων
        self.optimize_edges(graph, people)
        # τελικό layout και σχεδίαση εικόνας
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
    def optimize_edges(self, graph, people):
        for person in people:
        # για κάθε σχεδιασμένο κόμβο συζύγων, λήψη συντεταγμένων κέντρου και σημείων ένωσης με αγκύλη
            if person.spouse:
                current = graph.get_node(person.id)
                current_spouse = graph.get_node(person.spouse.id)
                # εύρεση link κόμβου
                for node in (current, current_spouse):
                    for edge_tuple in graph.edges(node):
                        for edge in edge_tuple:
                            if 'link' in edge and node == current:
                                current_link = edge
                                # λήψη του χρώματος
                                color = graph.get_edge(*edge_tuple).attr['color']
                            elif 'link' in edge and node == current_spouse:
                                current_spouse_link = edge
                # συντεταγμένες x κάθε κόμβου
                x_link_curr = float(graph.get_node(current_link).attr['pos'].split(',')[0])
                x_link_curr_spouse = float(graph.get_node(current_spouse_link).attr['pos'].split(',')[0])
                x_curr =  float(graph.get_node(current).attr['pos'].split(',')[0])
                # αν η ανίσωση ισχύει, υπάρχει διασταύρωση των ακμών και γίνεται αντιστροφή τους
                if  abs(x_curr - x_link_curr) > abs(x_curr - x_link_curr_spouse):
                    # διαγραφή υπάρχουσας ένωσης
                    graph.remove_edges_from([(current, current_link), (current_spouse, current_spouse_link)])
                    # προσθήκη σωστών ενώσεων
                    graph.add_edges_from([(current, current_spouse_link), (current_spouse, current_link)], color=color)


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