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
from .RDFStatInterface import RDFStatInterface
import RDF

class DistinctObjects(RDFStatInterface):
    """
        Distinct number of entities
        Entity - triple, where ?s is iri (not blank)
    """
    def __init__(self, results):
        super(DistinctObjects, self).__init__(results)
        self.objects = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        self.objects[o] = self.objects.get(o, 1) + 1
    
    def postproc(self):
        self.results['count'] = len(self.objects)

    def voidify(self, void_model, dataset):
        namespaces = lodstats.util.rdf_namespaces.RDFNamespaces()
        datatype_uri = namespaces.get_rdf_namespace("xsd").integer.uri
        number_of_distinct_objects = str(self.results['count'])
        number_of_distinct_objects_node = RDF.Node(literal=number_of_distinct_objects, 
                                          datatype=datatype_uri)
        void_model.append(RDF.Statement(dataset,
                                        namespaces.get_rdf_namespace("void").distinctObjects,
                                        number_of_distinct_objects_node))
    
    def sparql(self, endpoint):
        pass
