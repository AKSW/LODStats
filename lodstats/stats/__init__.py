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
from UsedClasses import UsedClasses
from ClassesDefined import ClassesDefined
from ClassHierarchyDepth import *
from PropertyUsage import PropertyUsage
from PropertyUsageDistinctPerSubject import PropertyUsageDistinctPerSubject
from PropertyUsageDistinctPerObject import PropertyUsageDistinctPerObject
from Outdegree import Outdegree
from Indegree import Indegree
from PropertyHierarchyDepth import PropertyHierarchyDepth
from SubclassUsage import SubclassUsage
from Entities import Entities

from Vocabularies import *
from basics import Literals, Blanks, Subclasses, TypedSubjects, LabeledSubjects, SameAs, LiteralsList
from CookieCounter import *
from StringLength import *
from Languages import *
from Datatypes import *
from PropertiesPerEntity import *
from Links import *
from RDFSyntax import *
from RDFSchema import *
from Owl import *
from PropertyHierarchy import *

# test
test_stats = [Indegree, Outdegree, PropertyHierarchyDepth, SubclassUsage, Entities]
# add Python-classes for doing stats here after importing them above:
available_stats = [UsedClasses, ClassesDefined, ClassHierarchyDepth, PropertyUsage,\
        Vocabularies, VocabulariesPerNode, Entities, Literals, Blanks,\
        Subclasses, TypedSubjects, LabeledSubjects, Languages, StringLength, PropertiesPerEntity,\
        RDFSyntax, RDFSchema, Owl, PropertyHierarchy, Links, Datatypes, SameAs]
# stuff usually run for lodstats/web
lodstats = [UsedClasses, ClassesDefined, Vocabularies, Entities, Literals, Blanks,\
    Subclasses, TypedSubjects, LabeledSubjects, Languages, StringLength, PropertiesPerEntity,\
    ClassHierarchyDepth, PropertyHierarchy, Links, Datatypes]
# not so useful/redundant optional stuff
stupid_stats = [LiteralsList, CookieCounter]
# stats for owl, rdf-schema, -syntax
vocab_stats = [RDFSyntax, RDFSchema, Owl]
# stats necessary for VoiD
void_stats = [UsedClasses, Vocabularies, Entities]
# links only
link_stats = [Links]

# will hold the objects doing the stats, initialized in init_stats()
stats_to_do = []
results = {}
# init stats-objects, only do void by default
def init_stats(stats_list=void_stats):
    """init classes from stats_list, those necessary for VoID per default"""
    for stat_class in stats_list:
        stats_to_do.append(stat_class(results))
    return results

# gather data
def run_stats(s, p, o, s_blank, o_l, o_blank, statement):
    """submit one triple to objects calculating stats"""
    for stat_object in stats_to_do:
        stat_object.count(s, p, o, s_blank, o_l, o_blank, statement)

def run_stats_sparql(endpoint):
    from SPARQLWrapper import SPARQLWrapper
    
    sparql = SPARQLWrapper(endpoint)
        
    for stat_object in stats_to_do:
        stat_object.sparql(sparql)

def postproc():
    for stat_object in stats_to_do:
        stat_object.postproc()
