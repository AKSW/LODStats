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

class PropertyHierarchyDepth(RDFStatInterface):
    """gather hierarchy of classes seen"""
    
    def __init__(self, results):
        super(PropertyHierarchyDepth, self).__init__(results)
        self.graph = self.results['graph'] = {}
        self.c = self.results['count'] = 0
    
    def count(self, s, p, o, s_blank, o_l, o_blank, statement):
        if statement.object.is_resource() and \
                statement.subject.is_resource() and \
                p == 'http://www.w3.org/2000/01/rdf-schema#subPropertyOf':
            self.graph[s] = o
    
    def voidify(self, void_model, dataset):
        pass
    
    def sparql(self, endpoint):
        pass

    def postproc(self):
        final_depth = 0
        for root_object, root_subject in self.results['graph'].items():
            depth = 0
            objects_encountered = []
            new_depth = self.get_depth(root_subject, self.results['graph'], depth, objects_encountered)
            if(new_depth > final_depth):
                final_depth = new_depth
        self.c = self.results['count'] = final_depth

    def get_depth(self, root_subject, graph, depth, objects_encountered):
        """
            TODO: recursive! check if it scales
        """
        new_depth = depth
        for object, subject in graph.items():
            if(object == root_subject):
                new_depth += 1
                objects_encountered.append(object)
                new_depth = self.get_depth(subject, graph, new_depth, objects_encountered)
                break
            if(new_depth > len(graph)):
                return 0
        return new_depth
