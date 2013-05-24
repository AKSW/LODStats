"""
Copyright 2013 AKSW Research group http://aksw.org/

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

class ClassesDefined(RDFStatInterface):
    """
        Used Classes Criterion
        Output format: {'classname': usage count}
    """

    def __init__(self, results):
        super(ClassesDefined, self).__init__(results)
        self.usage_count = self.results['usage_count'] = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):

        # "classes defined" criterion filter
        if (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2000/01/rdf-schema#Class') or\
           (p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and o == 'http://www.w3.org/2002/07/owl#Class'):
            self.usage_count[s] = 0
        # count usage of defined classes
        # if class is used as object
        if p == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and self.usage_count.has_key(o):
            self.usage_count[o] += 1
    
    def voidify(self, void_model, dataset):
        pass

    def postproc(self):
        self.count = self.results['count'] = len(self.usage_count)

    def sparql(sparql, endpoint):
        pass
