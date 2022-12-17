import owlready2
from owlready2 import *

from measures import utils


if __name__ == "__main__":
    onto = get_ontology("data/pizza.owl").load()
    with onto:
        sync_reasoner()
    pizza = onto.get_namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl")
    print(utils.shortest_path(pizza.SpicyPizza, pizza.Pizza, return_path=True))
    print(utils.shortest_path(pizza.SpicyPizza, pizza.Rosa, return_path=True))
