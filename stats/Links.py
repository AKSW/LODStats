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
from ..util.namespace import get_namespace

class Links(RDFStatInterface):
    """count links (object vocabulary != subject vocabulary)"""
    def __init__(self, results):
        super(Links, self).__init__(results)
        self.results['count'] = 0
        self.ns_links = self.results['namespacelinks'] = {}
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # count triples with obj. vocabulary not in subj. vocabulary)
        if not (statement.subject.is_resource and statement.object.is_resource):
            return
        
        subject_uri = get_namespace(s)
        object_uri = get_namespace(o)
        
        if object_uri is None or subject_uri is None:
            return
        
        if subject_uri != object_uri:
            self.results['count'] += 1
            so_uri = subject_uri+object_uri
            self.ns_links[so_uri] = self.ns_links.get(so_uri, 0) + 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

