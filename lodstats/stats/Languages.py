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

class Languages(RDFStatInterface):
    """list and count languages found"""
    
    def __init__(self, results):
        super(Languages, self).__init__(results)
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        # check if subject, predicate or object contain cookies
        if o_l and statement.object.literal_value['language'] is not None:
            lang = str(statement.object.literal_value['language'])
            self.results[lang] = self.results.get(lang, 0) + 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

