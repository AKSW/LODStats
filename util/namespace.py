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

# "namespaces" we're cheating on as not to get millions of links
namespace_exceptions = ['http://en.wikipedia.org/wiki', 'http://id.loc.gov/authorities', 'http://www.yovisto.com/resource',
                        'http://dblp.uni-trier.de/db', 'http://sws.geonames.org/', 'http://minsky.gsi.dit.upm.es/semanticwiki',
                        'http://id.southampton.ac.uk/syllabus', 'http://www.myexperiment.org/workflows', 'http://data.southampton.ac.uk/dumps',
                        'http://eprints.ecs.soton.ac.uk/', 'http://iserve.kmi.open.ac.uk/resource/services',
                        'http://id.southampton.ac.uk/point-of-service', 'http://semanticweb.org/wiki', 'http://id.southampton.ac.uk/building',
                        'http://telegraphis.net/data', 'http://www.pokepedia.fr/index.php', 'http://localhost/index.php',
                        'http://atlantides.org/capgrids', 'http://xkcd.com/', 'http://pleiades.stoa.org/places',
                        'http://enipedia.tudelft.nl/wiki', 'http://dx.doi.org/', 'http://www.edshare.soton.ac.uk/',
                        'http://api.talis.com/stores/govuk-statistics', 'http://catalogo.bn.pt/ipac20', 'http://patrimonia.porbase.org/',
                        'http://purl.pt/', 'http://europeanastatic.eu/api', 'http://id.southampton.ac.uk/vending-machine',
                        'http://dbpedia.org/resource', 'http://viaf.org/viaf']

def get_namespace(uri):
    '''extract namespace from uris'''
    # FIXME: just get those using http for now
    if not uri.startswith('http://'):
        return None
    # special handling of some namespaces, see above
    for namespace in namespace_exceptions:
        if uri.startswith(namespace):
            return namespace
    uri_no_http = uri[len('http://'):]
    for sep in ['#', ':']:
        split_uri = uri_no_http.rsplit(sep, 1)
        if len(split_uri) == 2:
            # base_uri is uri minus non-namepsace-part and separator
            return uri[:-(len(split_uri[1])+1)]
    # must be an uri with only '/' as separator now
    split_uri = uri_no_http.split('/', 2)
    if len(split_uri) == 3:
        return uri[:-(len(split_uri[2])+1)]
    elif len(split_uri) == 2:
        return uri[:-(len(split_uri[1])+1)]
    else:
        return None
    
def remove_namespace(uri):
    namespace = get_namespace(uri)
    return uri[len(namespace)+1:]
