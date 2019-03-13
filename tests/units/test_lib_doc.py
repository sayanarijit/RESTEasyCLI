import os
import unittest
from docify import Document

from .common import workspace
from resteasycli.lib.doc import APIDocument
from resteasycli.exceptions import FileExtensionNotSupportedException


class GenerateTest(unittest.TestCase):

    def test_create(self):
        doc = APIDocument(workspace)
        self.assertIsInstance(doc.doc, Document)

    def test_dump(self):
        doc = APIDocument(workspace)

        self.assertRaises(
            FileExtensionNotSupportedException,
            lambda: doc.dump('generated_docs'),
        )

        self.assertRaises(
            FileExtensionNotSupportedException,
            lambda: doc.dump('generated_docs.abcd'),
        )

        if os.path.exists('generated_docs.md'):
            os.remove('generated_docs.md')
        doc.dump('generated_docs.md')
        self.assertTrue(os.path.exists('generated_docs.md'))


if __name__ == '__main__':
    unittest.main()
