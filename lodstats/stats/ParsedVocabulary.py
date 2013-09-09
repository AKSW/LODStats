"""
Copyright 2012 Jan Demter <jan@demter.de>

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
import RDF
from os.path import realpath, dirname
from RDFStatInterface import RDFStatInterface
from lodstats.util.rdffile import RdfFile
from lodstats.util.namespace import ns_xs, ns_void, ns_rdf, ns_stats, ns_qb

class ParsedVocabulary(RDFStatInterface, RdfFile):
    """count usage of everything that #isDefinedBy some vocabulary"""
    
    def __init__(self, results, model_path):
        super(ParsedVocabulary, self).__init__(results)
        
        if model_path is not None:
            model = realpath(model_path)
        else:
            model = realpath(dirname(__file__) + "/../rdf/rdf-schema.rdf")
        self.set_uri(model)
        self.set_rdf_format(self.identify_rdf_format(self.uri))
        parser_model = self.identify_rdf_parser()

        model_stream = parser_model.parse_as_stream("file://%s" % model)
        
        self.results['s'] = {}
        self.results['p'] = {}
        self.results['o'] = {}
        self.results['sum'] = {}
        self.schema = None
        for statement in model_stream:
            if str(statement.predicate) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"\
                    and str(statement.object) == "http://www.w3.org/2002/07/owl#Ontology":
                self.schema = statement.subject
            #FIXME isDefinedBy nur aufnehmen, wenn es aus selbem namespace wie resource kommt
            if str(statement.predicate) == "http://www.w3.org/2000/01/rdf-schema#isDefinedBy":
                self.results['s'][str(statement.subject)] = 0
                self.results['p'][str(statement.subject)] = 0
                self.results['o'][str(statement.subject)] = 0
                self.results['sum'][str(statement.subject)] = 0
        if self.schema is None:
            self.schema = RDF.Uri("file://%s" % model)
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if self.results['s'].has_key(s):
            self.results['s'][s] += 1
            self.results['sum'][s] += 1
        if self.results['p'].has_key(p):
            self.results['p'][p] += 1
            self.results['sum'][p] += 1
        if self.results['o'].has_key(o):
            self.results['o'][o] += 1
            self.results['sum'][o] += 1
    
    def voidify(self, void_model, dataset):
        # usage as property
        for property_uri,result in self.results['sum'].iteritems():
            if result == 0:
                continue
            observation = RDF.Node()
            void_model.append(RDF.Statement(dataset, ns_void.observation, observation))
            void_model.append(RDF.Statement(observation, ns_rdf.type, ns_qb.Observation))
            void_model.append(RDF.Statement(observation, ns_stats.schema, self.schema))
            o_type = RDF.Uri(property_uri)
            void_model.append(RDF.Statement(observation, ns_stats.subjectsOfType, o_type))
            result_node = RDF.Node(literal=str(result), datatype=ns_xs.integer.uri)
            void_model.append(RDF.Statement(observation, ns_stats.value, result_node))
    
    def sparql(self, endpoint):
        pass
