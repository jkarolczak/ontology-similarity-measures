from owlready2 import *

from measures import utils
from measures import shortest_path


if __name__ == "__main__":
    onto = get_ontology("data/pizza.owl").load()
    with onto:
        sync_reasoner()
    pizza = onto.get_namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl")
    print(shortest_path(pizza.Pizza, pizza.Rosa))
    print("shortest", utils.shortest_path(pizza.Pizza, pizza.Rosa, return_path=True))
    print("longest", utils.longest_path(pizza.Pizza, pizza.Rosa, return_path=True))