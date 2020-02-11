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
from .RDFStatInterface import RDFStatInterface
import lodstats.util.rdf_namespaces
import RDF

class UsedClasses(RDFStatInterface):
    """
        Used Classes Criterion
        Output format: {'classname': usage count}
    """

    def __init__(self, results):
        super(UsedClasses, self).__init__(results)
        self.usage_count = self.results['usage_count'] = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and statement.object.is_resource():
            self.usage_count[o] = self.usage_count.get(o, 0) + 1
    
    def voidify(self, void_model, dataset):
        namespaces = lodstats.util.rdf_namespaces.RDFNamespaces()
        datatype_uri = namespaces.get_rdf_namespace("xsd").int.uri

        for class_uri_k, class_uri_v in self.usage_count.items():
                class_partitions_node = RDF.Node()

                statement_class_uri = RDF.Statement(class_partitions_node, namespaces.get_rdf_namespace("void")['class'],
                                        RDF.Node(uri_string=class_uri_k))
                statement_class_triples_value = RDF.Statement(class_partitions_node, namespaces.get_rdf_namespace("void").entities,
                                        RDF.Node(literal=str(class_uri_v), datatype=datatype_uri))
                statement = RDF.Statement(dataset, namespaces.get_rdf_namespace("void").classPartition, class_partitions_node)
                void_model.append(statement)
                void_model.append(statement_class_uri)
                void_model.append(statement_class_triples_value)

    def postproc(self):
        self.count = self.results['count'] = len(self.usage_count)

    def sparql(sparql, endpoint):
        pass
