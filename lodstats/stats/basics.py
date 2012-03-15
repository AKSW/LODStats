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
import distincthelper as dh
from lodstats.util.namespace import ns_xs, ns_void

class Entities(RDFStatInterface):
    """count entities (triple has an URI as subject, distinct)"""
    def __init__(self, results):
        super(Entities, self).__init__(results)
        self.results['count'] = 0
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if statement.subject.is_resource and not dh.query_distinct_subject(s, 0):
          self.results['count'] += 1
          dh.set_distinct_subject(s, 0)
    
    def voidify(self, void_model, dataset):
        result_node = RDF.Node(literal=str(self.results['count']), datatype=ns_xs.integer.uri)
        void_model.append(RDF.Statement(dataset, ns_void.entities, result_node))
    
    def sparql(self, endpoint):
        pass

class Literals(RDFStatInterface):
    def __init__(self, results):
        """number of triples with literals"""
        super(Literals, self).__init__(results)
        self.results['count'] = 0
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if o_l:
            self.results['count'] += 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

class Blanks(RDFStatInterface):
    def __init__(self, results):
        """number of triples with blank nodes, overall and as subject, object"""
        super(Blanks, self).__init__(results)
        self.results['count'] = 0
        self.results['s'] = 0
        self.results['o'] = 0
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if s_blank or o_blank:
            self.results['count'] += 1
        if s_blank:
            self.results['s'] += 1
        if o_blank:
            self.results['o'] += 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

class Subclasses(RDFStatInterface):
    def __init__(self, results):
        """number of subclasses"""
        super(Subclasses, self).__init__(results)
        self.results['count'] = 0
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if p == 'http://www.w3.org/2000/01/rdf-schema#subClassOf':
            self.results['count'] += 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

class TypedSubjects(RDFStatInterface):
    """number of typed subjects"""
    def __init__(self, results):
        super(TypedSubjects, self).__init__(results)
        self.results['count'] = 0
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and not dh.query_distinct_subject(s, 1):
            self.results['count'] += 1
            dh.set_distinct_subject(s, 1)
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

class LabeledSubjects(RDFStatInterface):
    """number of labeled subjects"""
    def __init__(self, results):
        super(LabeledSubjects, self).__init__(results)
        self.results['count'] = 0
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if p == 'http://www.w3.org/2000/01/rdf-schema#label' and not dh.query_distinct_subject(s, 2):
            self.results['count'] += 1
            dh.set_distinct_subject(s, 2)
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

class SameAs(RDFStatInterface):
    """number of triples with owl#sameAs as predicate"""
    def __init__(self, results):
        super(SameAs, self).__init__(results)
        self.results['count'] = 0
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if p == 'http://www.w3.org/2002/07/owl#sameAs':
            self.results['count'] +=1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

class LiteralsList(RDFStatInterface):
    """literal objects seen"""
    def __init__(self, results):
        super(LiteralsList, self).__init__(results)
        self.results['literal_objects'] = {}
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
         if o_l:
             self.results['literal_objects'][o] = self.results['literal_objects'].get(o, 0) + 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

