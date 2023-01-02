from owlready2 import *

from measures import utils


def shortest_path(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    return 2 * (len(utils.longest_path(c1, c2)) - 1) - len(utils.shortest_path(c1, c2)) + 1


def normalized_shortest_path(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    return 1 - (len(utils.shortest_path(c1, c2)) - 1) / (len(utils.longest_path(c1, c2)) - 1)
