from math import log

import numpy as np
from owlready2 import *

from measures import utils


def shortest_path(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    return 2 * (len(utils.longest_path(c1, c2)) - 1) - len(utils.shortest_path(c1, c2)) + 1


def shortest_path_ratio(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    return 1 - (len(utils.shortest_path(c1, c2)) - 1) / (len(utils.longest_path(c1, c2)) - 1)


def sim_wp(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    subsumes_1, subsumes_2 = set(c1.ancestors()), set(c2.ancestors())
    subsumes = subsumes_1.intersection(subsumes_2).difference({owl.Thing})
    closest = None
    n1, n2 = np.inf, np.inf
    for s in subsumes:
        s1_dist = len(utils.shortest_path(c1, s))
        s2_dist = len(utils.shortest_path(c2, s))
        if s1_dist + s2_dist < n1 + n2:
            n1, n2 = s1_dist, s2_dist
            closest = s

    n_max = 1
    queue = [[a] for a in closest.ancestors().difference({owl.Thing})]
    while queue:
        current = queue.pop(0)
        n_max = max(n_max, len(current))
        for a in current[-1].ancestors().difference({*current, owlready2.Thing}):
            queue.append([*current, a])

    return (2 * n_max) / (n1 + n2 + 2 * n_max)


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


def resnik(c1: owlready2.entity.ThingClass,
           c2: owlready2.entity.ThingClass,
           c_top: owlready2.entity.ThingClass = owl.Thing) -> float:
    mis, p_mis = _most_informative_subsume(c1, c2, c_top)
    return -log(p_mis)


def lin(c1: owlready2.entity.ThingClass,
        c2: owlready2.entity.ThingClass,
        c_top: owlready2.entity.ThingClass = owl.Thing) -> float:
    n = len(list(c_top.instances()))
    mis, p_mis = _most_informative_subsume(c1, c2, c_top, n=n)
    p_c1, p_c2 = _c_prob(c1, c_top, n=n), _c_prob(c2, c_top, n=n)
    return 2 * log(p_mis) / (log(p_c1) + log(p_c2))
