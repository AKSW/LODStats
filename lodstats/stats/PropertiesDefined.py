"""
Copyright 2013 AKSW Research group http://aksw.org/

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
from RDFStatInterface import RDFStatInterface
import lodstats.util.rdf_namespaces
import RDF

class PropertiesDefined(RDFStatInterface):
    """
        Properties Defined Criterion
        Output format: {'propertyname': usage count}
    """

    def __init__(self, results):
        super(PropertiesDefined, self).__init__(results)
        self.usage_count = self.results['usage_count'] = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # "classes defined" criterion filter
        if (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2002/07/owl#ObjectProperty') or\
           (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'):
            if(s.startswith("http")):
                self.usage_count[s] = 0
        # count usage of defined classes
        # if class is used as object
        # if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and self.usage_count.has_key(o):
        #    self.usage_count[o] += 1
    
    def voidify(self, void_model, dataset):
        namespaces = lodstats.util.rdf_namespaces.RDFNamespaces()
        datatype_uri = namespaces.get_rdf_namespace("xsd").integer.uri
	for property_uri_k, property_uri_v in self.usage_count.iteritems():
		property_partitions_node = RDF.Node()
		
		statement_property_uri = RDF.Statement(property_partitions_node, namespaces.get_rdf_namespace("void").property,
					RDF.Node(uri_string=property_uri_k))
		statement_property_triples_value = RDF.Statement(property_partitions_node, namespaces.get_rdf_namespace("void").triples,
					RDF.Node(literal=str(property_uri_v), datatype=datatype_uri))
		statement = RDF.Statement(dataset, namespaces.get_rdf_namespace("void").propertyPartition, property_partitions_node)
		void_model.append(statement)
		void_model.append(statement_property_uri)
		void_model.append(statement_property_triples_value)

    def postproc(self):
        self.count = self.results['count'] = len(self.usage_count)

    def sparql(sparql, endpoint):
        pass
