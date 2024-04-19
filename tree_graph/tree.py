from pathlib import Path
import pygraphviz as pgv
from json import load
from random import shuffle

"""Class Person: Μέλος του γενεαλογικού δέντρου με τις ορισμένες σχέσεις συγγένειας. Αποδίδεται 
    μοναδικός κωδικός μέσω του unique_id και το σύνολο των Person() αντικειμένων που έχουν δημιουργηθεί είναι 
    προσβάσιμο από οποιοδήποτε instance μέσω του person.all"""
class Person:
    all = []
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.gender = None
        self.children = []
        self.parents = []
        self.siblings = []
        self.spouse = None
        self.generation = None
        self.own_union = None
        Person.all.append(self)

# globals
depths = []
youngest_descendants = []

def main():

    # path στο json με τα περιεχόμενα συγγένειας
    path = Path.cwd().parent / 'data/data2.json'
    
    # δημιουργία σχέσεων συγγένειας

    # πέρασμα όλων των προσώπων στη μεταβλητή people
    all_people = load_data(path)

    # χρήση της traverse_down για την εύρεση όλων των πιθανών διαδρομών αναδρομικά από κάθε άτομο στα παιδιά του   
    for person in all_people:
        traverse_down(person, 0)

    # η μέγιστη τιμή του πίνακα depths δίνει το συνολικό ύψος του δέντρου (συνολικό πλήθος γενεών)
    max_depth = max(depths)

    # ανάθεση γενιάς σε κάθε άτομο - ορίζει το επίπεδο του δέντρου που θα τοποθετηθεί
    assign_generations(all_people, max_depth)

    # αρχικοποιίηση του γραφήματος
    graph = pgv.AGraph(splines="ortho", ranksep="0.75", nodesep="2.0")
    graph.node_attr.update(shape="box", penwidth=2.0, fontsize="20")
    graph.edge_attr.update(penwidth=5.0)
    #shuffle(all_people)
    draw(graph, sorted(all_people, key=lambda person:person.generation), max_depth)
    graph.layout(prog="dot")


""" Φορτώνει το αρχείο json με τις πληροφορίες συγγένειας και επιστρέφει
    τη λίστα με τα ολοκληρωμένα person objects"""
def load_data(json_path):
    # load json
    with open(json_path) as input_file:
        data = load(input_file)
    
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
            current = get_person(id, all)
        # δημιουργία γονιών
        parent_ids = (data[id]['mother_id'], data[id]['father_id'])
        parent_names = (f"{data[id]['mother_name']} {data[id]['mother_surname']}", 
                        f"{data[id]['father_name']} {data[id]['father_surname']}")
        parent_genders = ('female', 'male')
        for parent_id, parent_name, parent_gender in zip(parent_ids, parent_names, parent_genders):
            if parent_id not in existing:
                parent = Person(parent_id, parent_name)
            else:
                parent = get_person(parent_id, current.all)
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
                    if are_siblings(person, other_person):
                        person.siblings.append(other_person)
            # σε κάθε περίπτωση, αν υπάρχουν γονείς, τους θέτουμε συζύγους
            person.parents[0].spouse = person.parents[1]
            person.parents[1].spouse = person.parents[0]

    # επιστροφή της λίστας όλων των ατόμων στη main
    return all


""" Επιστρέφει το instance του ατόμου με το δεδομένο id """
def get_person(id, all):
    id_list = [person.id for person in all]
    for i, person_id in enumerate(id_list):
        if person_id == id:
            return all[i]
        

""" Επιστρέφει True αν τα Person1 και 2 είναι αδέρφια """        
def are_siblings(person1, person2):
    for parent in person1.parents:
        if parent not in person2.parents:
            return False
    return True


"""traverse_down: βρίσκει σε πόσα βήματα ξεκινώντας από το 0 μπορούμε να φτάσουμε στη νεότερη
    γενιά (αυτή που δεν έχει παιδιά) από κάθε άτομο. Αποθηκεύει κάθε τιμή στη global λίστα depths.
    Στο τέλος, η μέγιστη τιμή της λίστας αυτής θα δώσει το ύψος του δέντρου (το πλήθος των γενεών)"""
