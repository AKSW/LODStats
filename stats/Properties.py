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
import hashlib
import RDF
from LimitedSizeDict import LimitedSizeDict
from RDFStatInterface import RDFStatInterface
from ..util.namespace import ns_xs, ns_void
import distincthelper as dh

class PropertiesDefined(RDFStatInterface):
    """count properties that show up as predicate, works in combination with properties_histogram
       FIXME: sind properties immer "zuerst" definiert? wahrscheinlich nicht, dann klappt es leider so nicht richtig"""
    def __init__(self, results):
        super(PropertiesDefined, self).__init__(results)
        self.histogram = self.results['properties_histogram'] = {}
        self.distinct = self.results['properties_distinct'] = {}
        self.distinct_subject = self.results['properties_distinct_subject'] = {}
        self.distinct_object = self.results['properties_distinct_object'] = {}
        self.distinct_seen = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # count all property definitions
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and ( o == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property' or o == 'http://www.w3.org/2002/07/owl#ObjectProperty' ):
            self.histogram[s] = 0
        # count usage of defined properties
        if self.histogram.has_key(p):
            self.histogram[p] += 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

class PropertiesAll(RDFStatInterface):
    """count all properties"""
    def __init__(self, results):
        super(PropertiesAll, self).__init__(results)
        self.histogram = self.results['histogram'] = {}
        self.distinct = self.results['distinct'] = {}
        self.distinct_subject = self.results['distinct_subject'] = {}
        self.distinct_object = self.results['distinct_object'] = {}
        self.distinct_seen = LimitedSizeDict(size_limit=300000) # FIXME: make limit configurable

    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # count all properties
        self.histogram[p] = self.histogram.get(p, 0) + 1
        # distinct
        spo = s+p+o
        if not dh.query_distinct_spo(spo, 0):
            dh.set_distinct_spo(spo, 0)
            self.distinct[p] = self.distinct.get(p, 0) + 1
        # per subject
        sp = s+p
        if len(sp) > 16:
            sp_hash = hashlib.md5(sp).digest()
        else:
            sp_hash = sp
        if not self.distinct_seen.has_key(sp_hash):
            self.distinct_seen[sp_hash] = 1
            self.distinct_subject[p] = self.distinct_subject.get(p, 0) + 1
        # per object
        po = p+o
        if len(po) > 16:
            po_hash = hashlib.md5(po).digest()
        else:
            po_hash = po
        if not self.distinct_seen.has_key(po_hash):
            self.distinct_seen[po_hash] = 1
            self.distinct_object[p] = self.distinct_object.get(p, 0) + 1
    
    def voidify(self, void_model, dataset):
        # count
        result_node = RDF.Node(literal=str(len(self.histogram)), datatype=ns_xs.integer.uri)
        void_model.append(RDF.Statement(dataset, ns_void.properties, result_node))
        # property partition
        for property_uri,result in self.distinct.iteritems():
            pr_id = RDF.Node()
            void_model.append(RDF.Statement(dataset, ns_void.propertyPartition, pr_id))
            void_model.append(RDF.Statement(pr_id, ns_void.property, RDF.Uri(property_uri)))
            result_node = RDF.Node(literal=str(result), datatype=ns_xs.integer.uri)
            void_model.append(RDF.Statement(pr_id, ns_void.triples, result_node))
            if self.distinct_subject.has_key(property_uri):
                s_result = self.distinct_subject[property_uri]
                result_node = RDF.Node(literal=str(s_result), datatype=ns_xs.integer.uri)
                void_model.append(RDF.Statement(pr_id, ns_void.distinctSubjects, result_node))
            if self.distinct_object.has_key(property_uri):
                o_result = self.distinct_object[property_uri]
                result_node = RDF.Node(literal=str(o_result), datatype=ns_xs.integer.uri)
                void_model.append(RDF.Statement(pr_id, ns_void.distinctObjects, result_node))
    
    def sparql(self, endpoint):
        pass

