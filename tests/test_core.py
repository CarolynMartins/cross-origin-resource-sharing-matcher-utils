import unittest

from cross_origin_resource_sharing_matcher_utils import (
    is_origin_allowed,
    match_origin,
)


class TestCorsMatcher(unittest.TestCase):
    def test_exact_match(self):
        self.assertTrue(is_origin_allowed("https://example.org", "https://example.org"))

    def test_exact_mismatch(self):
        self.assertFalse(is_origin_allowed("https://example.org", "https://other.org"))

    def test_wildcard_allows_any(self):
        self.assertTrue(is_origin_allowed("https://example.org", "*"))
        self.assertTrue(is_origin_allowed("null", "*"))
        self.assertTrue(is_origin_allowed("", "*"))

    def test_wildcard_does_not_match_empty_allow(self):
        self.assertFalse(is_origin_allowed("https://example.org", ""))

    def test_case_sensitive(self):
        self.assertFalse(is_origin_allowed("https://Example.org", "https://example.org"))

    def test_allow_origin_with_multiple_origins_is_not_supported(self):
        # The CORS spec allows only a single origin or '*'. We treat any
        # other value as a literal string, so a comma-separated list will
        # not match a single origin.
        self.assertFalse(is_origin_allowed("https://example.org", "https://example.org, https://other.org"))

    def test_match_origin_alias(self):
        self.assertTrue(match_origin("https://example.org", "https://example.org"))
        self.assertFalse(match_origin("https://example.org", "https://other.org"))
        self.assertTrue(match_origin("https://example.org", "*"))

    def test_empty_origin_with_exact_allow(self):
        self.assertTrue(is_origin_allowed("", ""))

    def test_null_origin_exact(self):
        self.assertTrue(is_origin_allowed("null", "null"))
        self.assertFalse(is_origin_allowed("null", "https://example.org"))

    def test_whitespace_is_not_trimmed(self):
        self.assertFalse(is_origin_allowed(" https://example.org", "https://example.org"))
        self.assertFalse(is_origin_allowed("https://example.org", " https://example.org"))


if __name__ == "__main__":
    unittest.main()
