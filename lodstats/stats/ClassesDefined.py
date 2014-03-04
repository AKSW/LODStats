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

class ClassesDefined(RDFStatInterface):
    """
        Used Classes Criterion
        Output format: {'classname': usage count}
    """

    def __init__(self, results):
        super(ClassesDefined, self).__init__(results)
        self.usage_count = self.results['usage_count'] = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # "classes defined" criterion filter
        if (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2000/01/rdf-schema#Class') or\
           (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2002/07/owl#Class'):
            self.usage_count[s] = 0
        # count usage of defined classes
        # if class is used as object
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and self.usage_count.has_key(o):
            self.usage_count[o] += 1
    
    def voidify(self, void_model, dataset):
        namespaces = lodstats.util.rdf_namespaces.RDFNamespaces()
        datatype_uri = namespaces.get_rdf_namespace("xsd").integer.uri
        number_of_distinct_classes = str(self.results['count'])
        number_of_distinct_classes_node = RDF.Node(literal=number_of_distinct_classes, 
                                          datatype=datatype_uri)
        void_model.append(RDF.Statement(dataset,
                                        namespaces.get_rdf_namespace("void").classes,
                                        number_of_distinct_classes_node))

    def postproc(self):
        self.count = self.results['count'] = len(self.usage_count)

    def sparql(self, endpoint):
        from SPARQLWrapper import JSON
        endpoint.setQuery("SELECT distinct ?i ?c { ?i a ?c }")
        endpoint.setReturnFormat(JSON)
        results = endpoint.query().convert()
        if not isinstance(results, dict):
            raise Exception, "unknown response content type"
        for row in results['results']['bindings']:
            c = row['c']['value']
            if (c == 'http://www.w3.org/2000/01/rdf-schema#Class' or c == 'http://www.w3.org/2002/07/owl#Class') :
                i = row['i']['value']
                if not self.usage_count.has_key(i) :
                    self.usage_count[i] = 0
        for row in results['results']['bindings']:
            c = row['c']['value']
            if self.usage_count.has_key(c) :
                self.usage_count[c] += 1

