"""Κλάση Person: Αρχικοποιείται με όνομα name και 2 γονείς, αρχικά κενούς δείκτες"""
class Person():
    def __init__(self, name):
        self.name = name
        self.parents = {'dad' : None, 'mom' : None}

#Αρχική λίστα προσώπων για 3 γενιές, είναι global για την ώρα, η σειρά παίζει ρόλο, βλ. create_tree
people = ['Nick Zoumakis', 'George Zoumakis', 'Nick Zoumakis\n(grandfather)',
              'Thalia Kikaki\n(grandmother)','Valia Serdaki' , 'Nick Serdakis\n(grandfather)',
              'Katerina Giatromanolaki\n(grandmother)']

#επίσης global μετρητής για να μπορεί η αναδρομική create_tree να διαπερνάει γραμμικά τη λίστα people σε κάθε αναδρομική κλήση
people_counter = 0

#main συνάρτηση
def main():

    import graphviz
    
    #ορισμός πλήθους γενεών (βάθους δέντρου)
    generations = 3

    #κλήση της create_tree, βλ. παρακάτω
    root = create_tree(generations)

    #ορισμός του γραφήματος, το rankdir = ΒΤ δηλώνει ότι θα φτιαχτεί με κατεύθυνση bottom up, το format καθορίζει ότι θα βγάλει εικόνα png
    g = graphviz.Graph(format='png', engine='dot', graph_attr={'rankdir': 'BT'})

    #συνάρτηση create_graph
    create_graph(root, g)

    #TODO: προσθήκη και άλλων παραμέτρων στο Person class για ένωση με αδέρφια
    #δοκιμαστική προσθήκη και ένωση Node αδερφιού στο ίδιο επίπεδο με το υφιστάμενο
    """sib = Person('Katerina Zoumaki')
    with g.subgraph(name = 'cluster_0', graph_attr={'peripheries':'0'}) as c: #με peripheries 0 το cluster δεν έχει ορατά όρια
        c.edge(root.name, sib.name, constraint = 'false')"""

    g.render()

"""Η create_graph μπαίνει στο δέντρο ξεκινώντας από το πρώτο πρόσωπο (το νεότερο μέλος) και δημιουργεί μία ακμή μεταξύ παιδιού και γονιού σε κάθε επίπεδο
    εφόσον υπάρχουν γονείς (δεν επιτρέπεται να γίνει ακμή προς/από None αντικείμενο). Μετά καλεί αναδρομικά τον εαυτό της για τον άλλο γονιό"""
def create_graph(person, graph):
    for parent in person.parents:
        if person.parents[parent]:
            graph.edge(person.name, person.parents[parent].name)    #τo graph.edge αρκεί για να δημιουργηθούν και να ενωθούν 2 Nodes ταυτόχρονα
            create_graph(person.parents[parent], graph)


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
    """το return new_person εξυπηρετεί 2 σκοπούς : -επιστρέφει node σε κάθε αναδρομική κλήση στην ίδια τη συνάρτηση ώστε να ξέρει τι να ενώσει με τι στο loop
                                                   -επιστρέφει στο τέλος στη main το νεότερο μέλος του δέντρου """
if __name__ == '__main__':
    main()