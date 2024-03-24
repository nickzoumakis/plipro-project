"""Κλάση Person: Αρχικοποιείται με όνομα name και 2 γονείς, αρχικά κενούς δείκτες"""
class Person():
    def __init__(self, name):
        self.name = name
        self.parents = {'dad' : None, 'mom' : None}

#ενδεικτικά γεμίζουμε με αριθμούς τους κόμβους
people = [str(i) for i in range(100, 256)]

#global μετρητές για να διατηρούν τις τιμές τους μεταξύ των διπλών αναδρομικών κλήσεων των συναρτήσεων
people_counter = 0
point_counter  = 0

#main συνάρτηση
def main():

    import pygraphviz as pgv
    
    #ορισμός πλήθους γενεών (βάθους δέντρου)
    generations = 5

    #κλήση της create_tree, βλ. παρακάτω
    root = create_tree(generations)

    #ορισμός του γραφήματος, το rankdir = ΒΤ δηλώνει ότι θα φτιαχτεί με κατεύθυνση bottom up
    graph = pgv.AGraph(rankdir="BT")

    #συνάρτηση create_graph
    create_graph_new(root, graph)

    #TODO: προσθήκη και άλλων παραμέτρων στο Person class για ένωση με αδέρφια
    #δοκιμαστική προσθήκη και ένωση Node αδερφιού 
    """sib = Person("CAT")
    graph.add_edge("2", sib.name)
    graph.add_subgraph([sib.name, "2"], rank = 'same')

    sib = Person("DOG")
    graph.add_edge(sib.name, "2")
    graph.add_subgraph([sib.name, "2"], rank = 'same')"""

    graph.layout(prog='dot')    #χρήση της dot μεθόδου απεικόνισης
    """Έξοδος προγράμματος: graph.gv->πηγαίο αρχείο graphviz, graph.png->εικόνα γραφήματος"""
    graph.write("graph.gv")
    graph.draw("graph.png")


"""Η create_graph μπαίνει στο δέντρο ξεκινώντας από το πρώτο πρόσωπο (το νεότερο μέλος) και δημιουργεί μία ακμή μεταξύ παιδιού και γονιού σε κάθε επίπεδο
    εφόσον υπάρχουν γονείς (δεν επιτρέπεται να γίνει ακμή προς/από None αντικείμενο). Μετά καλεί αναδρομικά τον εαυτό της για τον άλλο γονιό"""
def create_graph_old(person, graph):
    for parent in person.parents:
        if person.parents[parent]:
            graph.add_edge(person.name, person.parents[parent].name)
            create_graph_old(person.parents[parent], graph)


def create_graph_new(person, graph):
    if person.parents['dad']:
        global point_counter
        #δημιουργία σημείου ένωσης
        point = str(point_counter)
        graph.add_node(point, shape='point')
        #σύνδεση κόμβων γονιών μέσω του σημείου ένωσης
        graph.add_edge(person.name, point)
        graph.add_edge(point, person.parents['dad'].name)
        graph.add_edge(person.parents['mom'].name, point)
        # υποομάδα κόμβων  mom και dad για να είναι στο ίδιο επίπεδο
        if point_counter > 0:
            graph.add_subgraph([person.parents['dad'].name, person.parents['mom'].name], rank='same')
            #δημιουργία αόρατης ακμής για να εξασφαλιστεί η εμφάνιση κάθε κλαδιού στη σωστή μεριά
            graph.add_edge(person.parents['dad'].name, person.name, style='invis')
            graph.add_edge(person.parents['mom'].name, person.name, style='invis')
        else:
            graph.add_subgraph([person.parents['dad'].name, point, person.parents['mom'].name], rank='same')
        #επανάληψη για κάθε γονιό με αύξηση του point_counter
        for parent in person.parents:
            point_counter += 1
            create_graph_new(person.parents[parent], graph)

    
"""Κατασκευάζει αναδρομικά το δέντρο σα δομή στην Python"""
def create_tree(generations):
    #δήλωση ότι θα γίνει χρήση του global people_counter
    global people_counter
    #σε κάθε κλήση, δημιουργείται ένα node τύπου Person, με όνομα το εκάστοτε από τη λίστα people
    new_person = Person(people[people_counter])
    if generations > 1:     #για όσο δεν έχουμε φτάσει στο τέρμα του δέντρου
        for parent in new_person.parents:       #για κάθε γονιό του ατόμου που μόλις δημιουργήθηκε
            people_counter += 1                 #αύξηση του μετρητή ώστε η επόμενη κλήση να πάρει το επόμενο όνομα από τη λίστα
            new_person.parents[parent] = create_tree(generations - 1)       #ένωσε το γονιό με το node που θα φτιάξεις στην επόμενη κλήση
    return new_person 
    
    
if __name__ == '__main__':
    main()