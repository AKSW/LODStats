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

class Datatypes(RDFStatInterface):
    """histogram of types used for literals"""
    
    def __init__(self, results):
        super(Datatypes, self).__init__(results)
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if o_l and statement.object.literal_value['datatype'] is not None:
            data_type = unicode(statement.object.literal_value['datatype'])
            self.results[data_type] = self.results.get(data_type, 0) + 1
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass
