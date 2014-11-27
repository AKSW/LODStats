"""
Copyright 2013 AKSW Research Group http://aksw.org

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
import lodstats.util.rdf_namespaces
from RDFStatInterface import RDFStatInterface
import RDF

class Entities(RDFStatInterface):
    """
        Distinct number of entities
        Entity - triple, where ?s is iri (not blank)
    """
    def __init__(self, results):
        super(Entities, self).__init__(results)
        #self.entities = []
        self.c = 0
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if statement.object.is_resource() and\
           statement.subject.is_resource() and\
           statement.predicate.is_resource():
               #self.entities.append( (s,p,o) )
               self.c += 1
    
    def postproc(self):
        #Entities mentioned
        self.results['count'] = self.c
        #Distinct entities
        #self.results['triples'] = self.triples

    def voidify(self, void_model, dataset):
        namespaces = lodstats.util.rdf_namespaces.RDFNamespaces()
        datatype_uri = namespaces.get_rdf_namespace("xsd").integer.uri
        number_of_distinct_entities = str(self.results['count'])
        number_of_entities_node = RDF.Node(literal=number_of_distinct_entities, 
                                          datatype=datatype_uri)
        void_model.append(RDF.Statement(dataset,
                                        namespaces.get_rdf_namespace("void").entities,
                                        number_of_entities_node))
    
    def sparql(self, endpoint):
        pass
