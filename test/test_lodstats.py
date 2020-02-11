import unittest

from requests.exceptions import HTTPError

import lodstats
from lodstats import RDFStats

from requests import HTTPError

from . import helpers

http_base = helpers.webserver(helpers.resources_path)
testfile_path = helpers.resources_path

class LodstatsTest(unittest.TestCase):

    def setUp(self):
        lodstats.stats.stats_to_do = []
        lodstats.stats.results = {}

    def test_remote_bz2(self):
        uri = http_base + 'heb.rdf.bz2'
        rdfstats = RDFStats(uri)
        #rdfstats.set_callback_function_download(test_callback_download)
        #rdfstats.set_callback_function_extraction(test_callback_extraction)
        rdfstats.start_statistics()
        assert(len(rdfstats.get_stats_results()) > 5)

    def test_local_rdf(self):
        uri = 'file://' + testfile_path + 'heb-original.rdf'
        rdfstats = RDFStats(uri)
        rdfstats.start_statistics()
        assert(len(rdfstats.voidify("turtle")) > 5)

    def test_remote_tar(self):
        uri = http_base + 'heb.nt.tgz'
        rdfstats = RDFStats(uri)
        rdfstats.start_statistics()
        assert(len(rdfstats.get_stats_results()) > 5)

    def test_404_remote_tar_gz(self):
        import tarfile
        uri = http_base + 'DOESNOTEXIST.nt.tgz'
        with self.assertRaises(HTTPError):
            rdfstats = RDFStats(uri)
            rdfstats.start_statistics()

    def test_remote_not_usual_extension(self):
        uri = http_base + "heb.nt.tgz?accessType=DOWNLOAD"
        rdfstats = RDFStats(uri, format="nt")
        rdfstats.start_statistics()
        assert(len(rdfstats.voidify("turtle")) > 5)

# FIXME add test for sitemaps
