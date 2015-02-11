import unittest
from os import path
import filecmp

from lodstats.util.archiveextractor import ArchiveExtractor

from helpers import resources_path

original = resources_path+'heb-original.rdf'
original_head = resources_path+'heb-head-original.nt'
original_tail = resources_path+'heb-tail-original.nt'

class ArchiveTests(unittest.TestCase):

    def test_uncompressed(self):
        gz_file_uri = 'file://'+resources_path+'heb.rdf'
        ae = ArchiveExtractor(gz_file_uri)
        self.assertTrue(filecmp.cmp(ae.get_extracted_file_path_list()[0],
                original), 'file differs')

    def test_gzip(self):
        gz_file_uri = 'file://'+resources_path+'heb.rdf.gz'
        ae = ArchiveExtractor(gz_file_uri)
        self.assertTrue(filecmp.cmp(ae.get_extracted_file_path_list()[0],
                original), 'file differs')

    def test_bz2(self):
        file_uri = 'file://'+resources_path+'heb.rdf.bz2'
        ae = ArchiveExtractor(file_uri)
        self.assertTrue(filecmp.cmp(ae.get_extracted_file_path_list()[0],
                original), 'file differs')

    def test_tar_gz(self):
        file_uri = 'file://'+resources_path+'heb.nt.tgz'
        ae = ArchiveExtractor(file_uri)
        self.assertTrue(filecmp.cmp(ae.get_extracted_file_path_list()[0],
                original_head), 'file 1 differs')
        self.assertTrue(filecmp.cmp(ae.get_extracted_file_path_list()[1],
                original_tail), 'file 2 differs')

    def test_zip(self):
        file_uri = 'file://'+resources_path+'heb.nt.zip'
        ae = ArchiveExtractor(file_uri)
        self.assertTrue(filecmp.cmp(ae.get_extracted_file_path_list()[0],
                original_head), "file 1 differs")
        self.assertTrue(filecmp.cmp(ae.get_extracted_file_path_list()[1],
                original_tail), "file 2 differs")

# FIXME test callback
