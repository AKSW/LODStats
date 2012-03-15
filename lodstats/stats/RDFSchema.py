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
from os.path import dirname
from ParsedVocabulary import ParsedVocabulary

class RDFSchema(ParsedVocabulary):
    """count usage of everything that #isDefinedBy some vocabulary"""
    
    def __init__(self, results):
        model = dirname(__file__) + "/../rdf/rdf-schema.rdf"
        super(RDFSchema, self).__init__(results, model)
