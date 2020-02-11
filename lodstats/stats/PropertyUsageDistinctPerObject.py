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
from .RDFStatInterface import RDFStatInterface
from hashlib import md5

class PropertyUsageDistinctPerObject(RDFStatInterface):
    """count properties that show up as predicate, works in combination with properties_histogram
       FIXME: sind properties immer "zuerst" definiert? wahrscheinlich nicht, dann klappt es leider so nicht richtig"""
    def __init__(self, results):
        super(PropertyUsageDistinctPerObject, self).__init__(results)
        self.usage_count = self.results['usage_count'] = {}
        self.digest_list = []

    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        po = p+o
        hash = md5.new()
        hash.update(po)
        digest = hash.hexdigest()
        if not digest in self.digest_list:
            self.digest_list.append(digest)
            self.usage_count[p] = self.usage_count.get(p, 0) + 1

    def voidify(self, void_model, dataset):
        pass

    def sparql(self, endpoint):
        pass

    def postproc(self):
        pass
