from itertools import chain
from typing import List

from ._types import SubmissionsType


def validate_cik(cik: str) -> str:
    cik = str(cik).strip().zfill(10)

    if not is_cik(cik):
        raise ValueError(
            "Invalid CIK. Please enter an valid SEC CIK at most 10 digits long."
        )

    return cik


def is_cik(cik: str) -> bool:
    try:
        int(cik)
        return 1 <= len(cik) <= 10
    except ValueError:
        return False


def merge_submission_dicts(to_merge: List[SubmissionsType]) -> SubmissionsType:
    """Merge dictionaries with same keys."""
    merged = {}
    for k in to_merge[0].keys():
        merged[k] = list(chain.from_iterable(d[k] for d in to_merge))
    return merged
