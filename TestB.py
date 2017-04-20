import unittest


class TestB(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)
    def test_something1(self):
        self.assertEqual(True, True)


    @staticmethod
    def suite():
        """TestSuite for this class"""
        suite = unittest.TestLoader().loadTestsFromTestCase(TestB)
        unittest.TextTestRunner(verbosity=2).run(suite)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestB)
    unittest.TextTestRunner(verbosity=2).run(suite)
