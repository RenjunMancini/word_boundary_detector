"""Unicode-aware word segmentation.

The Python standard library has no public API for UAX #29 word boundaries, so this
module implements a small, explicit rule set that covers the cases natural-language
text actually hits: apostrophes, hyphens, combining marks, and punctuation.

The design choice is deliberately conservative. Rather than trying to implement the
full UAX #29 state machine (which is large and changes between Unicode versions),
we classify code points into a handful of categories and apply a fixed set of rules.
That keeps the behaviour predictable and testable, at the cost of not matching every
corner of the Unicode specification.
"""

from __future__ import annotations

import unicodedata
from typing import Iterator, List

__all__ = ["split_words"]

# Characters that are treated as word-internal when they appear between two word
# characters. These are the punctuation marks that English and many other
# apostrophe-using languages rely on.
_APOSTROPHES = frozenset("\u0027\u2019\u02bc\u2018")

# Hyphen-like characters that join two word characters into one token.
_HYPHENS = frozenset("\u002d\u2010\u2011\u2012\u2013\u2014")


def _is_word_char(ch: str) -> bool:
    """Return True if *ch* is a letter, digit, or combining mark.

    Combining marks are included because a base letter followed by a combining
    mark is a single grapheme and must not be split.
    """
    cat = unicodedata.category(ch)
    if cat[0] in ("L", "N"):
        return True
    return cat in ("Mn", "Mc", "Me")


def _is_joiner(ch: str) -> bool:
    """Return True if *ch* can join two word characters into one token."""
    return ch in _APOSTROPHES or ch in _HYPHENS


def _iter_tokens(text: str) -> Iterator[str]:
    """Yield alternating word and non-word tokens from *text*.

    A token is either a maximal run of word characters (with internal joiners and
    combining marks) or a maximal run of non-word characters.
    """
    n = len(text)
    i = 0
    while i < n:
        ch = text[i]
        if _is_word_char(ch):
            start = i
            i += 1
            while i < n:
                cur = text[i]
                if _is_word_char(cur):
                    i += 1
                elif _is_joiner(cur) and i + 1 < n and _is_word_char(text[i + 1]):
                    # Keep the joiner and the following word character together.
                    i += 2
                else:
                    break
            yield text[start:i]
        else:
            start = i
            i += 1
            while i < n and not _is_word_char(text[i]):
                i += 1
            yield text[start:i]


def _has_word_char(token: str) -> bool:
    """Return True if *token* contains at least one word character."""
    return any(_is_word_char(ch) for ch in token)


def split_words(text: str) -> List[str]:
    """Split *text* into a list of word tokens.

    The function returns only tokens that contain at least one word character;
    runs of whitespace and punctuation are discarded. Apostrophes and hyphens are
    kept attached to the surrounding word when they sit between two word
    characters, so ``"don't"`` and ``"well-known"`` each yield a single token.

    A trailing joiner is not attached: ``"end-"`` yields ``"end"``, because there
    is no following word character to join to.
    """
    return [tok for tok in _iter_tokens(text) if _has_word_char(tok)]
