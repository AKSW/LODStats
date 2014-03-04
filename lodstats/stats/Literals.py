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

class Literals(RDFStatInterface):
    """
        Distinct number of entities
        Entity - triple, where ?s is iri (not blank)
    """
    def __init__(self, results):
        super(Literals, self).__init__(results)
        self.c = 0
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if o_l:
            self.c += 1
    
    def postproc(self):
        self.results['count'] = self.c

    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        from SPARQLWrapper import JSON
        endpoint.setQuery("SELECT (count(distinct ?l) AS ?literals) WHERE { ?s ?p ?l . filter(isLiteral(?l)) }")
        endpoint.setReturnFormat(JSON)
        results = endpoint.query().convert()
        if not isinstance(results, dict):
            raise Exception, "unknown response content type"
        self.c = int(results['results']['bindings'][0]['literals']['value'])
