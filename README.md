# cross-origin-resource-sharing-matcher-utils

Validates and matches HTTP `Origin` and `Access-Control-Allow-Origin` header pairs per the CORS specification.

## Usage

```python
from cross_origin_resource_sharing_matcher_utils import is_origin_allowed, match_origin

# Exact match
assert is_origin_allowed("https://app.example", "https://app.example") is True
assert is_origin_allowed("https://app.example", "https://other.example") is False

# Wildcard allows any origin
assert is_origin_allowed("https://app.example", "*") is True
assert is_origin_allowed("null", "*") is True

# match_origin is an alias with identical behaviour
assert match_origin("https://app.example", "*") is True
```

## Why this library exists

The CORS check for `Access-Control-Allow-Origin` is small but easy to get subtly wrong: the wildcard `*` must match any origin (including the literal string `"null"`), the comparison is case-sensitive, and the header must contain either a single origin or `*` — not a list. This library provides a single, well-tested function for that check, so callers do not have to reimplement the logic or accidentally accept malformed headers.

The trade-off: we do not parse or normalize origins. Origins are compared as exact strings. This avoids pulling in a URL parser and avoids surprising equivalences (for example, `http://example.com` and `http://example.com:80` are different strings and will not match). If you need normalization, do it before calling these functions.

## Edge case you will hit

If the `Access-Control-Allow-Origin` header contains a comma-separated list of origins (which is invalid per the CORS spec), this library treats it as a literal string and will not match any single origin. Similarly, leading or trailing whitespace is not trimmed; the comparison is exact. This is deliberate: the library validates the header value as-is, and callers should ensure the header is well-formed.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

