from owlready2 import *
from measures import resnik, lin

if __name__ == "__main__":
    onto = get_ontology("data/pizza_ext.owl").load()
    with onto:
        sync_reasoner()

    pizza = onto.get_namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl")

    print("all instances:", len(list(owl.Thing.instances())))
    print("Pizzas:", len(list(pizza.Pizza.instances())))
    print("Toppings:", len(list(pizza.PizzaTopping.instances())))

    c1, c2 = pizza.VegetarianPizza, pizza.VegetarianPizza
    print(c1.name, '|', c2.name)
    print(resnik(c1, c2))
    print(lin(c1, c2))

    print("======================")

    c1, c2 = pizza.VegetarianPizza, pizza.MeatyPizza
    print(c1.name, '|', c2.name)
    print(resnik(c1, c2))
    print(lin(c1, c2))

    print("======================")

    c1, c2 = pizza.VegetarianPizza, pizza.MeatyPizza
    print(c1.name, '|',  c2.name)
    print(resnik(c1, c2, pizza.Pizza))
    print(lin(c1, c2, pizza.Pizza))

    print("======================")

    c1, c2 = pizza.Capricciosa, pizza.American
    print(c1.name, '|',  c2.name)
    print(resnik(c1, c2, pizza.Pizza))
    print(lin(c1, c2, pizza.Pizza))

    print("======================")

    c1, c2 = pizza.Capricciosa, pizza.Veneziana
    print(c1.name, '|',  c2.name)
    print(resnik(c1, c2, pizza.Pizza))
    print(lin(c1, c2, pizza.Pizza))

