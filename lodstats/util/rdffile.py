import lodstats.config
import lodstats.stats
import RDF
import warnings
import logging

logger = logging.getLogger("lodstats")

from lodstats.util.interfaces import CallbackInterface
from lodstats.util.interfaces import UriParserInterface

class RdfFile(CallbackInterface, UriParserInterface):
    def __init__(self, uri, callback_function=None, stats=None, rdf_format=None):
        super(RdfFile, self).__init__()
        self.no_of_statements = 0
        self.warnings = 0
        self.last_warning = None
        self.processing_start_time = None
        self.processing_end_time = None
        self.rdf_format = rdf_format

        self.stats_results = []
        self.set_uri(uri)
        if(self.rdf_format is None):
            self.rdf_format = self.identify_rdf_format(self.uri) # UriParserInterface
        logger.debug("Rdf format identified: %s" % self.rdf_format)
        self.rdf_parser = self.identify_rdf_parser()
        self.rdf_stream = self.rdf_parser.parse_as_stream(self.uri)
        self.do_stats(callback_function)

    def get_no_of_statements(self):
        return self.no_of_statements

    def get_no_of_triples(self):
        return self.get_no_of_statements()

    def get_rdf_format(self):
        return self.rdf_format

    def get_rdf_parser(self):
        return self.rdf_parser

    def get_rdf_stream(self):
        return self.rdf_stream

    def set_uri(self, uri):
        self.uri = uri

    def set_rdf_format(self, rdf_format):
        self.rdf_format = rdf_format

    def identify_rdf_parser(self):
        format = self.rdf_format
        if format == 'ttl':
            parser = RDF.TurtleParser()
        elif format == 'nt' or format == 'n3': # FIXME: this probably won't do for n3
            parser = RDF.NTriplesParser()
        elif format == 'nq':
            parser = RDF.Parser(name='nquads')
        elif format == 'rdf':
            parser = RDF.Parser(name="rdfxml")
        elif format == 'sparql':
            return None
        elif format == 'sitemap':
            return None
        else:
            raise NameError("unsupported format")
        return parser

    def warn_handler(self, message, category, filename, lineno, file=None, line=None):
        self.warnings += 1
        self.last_warning = message

    def collect_stats_file(self, callback_function=None):
        with warnings.catch_warnings():
            warnings.showwarning = self.warn_handler
            for statement in self.rdf_stream:
                # count statements
                self.no_of_statements += 1

                # do custom counting
                self.do_custom_stats(statement)

                # optional callback (eg for status stuff) every 5000 triples
                if callback_function != None and self.no_of_statements % 5000 == 0:
                    callback_function(self)

        if callback_function is not None:
            callback_function(self)

    def do_custom_stats(self, statement):
        """call custom stats"""
        # make various things available to the custom code, triple is already there
        s_blank = statement.subject.is_blank()
        if s_blank:
            s = str(statement.subject)
        else:
            s = str(statement.subject.uri)
        p = str(statement.predicate.uri)
        o_l = statement.object.is_literal()
        o_blank = statement.object.is_blank()
        if o_l or o_blank:
            o = str(statement.object)
        else:
            o = str(statement.object.uri)

        lodstats.stats.run_stats(s, p, o, s_blank, o_l, o_blank, statement)

    def do_stats(self, callback_function = None):
        """do the real work"""
        logger.debug("do_stats()")
        self.callback_stats = callback_function

        if self.rdf_format == 'sitemap':
            self.sitemap(self.url)
            return
        elif self.rdf_format == 'sparql':
            self.collect_stats_sparql()
        else:
            self.collect_stats_file(callback_function)

        if self.no_of_statements == 0:
            raise Exception, "zero triples"

    def collect_stats_sparql(self):
        """do stats via SPARQL"""
        logger.debug("do_sparql_stats()")
        from SPARQLWrapper import SPARQLWrapper, JSON
        sparql = SPARQLWrapper(self.url)
        sparql.setQuery("SELECT (count(*) AS ?triples) WHERE { ?s ?p ?o }")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if not isinstance(results, dict):
            raise Exception, "unknown response content type"
        self.no_of_statements = int(results['results']['bindings'][0]['triples']['value'])

        lodstats.stats.run_stats_sparql(self.url)

