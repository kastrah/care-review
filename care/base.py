"""Shared data structures for the C.A.R.E. messaging review framework."""

from dataclasses import dataclass
from typing import List


@dataclass
class PrincipleResult:
    """Result of evaluating a single C.A.R.E. principle."""
    pass_: bool
    issues: List[str]
    fix_lever: str
