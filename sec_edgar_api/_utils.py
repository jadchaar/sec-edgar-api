from itertools import chain
from typing import List

from ._types import SubmissionsType


def validate_cik(func):
    def wrapper(*args, **kwargs):
        cik = str(kwargs["cik"] if "cik" in kwargs else args[1])

        if not is_cik(cik) or len(cik) > 10:
            raise ValueError(
                "Invalid CIK. Please enter an valid SEC CIK at most 10 digits long."
            )

        return func(*args, **kwargs)

    return wrapper


def is_cik(cik: str) -> bool:
    try:
        int(cik)
        return True
    except ValueError:
        return False


def merge_dicts_with_identical_keys(to_merge: List[SubmissionsType]) -> SubmissionsType:
    """Merge dictionaries with same keys."""
    merged = {}
    for k in to_merge[0].keys():
        merged[k] = list(chain.from_iterable(d[k] for d in to_merge))
    return merged
