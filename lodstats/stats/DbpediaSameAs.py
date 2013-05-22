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
import re

class DbpediaSameAs(RDFStatInterface):
    """count links (object vocabulary != subject vocabulary)"""
    def __init__(self, results):
        super(DbpediaSameAs, self).__init__(results)
        self.results['count'] = 0
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        
        #if triple has owl:sameAs property
        if(re.search('owl.*sameAs', p)):
            if(o.startswith('http://dbpedia.org')):
                self.results['count'] += 1
        else:
            return

    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

