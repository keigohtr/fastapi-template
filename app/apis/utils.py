"""
Utils.
"""
from typing import List

from app import entities


def set_error_responses(status_codes: List[int]) -> dict:
    return {x: {"model": entities.Message} for x in status_codes}
