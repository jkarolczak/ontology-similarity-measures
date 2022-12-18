from owlready2 import *
from math import log
from . import utils


def shortest_path(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> float:
    return 2 * utils.longest_path(c1, c2) - utils.shortest_path(c1, c2)


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

