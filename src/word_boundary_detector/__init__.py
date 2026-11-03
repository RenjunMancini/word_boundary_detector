"""Word boundary detection for natural language text.

This package exposes a single public function, :func:`word_boundary_detector.split_words`,
which splits text into words using a Unicode-aware rule set that keeps apostrophes,
hyphens, and combining marks attached to their base word.
"""

from .core import split_words

__all__ = ["split_words"]
