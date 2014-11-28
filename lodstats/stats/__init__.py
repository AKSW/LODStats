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
from PropertiesDefined import PropertiesDefined
from PropertyUsageDistinctPerSubject import PropertyUsageDistinctPerSubject
from PropertyUsageDistinctPerObject import PropertyUsageDistinctPerObject
from PropertiesPerEntity import PropertiesPerEntity
from Outdegree import Outdegree
from Indegree import Indegree
from PropertyHierarchyDepth import PropertyHierarchyDepth
from SubclassUsage import SubclassUsage
from Entities import Entities
from Literals import Literals
from BlanksAsSubject import BlanksAsSubject
from BlanksAsObject import BlanksAsObject
from Datatypes import Datatypes
from Languages import Languages
from StringLength import StringLength
from TypedSubjects import TypedSubjects
from LabeledSubjects import LabeledSubjects
from SameAs import SameAs
from Links import Links
# max per property
# avg per property
from Vocabularies import Vocabularies, VocabulariesPerNode

#Void specific
from DistinctSubjects import DistinctSubjects
from DistinctObjects import DistinctObjects

from basics import LiteralsList
from CookieCounter import *

#vocabulary count
from RDFSyntax import RDFSyntax
from RDFSchema import RDFSchema
from Owl import Owl

# test
test_stats = [PropertyUsageDistinctPerSubject]
# add Python-classes for doing stats here after importing them above:
available_stats = [ClassesDefined, UsedClasses, ClassHierarchyDepth, PropertiesDefined, PropertyUsage, PropertyUsageDistinctPerSubject, PropertyUsageDistinctPerObject,\
        Outdegree, Indegree, PropertyHierarchyDepth, SubclassUsage, Entities, Literals, BlanksAsSubject, BlanksAsObject, Datatypes,\
        Languages, StringLength, TypedSubjects, LabeledSubjects, SameAs, Links, Vocabularies, VocabulariesPerNode]
# stuff usually run for lodstats/web
lodstats_old = [UsedClasses, Vocabularies, PropertiesDefined, PropertyUsage, ClassesDefined, Entities, Literals, BlanksAsObject, BlanksAsSubject,\
                SubclassUsage, TypedSubjects, LabeledSubjects, ClassHierarchyDepth, PropertyHierarchyDepth, PropertiesPerEntity,\
                StringLength, Links, Datatypes, Languages]
lodstats = [ClassesDefined, UsedClasses, ClassHierarchyDepth, PropertiesDefined, PropertyUsage,\
        PropertyHierarchyDepth, SubclassUsage, Entities, Literals, BlanksAsSubject, BlanksAsObject, Datatypes,\
        Languages, StringLength, TypedSubjects, LabeledSubjects, SameAs, Links, Vocabularies, VocabulariesPerNode, PropertiesPerEntity]
slow_stats = [PropertyUsageDistinctPerSubject, PropertyUsageDistinctPerObject]
memory_stats = [Indegree, Outdegree, TypedSubjects, Entities]
#lodstats_new = lodstats - lodstats_old = what's missing on the site

# not so useful/redundant optional stuff
stupid_stats = [LiteralsList, CookieCounter]
# stats for owl, rdf-schema, -syntax
vocab_stats = [RDFSyntax, RDFSchema, Owl]
# stats necessary for VoiD
void_stats = [Vocabularies, Entities, ClassesDefined, UsedClasses, PropertiesDefined, PropertyUsage, DistinctSubjects, DistinctObjects]
# links only
link_stats = [Links]

# will hold the objects doing the stats, initialized in init_stats()
stats_to_do = []
results = {}
# init stats-objects, only do void by default
def init_stats(stats_list=void_stats):
    #stats_to_do = []
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
