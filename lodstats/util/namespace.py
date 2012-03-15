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

# some often used namespaces
ns_xs = RDF.NS("http://www.w3.org/2001/XMLSchema#")
ns_void = RDF.NS("http://rdfs.org/ns/void#")
ns_rdf = RDF.NS("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
ns_stats = RDF.NS("http://example.org/XStats#")
ns_qb = RDF.NS("http://purl.org/linked-data/cube#")

def get_namespace(uri):
    '''extract namespace from uris'''
    # FIXME: just get those using http for now
    if not uri.startswith('http://'):
        return None
    uri_no_http = uri[len('http://'):]
    for sep in ['#', ':', '/']:
        split_uri = uri_no_http.rsplit(sep, 1)
        if len(split_uri) == 2:
            # base_uri is uri minus non-namepsace-part and separator
            return uri[:-(len(split_uri[1])+1)]
    return None
    
def remove_namespace(uri):
    namespace = get_namespace(uri)
    return uri[len(namespace)+1:]
