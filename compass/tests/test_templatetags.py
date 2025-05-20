# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import re
from django.test import TestCase
from compass.templatetags.vite import vite_styles, vite_scripts


class ViteTestClass(TestCase):
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_vite_styles(self):
        entries = ("compass_vue/main.js",)
        link = vite_styles(*entries)
        pattern = re.compile(r'<link\s+[^>]*href="[^"]*main-[^"]*"[^>]*>')
        self.assertTrue(pattern.search(link))

    def test_vite_scripts(self):
        entries = ("compass_vue/main.js",)
        script = vite_scripts(*entries)
        pattern = re.compile(
            r'<script\s+[^>]*src="[^"]*main-[^"]*"[^>]*></script>'
        )
        self.assertTrue(pattern.search(script))
