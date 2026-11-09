"""Core logic for matching CORS Origin and Access-Control-Allow-Origin headers.

The implementation follows the CORS specification (Fetch Standard) for the
Access-Control-Allow-Origin header, with one deliberate simplification:
we treat the special value ``*`` as matching any origin, but we do not
implement the full origin serialization algorithm (e.g., we do not parse
or normalize origins). We compare the origin string exactly as provided.

Why the simplification? The brief asks for a small, focused library.
Origin parsing is a separate concern and would require a full URL parser
plus scheme/host/port normalization. By comparing strings exactly, we
avoid surprising behaviour (e.g., treating ``http://example.com`` and
``http://example.com:80`` as equal) and keep the function deterministic
and dependency-free.

Exported functions:
    is_origin_allowed(origin, allow_origin) -> bool
    match_origin(origin, allow_origin) -> bool
"""

from __future__ import annotations


def is_origin_allowed(origin: str, allow_origin: str) -> bool:
    """Return True if *origin* is allowed by *allow_origin*.

    This implements the CORS check for the Access-Control-Allow-Origin
    response header. The header may contain either a single origin or the
    wildcard ``*``. When the wildcard is present, any origin (including the
    literal string ``"null"`` or an empty string) is allowed.

    Args:
        origin: The origin from the request's Origin header.
        allow_origin: The value of the Access-Control-Allow-Origin header.

    Returns:
        True if the origin is allowed, False otherwise.

    Notes:
        - The comparison is case-sensitive and exact. Origins are typically
          lowercase, but we do not normalize them.
        - The wildcard ``*`` matches any origin, including ``"null"``.
        - If *allow_origin* is an empty string, no origin is allowed.
    """
    if allow_origin == "*":
        return True
    return origin == allow_origin


def match_origin(origin: str, allow_origin: str) -> bool:
    """Alias for :func:`is_origin_allowed`.

    Provided for callers who prefer the term "match" when checking CORS
    headers. The behaviour is identical.
    """
    return is_origin_allowed(origin, allow_origin)
