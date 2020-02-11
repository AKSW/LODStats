import unittest
from os.path import exists
import filecmp
from requests.exceptions import HTTPError

from requests.exceptions import HTTPError

import lodstats
from lodstats.util.remotefile import RemoteFile

from . import helpers

http_base = helpers.webserver(helpers.resources_path)

class RemoteFileTest(unittest.TestCase):

    def setUp(self):
        lodstats.stats.stats_to_do = []
        lodstats.stats.results = {}


    def test_remotefile(self):
        remote_file = RemoteFile(http_base + 'heb.rdf')
        file_uri = remote_file.get_downloaded_file_uri()
        self.assertTrue(exists(file_uri[7:]))
        self.assertTrue(filecmp.cmp(file_uri[7:],
                        helpers.resources_path + 'heb.rdf'))

    def test_remotefile_404(self):
        remote_file = RemoteFile(http_base + 'DOESNOTEXIST.rdf')
        with self.assertRaises(HTTPError):
            file_uri = remote_file.get_downloaded_file_uri()

