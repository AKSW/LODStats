import lodstats.util.rdffile
import lodstats.config
import logging

logger = logging.getLogger("lodstats")

class RdfParser(object):
    def __init__(self, uri_list, callback_function=None, stats=None, rdf_format=None):
        self.rdf_format=rdf_format
        self.callback_function = callback_function
        self.uri_list = uri_list
        self.stats = stats
        self.stream = None
        self.stats_results = None # shared object between several rdf_file
        self.init_stats(stats)
        self.rdf_file_list = self.process_uri_list()

    def init_stats(self, stats):
        if stats is None:
            self.stats_results = lodstats.stats.init_stats()
        else:
            self.stats_results = lodstats.stats.init_stats(stats)

    def get_rdf_file_list(self):
        return self.rdf_file_list

    def get_no_of_statements(self):
        result = 0
        for rdf_file in self.get_rdf_file_list():
            result += rdf_file.get_no_of_statements()
        return result

    def get_no_of_triples(self):
        return self.get_no_of_statements()

    def get_no_of_warnings(self):
        no_of_warnings = 0
        for rdf_file in self.get_rdf_file_list():
            no_of_warnings += rdf_file.warnings
        return no_of_warnings

    def get_stats_results(self):
        return self.stats_results

    def process_uri_list(self):
        rdf_files = []
        for uri in self.uri_list:
            logger.debug("Processing rdf file: %s" % uri)
            rdf_file = lodstats.util.rdffile.RdfFile(uri,
                                                     stats=self.stats,
                                                     callback_function=self.callback_function,
                                                     rdf_format=self.rdf_format)
            rdf_files.append(rdf_file)
        lodstats.stats.postproc()
        return rdf_files


if __name__ == "__main__":
    rdfparser = RdfParser([lodstats.config.rdf_test_file_uri])
    print rdfparser.get_stats_results()
    pass
