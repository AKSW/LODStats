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
from .RDFStatInterface import RDFStatInterface

class CookieCounter(RDFStatInterface):
    """count tasty cookies"""
    
    def __init__(self, results):
        super(CookieCounter, self).__init__(results)
        self.results['count'] = 0;
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # check if subject, predicate or object contain cookies
        if any("cookies" in x for x in (s, p, o)):
            self.results['count'] += 1
    
    def sparql(self, endpoint):
        pass

