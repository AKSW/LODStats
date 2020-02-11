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

class StringLength(RDFStatInterface):
    """average length of untyped/string literals"""
    
    def __init__(self, results):
        super(StringLength, self).__init__(results)
        self.literals_untyped = 0
        self.length_untyped = 0
        self.results['avg_untyped'] = 0
        self.literals_typed = 0
        self.length_typed = 0
        self.results['avg_typed'] = 0
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if o_l and statement.object.literal_value['datatype'] is None:
            self.literals_untyped += 1
            self.length_untyped += len(o)
        if o_l and str(statement.object.literal_value['datatype']) == "http://www.w3.org/2001/XMLSchema#string":
            self.literals_typed += 1
            self.length_typed += len(o)
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass
    
    def postproc(self):
        if self.literals_typed > 1:
            self.results['avg_typed'] = self.length_typed/self.literals_typed
        else:
            self.results['avg_typed'] = self.length_typed
        if self.literals_untyped > 1:
            self.results['avg_untyped'] = self.length_untyped/self.literals_untyped
        else:
            self.results['avg_untyped'] = self.length_untyped

