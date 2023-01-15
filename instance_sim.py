from owlready2 import *
from measures import sim_tversky, sim_swsn

if __name__ == "__main__":
    onto = get_ontology("data/pizza_ext.owl").load()
    with onto:
        sync_reasoner()

    pizza = onto.get_namespace("http://www.co-ode.org/ontologies/pizza/pizza.owl")

    margherita = pizza.margherita1
    siciliana = pizza.siciliana1
    lareine = pizza.lareine1
    capricciosa = pizza.capricciosa1
    mushroom = pizza.mushroom1
    quattroformaggi = pizza.quattroformaggi1

    print("ingredients:")
    print("margherita:", margherita.hasTopping)
    print("quattro formaggi:", quattroformaggi.hasTopping)
    print("siciliana:", siciliana.hasTopping)
    print("lareine:", lareine.hasTopping)
    print("capricciosa:", capricciosa.hasTopping)
    print("mushroom:", mushroom.hasTopping)
    print("\n======================\n")

    print("margherita -> margherita")
    print("Tversky:", sim_tversky(margherita, margherita))
    print("SWSN:", sim_swsn(margherita, margherita))
    print("======================")

    print("margherita -> quattroformaggi")
    print("Tversky:", sim_tversky(margherita, quattroformaggi))
    print("SWSN:", sim_swsn(margherita, quattroformaggi))
    print("======================")

    print("margherita -> mushroom")
    print("Tversky:", sim_tversky(margherita, mushroom))
    print("SWSN:", sim_swsn(margherita, mushroom))
    print("======================")

    print("lareine -> mushroom")
    print("Tversky:", sim_tversky(lareine, mushroom))
    print("SWSN:", sim_swsn(lareine, mushroom))
    print("======================")

    print("siciliana -> capricciosa")
    print("Tversky:", sim_tversky(siciliana, capricciosa))
    print("SWSN:", sim_swsn(siciliana, capricciosa))
    print("======================")

    print("capricciosa -> mushroom")
    print("Tversky:", sim_tversky(capricciosa, mushroom))
    print("SWSN:", sim_swsn(capricciosa, mushroom))
    print("======================")