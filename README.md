# word_boundary_detector

Splits natural language text into words using Unicode-aware rules that keep
apostrophes, hyphens, and combining marks attached to their base word.

```python
from word_boundary_detector import split_words

split_words("don't stop well-known")
# ['don't', 'stop', 'well-known']

split_words("caf\u0065\u0301")
# ['caf\u0065\u0301']
```

## Why this exists

The Python standard library exposes no public API for UAX #29 word
segmentation. A naive `str.split()` breaks `"don't"` into `"don"` and `"t"`, and
regex-based approaches either lose combining marks or require third-party
packages. This library implements a small, explicit rule set on top of
`unicodedata` so that the common English cases — contractions, hyphenated
compounds, accented letters — behave the way a reader expects.

The trade-off is deliberate: this is not a full UAX #29 implementation. It
classifies code points into word characters (letters, digits, combining marks)
and everything else, then keeps apostrophes and hyphens attached only when they
sit between two word characters. That covers the cases natural-language text
actually hits while staying dependency-free and predictable.

## The awkward edge

A joiner at the edge of a word is dropped. `"end-"` yields `["end"]`, and
`"'tis"` yields `["tis"]`, because there is no word character on both sides.
If you need to preserve those characters, post-process the input or the output.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

## Contributing

Issues and pull requests are welcome. Please keep the dependency list empty —
that constraint is the point of the project, not an oversight.

