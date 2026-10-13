"""Falsifiers for the cors-test sitemap-artifact fix (fu010).

The live defect (2026-10-13): sitemap.xml declares /cors-test/ and
cors-test/index.html carries no robots meta — a development diagnostic
page is indexable and sitemap-declared on a live host.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class SitemapHygieneTests(unittest.TestCase):
    def test_sitemap_excludes_cors_test(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertNotIn("cors-test", sitemap)

    def test_sitemap_still_lists_root(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        self.assertIn("<loc>https://search-archive.isaackoi.com/</loc>", sitemap)

    def test_cors_test_carries_noindex(self):
        page = (ROOT / "cors-test" / "index.html").read_text(encoding="utf-8")
        self.assertRegex(
            page,
            r'<meta\s+name="robots"\s+content="[^"]*noindex',
        )

    def test_root_stays_indexable(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertNotRegex(page, r'<meta\s+name="robots"\s+content="[^"]*noindex')


if __name__ == "__main__":
    unittest.main()
