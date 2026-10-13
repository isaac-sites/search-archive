"""Source-level sitemap/robots hygiene falsifiers for search-archive.

The /cors-test/ diagnostic page must not be advertised to crawlers: no
<url> block for it in sitemap.xml, and the page itself carries a
``noindex`` robots meta.  The archive-search tool surface (root
index.html) stays indexable — it must NOT carry a noindex meta.
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SITEMAP = REPO_ROOT / "sitemap.xml"
CORS_TEST_PAGE = REPO_ROOT / "cors-test" / "index.html"
ROOT_PAGE = REPO_ROOT / "index.html"

_LOC_RE = re.compile(r"<loc>\s*([^<]+?)\s*</loc>")
_ROBOTS_NOINDEX_RE = re.compile(
    r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex',
    re.IGNORECASE,
)


class SitemapHygieneTests(unittest.TestCase):
    def test_sitemap_has_no_cors_test_loc(self):
        locs = _LOC_RE.findall(SITEMAP.read_text(encoding="utf-8"))
        cors = [loc for loc in locs if "/cors-test" in loc]
        self.assertEqual(cors, [], f"cors-test still declared: {cors}")

    def test_sitemap_remains_valid_and_lists_root(self):
        text = SITEMAP.read_text(encoding="utf-8")
        self.assertIn("<urlset", text)
        self.assertIn("</urlset>", text)
        locs = _LOC_RE.findall(text)
        self.assertIn("https://search-archive.isaackoi.com/", locs)

    def test_cors_test_page_carries_noindex(self):
        html = CORS_TEST_PAGE.read_text(encoding="utf-8")
        self.assertRegex(
            html,
            _ROBOTS_NOINDEX_RE,
            "cors-test/index.html lacks a noindex robots meta",
        )

    def test_root_page_stays_indexable(self):
        html = ROOT_PAGE.read_text(encoding="utf-8")
        self.assertIsNone(
            _ROBOTS_NOINDEX_RE.search(html),
            "root index.html must not carry a noindex robots meta",
        )


if __name__ == "__main__":
    unittest.main()
