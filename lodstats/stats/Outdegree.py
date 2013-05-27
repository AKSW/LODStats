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

class Outdegree(RDFStatInterface):
    def __init__(self, results):
        super(Outdegree, self).__init__(results)
        self.usage_count = {}
        
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        self.usage_count[s] = self.usage_count.get(s, 0) + 1
    
    def postproc(self):
        usage_overall = 0
        for usage in self.usage_count:
            usage_overall += self.usage_count[usage]
        outdegree = float(usage_overall) / float(len(self.usage_count))
        self.count = self.results['count'] = outdegree

    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass
