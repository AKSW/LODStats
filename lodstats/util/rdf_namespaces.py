import RDF
import logging

logger = logging.getLogger("lodstats")

class RDFNamespaces(object):
    namespaces = {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "void": "http://rdfs.org/ns/void#",
            "void_ext": "http://stats.lod2.eu/rdf/void-ext/",
            "qb": "http://purl.org/linked-data/cube#",
            "dcterms": "http://purl.org/dc/terms/",
            "ls_void": "http://stats.lod2.eu/rdf/void/",
            "ls_qb": "http://stats.lod2.eu/rdf/qb/",
            "ls_cr": "http://stats.lod2.eu/rdf/qb/criteria/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "stats": "http://example.org/XStats#",
            "foaf": "http://xmlns.com/foaf/0.1/",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
            }

    def __init__(self):
        pass

    def get_rdf_namespace(self, namespace):
        if(namespace in self.namespaces):
            return RDF.NS(self.namespaces[namespace])
        else:
            logger.error("Namespace %s is not defined"%namespace)
            return None

    def get_namespace(self, namespace):
        if(namespace in self.namespaces):
            return self.namespaces[namespace]
        else:
            logger.error("Namespace %s is not defined"%namespace)
            return None
