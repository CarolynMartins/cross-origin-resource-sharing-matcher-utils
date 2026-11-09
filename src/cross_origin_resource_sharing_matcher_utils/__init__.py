"""Cross Origin Resource Sharing Matcher Utilities.

This package provides functions to validate and match HTTP Origin and
Access-Control-Allow-Origin header pairs according to the CORS specification.

Exported names:
    is_origin_allowed(origin, allow_origin) -> bool
    match_origin(origin, allow_origin) -> bool
"""

from .core import is_origin_allowed, match_origin

__all__ = ["is_origin_allowed", "match_origin"]
