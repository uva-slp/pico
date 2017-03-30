from django.test import TestCase

from users.lib import storage

class GitRootTest(TestCase):

    # nathan
    def test_called_process_error(self):
        self.assertEqual(storage.git_root('INVALID_PATH', 'default'), 'default')

class DiskUsageTest(TestCase):

    # nathan
    def test_usage_root(self):
        usage = storage.usage_root()
        self.assertIsNotNone(usage)
        self.assertIsNotNone(usage.total)
        self.assertIsNotNone(usage.used)
        self.assertIsNotNone(usage.free)

    # nathan
    def test_du(self):
        usage_pico = storage.usage_pico()
        self.assertIsNotNone(usage_pico)
        self.assertIsInstance(usage_pico, int)

    # nathan
    def test_usage_db(self):
        usage_db = storage.usage_db()
        self.assertIsNotNone(usage_db)
        self.assertIsInstance(usage_db, int)
