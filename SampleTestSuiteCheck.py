import unittest


from test_client.TestA import TestA
from test_client.TestB import TestB


class SampleTestSuite(unittest.TestCase):

    if __name__ == '__main__':
        loader = unittest.TestLoader()
        module1 = TestA.suite()
        module2 = TestB.suite()
        # module2 = ChatTest_TicketQuerying.suite()
        # module3 = ChatTest_MultilingualHindi.suite()
        suite = unittest.TestSuite([module1, module2])
        unittest.TextTestRunner(verbosity=2).run(suite)