#TODO: να βελτιωθεί -> η αναδρομή μπορεί να παραλείπεται αν έχει ήδη εξερευνηθεί το μονοπάτι
def traverse_down(person, count):
    # εφόσον υπάρχουν παιδιά
    for child in person.children:
        global depths
        # πρόσθεση +1 βήματος προς τα κάτω
        depths.append(count + 1)
        # αναδρομική κλήση για κάθε παιδί με προσαυξημένο το μετρητή βημάτων
        traverse_down(child, count + 1)


"""assign_generations: αποδίδει αριθμό γενιάς σε κάθε άτομο που έχει δηλωθεί. Ορίσματα η λίστα με όλα
    τα άτομα και το συνολικό πλήθος των γενεών"""
def assign_generations(people, max_depth):
    global youngest_descendants
    
    # εύρεση πρώτα των νεότερων απογόνων
    # αρκεί να ψάξουμε τις διαδρομές από τους γηραιότερους, αυτούς που δεν έχουν γονείς
    oldest = [person for person in people if not person.parents]
    for person in oldest:
        youngest(person, 0, max_depth)

    # ορίζουμε τη γενιά των νεότερων απογόνων ως τη μέγιστη
    for person in set(youngest_descendants):     # χρήση set, το descendants έχει πολλές φορές τον κάθε νεότερο απόγονο αφού προσεγγίζονται και από τους 2 γονείς τους
        person.generation = max_depth

    # go up the parent ladder for each person, assigning max gen - 1 
    for person in set(youngest_descendants):
        for parent in person.parents:
            assign_generations_up(parent, max_depth - 1)
    

"""youngest: εύρεση των νεότερων απογόνων=>τα άτομα για τα οποία υπάρχει 
    μονοπάτι προς αυτά προς τα κάτω (μονοπάτι children) με τόσα βήματα 
    όσα και το σύνολο των γενεών""" 
def youngest(person, count, generations):
    if count == generations:
        youngest_descendants.append(person)
    else:
        for child in person.children:
            # κίνηση προς παιδί (προς τα κάτω), ο μετρητής αυξάνεται
            youngest(child, count + 1, generations)


"""assign_generations_up: ανάθεση αριθμού γενιάς ξεκινώντας από τους νεότερους απογόνους που βρήκε η youngest 
    και πηγαίνοντας προς τα πάνω (μονοπάτι parents)"""
def assign_generations_up(person, current_generation, is_sibling=False, is_spouse=False):
    if current_generation >= 0:
        person.generation = current_generation
        
    # ίδια γενιά για κάθε αδερφό 
    if not is_sibling:
        for sibling in person.siblings:
            sibling.generation = current_generation
            # θέτω την is_sibling προαιρετική παράμετρο True εφόσον βρίσκομαι σε αδερφό
            # διαφορετικά πέφτουμε σε infinite recursion loop (συνεχές μπρος πίσω μεταξύ αδερφών)
            assign_generations_up(sibling, current_generation, is_sibling=True)

    # ομοίως για συζύγους
    if person.spouse and not is_spouse:
        person.spouse.generation = current_generation
        assign_generations_up(person.spouse, current_generation, is_spouse=True)
    
    # περνάω στους γονείς μειώνοντας τη γενιά κατά 1
    for parent in person.parents:
        parent.generation = current_generation - 1
        assign_generations_up(parent, current_generation - 1)


"""draw: σχεδιάζει το δέντρο σε επίπεδα γενεών ξεκινώντας από το παλιότερο, διάφορες παράμετροι εδώ έχουν
    τεθεί με βάση το dot layout του graphviz"""
