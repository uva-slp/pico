from django.test import TestCase

class ValidOrganizationNameTest(TestCase):
    #form should prevent invalid characters from being entered and that len() > 0
    def invalid_org_name(self):
        o1 = Organization(name='')
        o2 = Organization(name='123org...()')
        o1.save()
        o2.save()
        self.assertFalse(len(o1.name) > 0)
        self.assertFalse(all(c.isalnum() for c in o2.name))