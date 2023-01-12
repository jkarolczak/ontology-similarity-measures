from math import log

import numpy as np
from owlready2 import *

from measures import utils


def shortest_path(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    return 2 * (len(utils.longest_path(c1, c2)) - 1) - len(utils.shortest_path(c1, c2)) + 1


def shortest_path_ratio(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    return 1 - (len(utils.shortest_path(c1, c2)) - 1) / (len(utils.longest_path(c1, c2)) - 1)


def sim_wp(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    ancestor, n1, n2 = utils.closest_ancestor(c1, c2)
    n_max = 1
    queue = [[a] for a in ancestor.ancestors().difference({owl.Thing})]
    while queue:
        current = queue.pop(0)
        n_max = max(n_max, len(current))
        for a in current[-1].ancestors().difference({*current, owlready2.Thing}):
            queue.append([*current, a])

    return (2 * n_max) / (n1 + n2 + 2 * n_max)


def spad(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    if c1 == c2:
        return 1
    ancestor, n1, n2 = utils.closest_ancestor(c1, c2)
    sp = len(utils.shortest_path(c1, c2)) - 1
    return 2 * np.log(1 / (((n1 + n2) / 2) * sp) + 1)


def _c_prob(c: owlready2.entity.ThingClass,
            c_top: owlready2.entity.ThingClass,
            n: int = None):
    if n is None:
        n = len(list(c_top.instances()))

    return len(list(c.instances())) / n


def _most_informative_subsume(c1: owlready2.entity.ThingClass,
                              c2: owlready2.entity.ThingClass,
                              c_top: owlready2.entity.ThingClass,
                              n: int = None):
    if n is None:
        n = len(list(c_top.instances()))

    subsumes_1, subsumes_2 = set(c1.ancestors()), set(c2.ancestors())
    subsumes = subsumes_1.intersection(subsumes_2)
    if len(subsumes) == 0:
        raise OwlReadyInconsistentOntologyError()

    mis = None
    p_mis = 1
    for subsume in subsumes:
        p = len(list(subsume.instances())) / n
        if p <= p_mis:
            mis = subsume
            p_mis = p

    return mis, p_mis


def sim_resnik(c1: owlready2.entity.ThingClass,
           c2: owlready2.entity.ThingClass,
           c_top: owlready2.entity.ThingClass = owl.Thing) -> float:
    mis, p_mis = _most_informative_subsume(c1, c2, c_top)
    return -log(p_mis)


def sim_lin(c1: owlready2.entity.ThingClass,
        c2: owlready2.entity.ThingClass,
        c_top: owlready2.entity.ThingClass = owl.Thing) -> float:
    n = len(list(c_top.instances()))
    mis, p_mis = _most_informative_subsume(c1, c2, c_top, n=n)
    p_c1, p_c2 = _c_prob(c1, c_top, n=n), _c_prob(c2, c_top, n=n)
    return 2 * log(p_mis) / (log(p_c1) + log(p_c2))


def _get_relations(c: owlready2.Thing) -> set:
    relations = set()
    for property in c.get_properties():
        for source, target in property.get_relations():
            if source != c:
                continue
            target_concepts = tuple(target.is_a)
            relations.add((property, target_concepts))
    return relations


def sim_tversky(c1: owlready2.entity.ThingClass,
        c2: owlready2.entity.ThingClass, alpha: float = 0.5) -> float:
    c1_relations, c2_relations = _get_relations(c1), _get_relations(c2)
    intersect = len(c1_relations.intersection(c2_relations))
    c1_diff = len(c1_relations.difference(c2_relations))
    c2_diff = len(c2_relations.difference(c1_relations))
    return intersect / (intersect + alpha * (c1_diff + c2_diff))