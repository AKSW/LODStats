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
import RDF

def get_format(url):
    lowerurl = url.lower()
    # guess serialization format from URL
    if lowerurl.endswith("ttl"):
        format = "ttl"
    elif lowerurl.endswith("nt"):
        format = "nt"
    elif lowerurl.endswith('n3'):
        format = 'n3'
    elif any(lowerurl.endswith(x) for x in ('rdf', 'owl', 'rdfs')):
        format = 'rdf'
    elif lowerurl.endswith('.nq'):
        format = 'nq'
    elif any(lowerurl.endswith(x) for x in ('sparql', 'sparql/')):
        format = 'sparql'
    else:
        raise NameError("could not guess format")
    return format

def get_parser(url, format=None):
    if format is None:
        format = get_format(url)
    
    if format == 'ttl':
        parser = RDF.TurtleParser()
    elif format == 'nt' or format == 'n3': # FIXME: this probably won't do for n3
        parser = RDF.NTriplesParser()
    elif format == 'nq':
        parser = RDF.Parser(name='nquads')
    elif format == 'rdf':
        parser = RDF.Parser(name="rdfxml")
    elif format == 'sparql':
        pass
    else:
        raise NameError("unsupported format")
    return parser
