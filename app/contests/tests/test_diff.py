from django.test import TestCase
from contests.lib.html import Element

class ElementTest(TestCase):

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
