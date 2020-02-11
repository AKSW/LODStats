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

class PropertiesPerEntity(RDFStatInterface):
    """count all properties"""
    def __init__(self, results):
        super(PropertiesPerEntity, self).__init__(results)
        self.current_subject = ''
        self.properties = {}
        self.subjects = 0
        self.results['avg'] = 0
        self.sum = 0

#FIXME: vielleicht immer die letzen 10-100 props merken, um bei "out of order" serialisierung besser zu performen
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if not s_blank and self.current_subject != s:
            self.sum += len(self.properties)
            if self.subjects > 0:
                self.results['avg'] = self.sum/float(self.subjects)
            else:
                self.results['avg'] = self.sum
            self.current_subject = s
            self.subjects += 1
            self.properties = {}
        # count all properties
        self.properties[p] = self.properties.get(p, 0) + 1

    def voidify(self, void_model, dataset):
        pass

    def sparql(self, endpoint):
        pass
