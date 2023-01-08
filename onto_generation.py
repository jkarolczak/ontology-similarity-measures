from owlready2 import *

if __name__ == "__main__":
    onto = get_ontology("data/pizza.owl").load()
    pizza = onto.get_namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl")

    with onto:
        sync_reasoner()

    for concept in pizza.Pizza.descendants():
        sub_concepts = list(concept.descendants())
        if len(sub_concepts) == 1:
            pizza_instance = concept(namespace=pizza)
            necessary_toppings = list(concept.hasTopping)
            toppings = []
            for topping in necessary_toppings:
                toppings.append(topping(namespace=pizza))
            pizza_instance.hasTopping = toppings

    onto.save(file='data/pizza_ext.owl')