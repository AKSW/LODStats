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
from .RDFStatInterface import RDFStatInterface
from lodstats.util.namespace import get_namespace, ns_void

class Vocabularies(RDFStatInterface):
    """count usage of vocabularies"""
    
    def __init__(self, results):
        super(Vocabularies, self).__init__(results)
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # count triples that use some vocabulary (via its base-URI, hope that's not silly)
        # if not s_blank:
        #     base_uri = get_namespace(s)
        #     if base_uri:
        #         self.results[base_uri] = self.results.get(base_uri, 0) + 1
        base_uri = get_namespace(p)
        if base_uri:
            self.results[base_uri] = self.results.get(base_uri, 0) + 1
        # if not (o_blank or o_l):
        #     base_uri = get_namespace(o)
        #     if base_uri:
        #         self.results[base_uri] = self.results.get(base_uri, 0) + 1
    
    def voidify(self, void_model, dataset):
        for base_uri,result in self.results.items():
            if result > 0:
                void_model.append(RDF.Statement(dataset, ns_void.vocabulary, RDF.Uri(base_uri)))
    
    def sparql(self, endpoint):
        pass


class VocabulariesPerNode(RDFStatInterface):
    """count usage of vocabularies as subject, predicate, object"""
    def __init__(self, results):
        super(VocabulariesPerNode, self).__init__(results)
        self.results['s'] = {}
        self.results['p'] = {}
        self.results['o'] = {}
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # count triples that use some vocabulary (via its base-URI, hope that's not silly)
        s_namespace = get_namespace(s)
        if s_namespace:
            self.results['s'][s_namespace] = self.results['s'].get(s_namespace, 0) + 1
        p_namespace = get_namespace(p)
        if p_namespace:
            self.results['p'][p_namespace] = self.results['p'].get(p_namespace, 0) + 1
        o_namespace = get_namespace(o)
        if o_namespace:
            self.results['o'][o_namespace] = self.results['o'].get(o_namespace, 0) + 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

