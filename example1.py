from owlready2 import *

from measures import sim_wp, spad

if __name__ == "__main__":
    onto = get_ontology("data/pizza.owl").load()
    pizza = onto.get_namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl")
    with onto:
        sync_reasoner()

    print("sim wp, Pizza-Rosa", sim_wp(pizza.Pizza, pizza.Rosa))
    print("sim_wp, ParmaHamTopping-VegetarianPizza", sim_wp(pizza.ParmaHamTopping, pizza.VegetarianPizza))
    print("sim_wp, VegetarianPizza-VegetarianPizza", sim_wp(pizza.VegetarianPizza, pizza.VegetarianPizza))
    print("sim_wp, VegetarianPizza-MeatyPizza", sim_wp(pizza.VegetarianPizza, pizza.MeatyPizza))
    print("sim_wp, CheeseyPizza-CheeseTopping", sim_wp(pizza.CheeseyPizza, pizza.CheeseTopping))
    print("sim_wp, Capricciosa-Capricciosa", sim_wp(pizza.Capricciosa, pizza.Capricciosa))
    print("sim_wp, Capricciosa-American", sim_wp(pizza.Capricciosa, pizza.American))
    print("sim_wp, Capricciosa-Veneziana", sim_wp(pizza.Capricciosa, pizza.Veneziana))

    print("spad, Rosa-Rosa", spad(pizza.Rosa, pizza.Rosa))
    print("spad, Pizza-NamedPizza", spad(pizza.Pizza, pizza.NamedPizza))
    print("spad, Rosa-Pizza", spad(pizza.Rosa, pizza.Pizza))
    print("spad, Rosa-Capricciosa", spad(pizza.Rosa, pizza.Capricciosa))
    print("spad, Rosa-ParmaHamTopping", spad(pizza.Rosa, pizza.ParmaHamTopping))
    print("spad, VegatarianPizza-ParmaHamTopping", spad(pizza.VegetarianPizza, pizza.ParmaHamTopping))
    print("spad, CheeseyPizza-CheeseTopping", spad(pizza.CheeseyPizza, pizza.CheeseTopping))
