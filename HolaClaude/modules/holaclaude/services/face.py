import math
from typing import List


FACE_MATCH_THRESHOLD = 0.5


def euclidean_distance(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        return 999.0
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def is_same_face(stored: List[float], candidate: List[float]) -> bool:
    return euclidean_distance(stored, candidate) < FACE_MATCH_THRESHOLD


def validate_descriptor(desc) -> bool:
    if not isinstance(desc, list) or len(desc) != 128:
        return False
    return all(isinstance(x, (int, float)) for x in desc)
