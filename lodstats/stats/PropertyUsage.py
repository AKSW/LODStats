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
from RDFStatInterface import RDFStatInterface
import lodstats.util.rdf_namespaces
import RDF

class PropertyUsage(RDFStatInterface):
    def __init__(self, results):
        super(PropertyUsage, self).__init__(results)
        self.usage_count = self.results['usage_count'] = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        self.usage_count[p] = self.usage_count.get(p, 0) + 1
    
    def voidify(self, void_model, dataset):
        namespaces = lodstats.util.rdf_namespaces.RDFNamespaces()
        datatype_uri = namespaces.get_rdf_namespace("xsd").integer.uri
        number_of_distinct_properties = str(len(self.usage_count))
        number_of_distinct_properties_node = RDF.Node(literal=number_of_distinct_properties, 
                                          datatype=datatype_uri)
        void_model.append(RDF.Statement(dataset,
                                        namespaces.get_rdf_namespace("void").properties,
                                        number_of_distinct_properties_node))
    
    def sparql(self, endpoint):
        pass
