"""
Copyright 2013 AKSW research group -- http://aksw.org/

This file is part of LODStats.

LODStats is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LODStats is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LODStats.  If not, see <http://www.gnu.org/licenses/>.
"""
"""Parse RDF and do some stats"""
import datetime
import lodstats.stats
import lodstats.util.archiveextractor
import lodstats.util.rdfparser
import lodstats.util.remotefile
import lodstats.util.sitemap
import lodstats.util.makevoid
import lodstats.util.interfaces

import lodstats.config

import logging
logger = logging.getLogger("lodstats")

class RDFStats(lodstats.util.interfaces.UriParserInterface):

    """Get some interesting numbers from RDFish resources"""
    def __init__(self, rdfurl, do_custom_stats=True,
            stats=None, new_stats=None, format=None):

        #from the LODStats_WWW DB or command line script
        self.rdf_format = format

        self.rdf_parser = None

        #run start_statistics to gather stats
        self.uri = self.fix_uri(rdfurl)

        #stats to be calculated (list)
        self.stats = stats

        #use set_callback_function_* to set custom callback
        self.set_callback_function_download(None)
        self.set_callback_function_extraction(None)
        self.set_callback_function_statistics(None)

        # TODO: no_of_statements -> triples_number
        self.no_of_statements = 0

        #for backward compatibility
        self.last_modified = None

        # this is a hook for parsing vocabulary
        # new_stats = [ParsedVocabulary, options.rdf_model]
        if new_stats:
            lodstats.stats.stats_to_do.append(new_stats[0](self.stats_results, new_stats[1]))

    def start_statistics(self):
        logger.debug("Downloading remote file ...")
        remote_file = lodstats.util.remotefile.RemoteFile(self.uri, callback_function=self.callback_function_download)
        downloaded_file_uri = remote_file.get_downloaded_file_uri()

        #logger.debug("Parsing sitemap ...")
        #sitemap = lodstats.util.sitemap.SiteMap(uri)

        logger.debug("Extracting the file from archive: %s" % downloaded_file_uri)
        archive_extractor = lodstats.util.archiveextractor.ArchiveExtractor(downloaded_file_uri,
                                                                            callback_function=self.callback_function_extraction,
                                                                            remote_file=remote_file)
        extracted_file_uri_list = archive_extractor.get_extracted_file_uri_list()

        logger.debug("Parsing RDF files ...")
        self.rdfparser = lodstats.util.rdfparser.RdfParser(extracted_file_uri_list,
                                                           stats=self.stats,
                                                           callback_function=self.callback_function_statistics,
                                                           rdf_format=self.rdf_format)

    def get_stats_results(self):
        return self.rdfparser.get_stats_results()

    def get_no_of_triples(self):
        return self.rdfparser.get_no_of_triples()

    def get_no_of_warnings(self):
        return self.rdfparser.get_no_of_warnings()

    def get_last_warning(self):
        return self.rdfparser.get_last_warning()

    def enable_debug(self):
        lodstats.config.enable_debug()

    def disable_debug(self):
        lodstats.config.disable_debug()

    def set_callback_function_download(self, callback_function):
        if(callback_function is None):
            self.callback_function_download = lodstats.config.callback_function_download
        else:
            self.callback_function_download = callback_function

    def disable_callback_function_download(self):
        self.callback_function_download = None

    def set_callback_function_extraction(self, callback_function):
        if(callback_function is None):
            self.callback_function_extraction = lodstats.config.callback_function_archive_extraction
        else:
            self.callback_function_extraction = callback_function

    def disable_callback_function_extraction(self):
        self.callback_function_extraction = None

    def set_callback_function_statistics(self, callback_function):
        if(callback_function is None):
            self.callback_function_statistics = lodstats.config.callback_function_statistics
        else:
            self.callback_function_statistics = callback_function

    def disable_callback_function_statistics(self):
        self.callback_function_statistics = None

    def sitemap(self, sitemapurl, callback_parse=None, callback_stats=None):
        """process datadumps from a sitemap.xml as per http://XXX"""
        logger.debug("processing sitemap %s" % sitemapurl)
        datadumps = lodstats.util.format.parse_sitemap(sitemapurl)

        if callback_parse is None:
            callback_parse = self.callback_parse
        if callback_stats is None:
            callback_stats = self.callback_stats

        for datadump in datadumps:
            self.next_file(datadump)
            self.parse(callback_parse)
            self.do_stats(callback_stats)
    # accessors for statistics here

    def no_of_namespaces(self):
        """docstring for noofnamespaces"""
        if self.format != 'sparql':
            return len(self.parser.namespaces_seen())

    def measure_execution_time_start(self):
        self.start_time = datetime.datetime.now()

    def measure_execution_time_stop(self):
        self.end_time = datetime.datetime.now()

    def voidify(self, serialize_as = "ntriples"):
        makevoid = lodstats.util.makevoid.MakeVoid(self, serialize_as=serialize_as)
        return makevoid.voidify()


if __name__ == "__main__":
    def test_callback_extraction(object):
        print "%s bytes" % object.bytes_extracted

    def test_callback_download(object):
        print "%s bytes" % object.bytes_downloaded

    #logger.debug("Test case 1: remote file, bzip2 archive")
    #logger.debug("=======================================")
    #uri = "https://dl.dropboxusercontent.com/u/4882345/lodstats-test/heb.rdf.bz2"
    #rdfstats = RDFStats(uri)
    #rdfstats.set_callback_function_download(test_callback_download)
    #rdfstats.set_callback_function_extraction(test_callback_extraction)
    #rdfstats.start_statistics()
    #print rdfstats.get_stats_results()
    #print "\n\n\n"
    #lodstats.stats.stats_to_do = []


    logger.debug("Test case 2: local file")
    logger.debug("======================================")
    uri = lodstats.config.rdf_test_file_uri
    rdfstats = RDFStats(uri)
    rdfstats.set_callback_function_download(test_callback_download)
    rdfstats.set_callback_function_extraction(test_callback_extraction)
    rdfstats.start_statistics()
    print rdfstats.voidify("turtle")
    #print rdfstats.get_stats_results()
    print "\n\n\n"
    lodstats.stats.stats_to_do = []

    #logger.debug("Test case 3: remote file, tar archive")
    #logger.debug("======================================")
    #uri = "https://dl.dropboxusercontent.com/u/4882345/lodstats-test/heb.nt.tgz"
    #rdfstats = RDFStats(uri)
    #rdfstats.set_callback_function_download(test_callback_download)
    #rdfstats.set_callback_function_extraction(test_callback_extraction)
    #rdfstats.start_statistics()
    ##print rdfstats.get_stats_results()
    #print "\n\n\n"
    #lodstats.stats.stats_to_do = []

    #Test case 4:
    #sitemap
