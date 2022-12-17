import sys
from typing import List, Optional, Set, Tuple, Union

from owlready2 import *


def restriction_to_neighbours(r: owlready2.Restriction) -> List[owlready2.ThingClass]:
    if hasattr(r, "get_Classes"):
        return r.get_Classes()
    elif hasattr(r.value, "get_Classes"):
        return r.value.get_Classes()
    else:
        return [r.value]


def neighbours(c: owlready2.entity.ThingClass) -> Set[owlready2.entity.ThingClass]:
    neighbourhood = {c}
    for c_i in c.is_a:
        if isinstance(c_i, owlready2.ThingClass):
            neighbourhood.add(c_i)
        elif isinstance(c_i, owlready2.class_construct.Restriction):
            neighbourhood.update(restriction_to_neighbours(c_i))
        else:
            raise NotImplementedError(f"Finding neighbourhood of {type(c_i).__name__} is not yet supported")
    return neighbourhood.difference({owlready2.owl.Thing})


def longest_path(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass) -> int:
    pass


def _shortest(origin: owlready2.entity.ThingClass, target: owlready2.entity.ThingClass,
              path: Optional[List[owlready2.entity.ThingClass]] = None
              ) -> Tuple[List[owlready2.entity.ThingClass], bool]:
    if origin == target:
        return [*path, origin], True
    path = path or []
    path.append(origin)
    neighbourhood = neighbours(origin).difference(path)
    if not len(neighbourhood):
        return [*path, "dummy"], False
    else:
        paths = [_shortest(neighbour, target, path) for neighbour in neighbourhood]
        found_idx, found_len = None, sys.maxsize
        not_found_idx, not_found_len = None, sys.maxsize
        for idx, it_path in enumerate(paths):
            if target in it_path[0]:
                if len(it_path[0]) < found_len:
                    found_idx = idx
                    found_len = len(it_path[0])
            else:
                if len(it_path[0]) < not_found_len:
                    not_found_idx = idx
                    not_found_len = len(it_path[0])

        if found_idx is not None:
            return paths[found_idx][0], True
        return paths[not_found_idx][0], False


def shortest_path(c1: owlready2.entity.ThingClass, c2: owlready2.entity.ThingClass, return_path: bool = False
                  ) -> Union[int, List[owlready2.entity.ThingClass]]:
    p1, found1 = _shortest(c1, c2)
    p2, found2 = _shortest(c2, c1)
    if found1 or found2:
        if return_path:
            if len(p1) < len(p2):
                return p1
            else:
                return p2
        return min([len(p1), len(p2)])
    common = set(p1).intersection(set(p2))
    dist_min = sys.maxsize
    c_min = None
    for c in common:
        dist = p1.index(c) + p2.index(c) - 1
        if dist < dist_min:
            dist_min = dist
            c_min = c

    path = p1[:p1.index(c_min)] + p2[:p2.index(c_min) - 1][::-1]
    if return_path:
        return path
    else:
        return len(path)
