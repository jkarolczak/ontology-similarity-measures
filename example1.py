from owlready2 import *

from measures import shortest_path, shortest_path_ratio, sim_wp

if __name__ == "__main__":
    onto = get_ontology("data/pizza.owl").load()
    pizza = onto.get_namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl")
    with onto:
        sync_reasoner()
    print("shortest path", shortest_path(pizza.Pizza, pizza.Rosa))
    print("shortest path (ratio)", shortest_path_ratio(pizza.Pizza, pizza.Rosa))
    print("sim wp", sim_wp(pizza.Pizza, pizza.Rosa))
    print("shortest path", shortest_path(pizza.ParmaHamTopping, pizza.VegetarianPizza))
    print("shortest path (ratio)", shortest_path_ratio(pizza.ParmaHamTopping, pizza.VegetarianPizza))
    print("sim_wp", sim_wp(pizza.ParmaHamTopping, pizza.VegetarianPizza))
    print("sim_wp", sim_wp(pizza.VegetarianPizza, pizza.VegetarianPizza))
    print("sim_wp", sim_wp(pizza.VegetarianPizza, pizza.MeatyPizza))
    print("sim_wp", sim_wp(pizza.CheeseyPizza, pizza.CheeseTopping))
    print("sim_wp", sim_wp(pizza.Capricciosa, pizza.Capricciosa))
    print("sim_wp", sim_wp(pizza.Capricciosa, pizza.American))
