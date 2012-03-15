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
from RDFStatInterface import RDFStatInterface
from lodstats.util.namespace import ns_xs, ns_void, ns_rdf, ns_stats, ns_qb

class ClassHierarchy(RDFStatInterface):
    """gather hierarchy of classes seen"""
    
    def __init__(self, results):
        super(ClassHierarchy, self).__init__(results)
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2000/01/rdf-schema#Class':
            self.results[s] = 0
        if p == 'http://www.w3.org/2000/01/rdf-schema#subClassOf':
            if self.results.has_key(o):
                self.results[s] = self.results[o] + 1
            else:
                self.results[o] = 0
                self.results[s] = 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass
