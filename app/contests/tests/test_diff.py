from django.test import TestCase
from contests.lib.diff import HtmlFormatter
from contests.lib.html import Element

class HtmlElementTest(TestCase):

    # nathan
    def test_set_element_id(self):
        elem = Element('div').setElementId('id')
        self.assertEqual('id', elem.elid)

    # nathan
    def test_style_str(self):
        elem = Element('div').addStyle('height', '0').addStyle('width', '0')
        style_str = elem.styleStr()
        self.assertTrue('height:0' in style_str)
        self.assertTrue('width:0' in style_str)

class HtmlFormatterTest(TestCase):

    # nathan
    def test_prepare_add(self):
        html = str(HtmlFormatter().prepare(0, '\0+ \1'))
        self.assertTrue('diff-add' in html)
        self.assertTrue('diff-add-bg' in html)

    # nathan
    def test_prepare_del(self):
        html = str(HtmlFormatter().prepare(0, '\0- \1'))
        self.assertTrue('diff-del' in html)
        self.assertTrue('diff-del-bg' in html)

    # nathan
    def test_prepare_chg_from(self):
        html = str(HtmlFormatter(distinguish_changed=False).prepare(0, '\0^ \1'))
        self.assertTrue('diff-del' in html)
        self.assertTrue('diff-del-bg' in html)
        self.assertFalse('diff-chg' in html)
        self.assertFalse('diff-chg-bg' in html)

    # nathan
    def test_prepare_chg_to(self):
        html = str(HtmlFormatter(distinguish_changed=False).prepare(1, '\0^ \1'))
        self.assertTrue('diff-add' in html)
        self.assertTrue('diff-add-bg' in html)
        self.assertFalse('diff-chg' in html)
        self.assertFalse('diff-chg-bg' in html)

    # nathan
    def test_prepare_chg(self):
        html = str(HtmlFormatter(distinguish_changed=True).prepare(0, '\0^ \1'))
        self.assertTrue('diff-chg' in html)
        self.assertTrue('diff-chg-bg' in html)

    # nathan
    def test_prepare_whitespace(self):
        html = str(HtmlFormatter().prepare(0, '\0+ asdf   \1'))
        self.assertTrue('diff-whitespace' in html)
        self.assertFalse('diff-emptyline' in html)

    # nathan
    def test_prepare_emptyline(self):
        html = str(HtmlFormatter().prepare(0, '\0+ \1'))
        self.assertFalse('diff-whitespace' in html)
        self.assertTrue('diff-emptyline' in html)