# παραλλαγή με επιπλέον κόμβο για τους γονείς
def draw(graph, people, max_generation):
    # p_nodes μετρητής σημείων ένωσης συζύγων/γονιών
    p_nodes = 0
    # sib_nodes μετρητής αόρατων κόμβων για τις ενώσεις
    sib_nodes = 0
    # ξεκινάμε από την παλιότερη γενιά
    current_gen = 0
    node_fill = ["cadetblue1", "lightpink"]
    # 2 χρώματα για κάθε γάμο
    marriage_colors = ["red", "chartreuse"]
    for person in people:
        graph.add_node(person.id, label=f"{person.name}", style="filled", fillcolor=node_fill[0] if person.gender=="male" else node_fill[1])
    # για κάθε γενιά
    while current_gen <= max_generation:
        # completed links λίστες εξαιρούν αδέρφια και συζύγους για να μη γίνονται πολλαπλές ενώσεις
        completed_spouse_links = []
        completed_sibling_links = []
        is_red = True
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
                    graph.add_node(point, shape="point")
                    graph.add_node(link_left, shape="circle", style="filled", fillcolor=marriage_colors[0] if is_red else marriage_colors[1],
                                   label="", height=0.05, color=marriage_colors[0] if is_red else marriage_colors[1])
                    graph.add_node(link_right, shape="circle", style="filled", fillcolor=marriage_colors[0] if is_red else marriage_colors[1], 
                                   label="", height=0.05, color=marriage_colors[0] if is_red else marriage_colors[1])
                    # ακμές
                    graph.add_edge(link_left, point, color=marriage_colors[0] if is_red else marriage_colors[1])
                    graph.add_edge(point, link_right, color=marriage_colors[0] if is_red else marriage_colors[1])
                    graph.add_subgraph([link_left, point, link_right], rank="same")
                    # σύνδεση link left & link right με κάθε σύζυγο
                    graph.add_edge(spouse_id, link_right, color=marriage_colors[0] if is_red else marriage_colors[1])
                    graph.add_edge(id, link_left, color=marriage_colors[0] if is_red else marriage_colors[1])
                    # προσθήκη στη λίστα εξαιρέσεων
                    completed_spouse_links.append(person)
                    # αύξηση μετρητή σημείων ένωσης
                    p_nodes += 1
                    # αλλαγή χρώματος για την επόμενη ένωση
                    if is_red:
                        is_red = False
                # δημιουργία παιδιών
                if person.parents and person not in completed_sibling_links:
                    # στοιχεία ατόμου που εξετάζεται
                    id = person.id
                    name = person.name
                    # εύρεση σημείου ένωσης γονιών του
                    parent_union = "point" + str(person.parents[0].own_union)
                    # αν 1 παιδί, ένωση αμέσως
                    if not person.siblings:
                        # δημιουργία node σύνδεσης
                        sib = "sib" + str(sib_nodes)
                        graph.add_node(sib, label="", height=0.01, width=0.01)
                        graph.add_edge(parent_union, sib, color="blue")
                        graph.add_edge(sib, id, color="blue")
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
                            graph.add_node(sib, label="", height=0.01, width=0.01)
                            inv_nodes.append(sib)
                            sib_nodes += 1
                        # σύνδεση κόμβων μεταξύ τους
                        for i in range(total - 1):
                            graph.add_edge(inv_nodes[i], inv_nodes[i + 1], color="blue")
                        graph.add_subgraph(inv_nodes, rank="same")
                        if even:
                            # εξαίρεση μεσαίου στοιχείου από την ένωση αν έχουμε ζυγό πλήθος αδελφών (το μέσον της δομής μένει κενό)
                            bridge = inv_nodes.pop(total // 2)
                        # ένωση των κόμβων με κάθε αδερφό
                        for link, sibling in zip(inv_nodes, all):
                            graph.add_edge(link, sibling, color="blue")
                        # ένωση δομής με γονείς
                        if even:
                            graph.add_edge(parent_union, bridge, color="blue")
                        else:
                            graph.add_edge(parent_union, inv_nodes[len(inv_nodes) // 2], color="blue")
                        # εξαίρεση αδερφιών από μελλοντικές συνδέσεις
                        for sibling in person.siblings:
                            completed_sibling_links.append(sibling)

        # προχωράμε στην επόμενη γενιά
        current_gen += 1
    graph.layout(prog="dot")
    #graph.write("tree_new_default.dot")
    graph.draw("tree_new_default.png")


if __name__ == "__main__":
    main()