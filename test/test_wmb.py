import utils
import os
import unittest

TOPDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)
utils.set_search_paths(TOPDIR)


import whatsmyblob


class TestWhatsMyBlob(unittest.TestCase):

    def test_data_group(self):
        # This is a working test
        a_value = 2
        c_value = 2
        self.assertEqual(
            a_value,
            c_value
        )

    @unittest.expectedFailure
    def test_fit_data_setter(self):
        # This is a failing test
        self.assertEqual(
            False,
            True
        )

