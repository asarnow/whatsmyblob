import utils
import os
import unittest
import tempfile

TOPDIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')
)
utils.set_search_paths(TOPDIR)

import whatsmyblob
import whatsmyblob.result_table


class TestWhatsMyBlob(unittest.TestCase):

    def test_generate_result_table(self):
        html_str = whatsmyblob.result_table.generate_html(
            jobid=1,
            folder='./data/results/',
            title='Test title 1'
        )
        # write to file
        filename_html = 'test.html'
        with open(file=filename_html, mode='w') as fp:
            fp.write(html_str)

    def test_data_group(self):
        # This is an example for a working test
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

