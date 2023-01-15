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


def _get_relations(c: owlready2.Thing, return_dict: bool = False):
    relations = set() if not return_dict else dict()
    for property in c.get_properties():
        if return_dict:
            relations[property] = set()
        for source, target in property.get_relations():
            if source != c:
                continue
            target_concepts = tuple(target.is_a)
            if return_dict:
                relations[property].add((property, target_concepts))
            else:
                relations.add((property, target_concepts))
    return relations


def sim_tversky(c1: owlready2.entity.ThingClass,
        c2: owlready2.entity.ThingClass, alpha: float = 0.5) -> float:
    c1_relations, c2_relations = _get_relations(c1), _get_relations(c2)
    intersect = len(c1_relations.intersection(c2_relations))
    c1_diff = len(c1_relations.difference(c2_relations))
    c2_diff = len(c2_relations.difference(c1_relations))
    return intersect / (intersect + alpha * (c1_diff + c2_diff))


def sim_swsn(c1: owlready2.entity.ThingClass,
        c2: owlready2.entity.ThingClass, alpha: float = 0.5) -> float:
    c1_relations, c2_relations = _get_relations(c1, return_dict=True), _get_relations(c2, return_dict=True)
    properties = set(c1_relations.keys()).union(set(c2_relations.keys()))

    nominator = 0
    denominator = 0

    for property in properties:
        c1_rel, c2_rel = [rel[1][0] for rel in c1_relations[property]], [rel[1][0] for rel in c2_relations[property]]
        max_shape = max(len(c1_rel), len(c2_rel))
        information_matrix = np.full((max_shape, max_shape), 0, dtype=np.float32)

        c_top = property.range[0]
        max_instances = len(list(c_top.instances()))

        for idx_1, relation_1 in enumerate(c1_rel):
            for idx_2, relation_2 in enumerate(c2_rel):
                c_1, c_2 = relation_1, relation_2
                information_matrix[idx_1, idx_2] = -log(_most_informative_subsume(c_1, c_2, c_top, max_instances)[1])

        c1_rel += [c_top for _ in range(len(c1_rel), max_shape)]
        c2_rel += [c_top for _ in range(len(c2_rel), max_shape)]

        for _ in range(max_shape):
            c1_idx, c2_idx = np.unravel_index(np.argmax(information_matrix, axis=None), information_matrix.shape)
            information = information_matrix[c1_idx, c2_idx]
            information_matrix[c1_idx, :] = -np.inf
            information_matrix[:, c2_idx] = -np.inf

            c_1, c_2 = c1_rel[c1_idx], c2_rel[c2_idx]

            c1_p = _most_informative_subsume(c_1, c_1, c_top, max_instances)[1]
            c2_p = _most_informative_subsume(c_2, c_2, c_top, max_instances)[1]
            max_information = -log(min(c1_p, c2_p))

            nominator += information
            denominator += information + alpha * (max_information - information)

    if denominator == 0:
        raise ValueError("At least one of the instances must have non-zero number of relations")
    return round(nominator / denominator, 6)





