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
from RDFStatInterface import RDFStatInterface
import RDF
from lodstats.util.namespace import ns_xs, ns_void
import distincthelper as dh

class Classes(RDFStatInterface):
    """count class usage"""
    def __init__(self, results):
        super(Classes, self).__init__(results)
        self.histogram = self.results['histogram'] = {}
        self.subject_distinct = self.results['distinct'] = {} # FIXME: namen aendern, ist spo-distinct, nicht nur subj
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # mimic make-void, count every class usage
        count_it = False
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and statement.object.is_resource():
            self.histogram[o] = self.histogram.get(o, 0) + 1
            count_it = True
        # distinct per subject
        spo = s+p+o
        if count_it and not dh.query_distinct_spo(spo, 1):
            dh.set_distinct_spo(spo, 1)
            self.subject_distinct[o] = self.subject_distinct.get(o, 0) + 1
    
    def voidify(self, void_model, dataset):
        # no of classes
        result_node = RDF.Node(literal=str(len(self.histogram)), datatype=ns_xs.integer.uri)
        void_model.append(RDF.Statement(dataset, ns_void.classes, result_node))
        # class partition
        for class_uri,result in self.subject_distinct.iteritems():
            clid = RDF.Node()
            void_model.append(RDF.Statement(dataset, ns_void.classPartition, clid))
            void_model.append(RDF.Statement(clid, ns_void['class'], RDF.Uri(class_uri)))
            result_node = RDF.Node(literal=str(result), datatype=ns_xs.integer.uri)
            void_model.append(RDF.Statement(clid, ns_void.entities, result_node))
    
    def sparql(sparql, endpoint):
        pass

class ClassesDefined(RDFStatInterface):
    """count usage of classes defined"""
    def __init__(self, results):
        super(ClassesDefined, self).__init__(results)
        self.histogram = self.results['histogram'] = {}
        self.subject_distinct = self.results['distinct'] = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # count all class definitions
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2000/01/rdf-schema#Class':
            self.histogram[s] = 0
        # count usage of defined classes
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and self.histogram.has_key(o):
            self.histogram[o] += 1
        # distinct per subject
        spo = s+p+o
        if self.histogram.has_key(o) and not dh.query_distinct_spo(spo, 2):
            dh.set_distinct_spo(spo, 2)
            self.subject_distinct[o] = self.subject_distinct.get(o, 0) + 1
    
    def sparql(self, endpoint):
        pass
    
    def voidify(self, void_model, dataset):
        pass

