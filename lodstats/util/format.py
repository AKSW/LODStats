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
import logging
logger = logging.getLogger("lodstats.format")

def get_format(url):
    logger.debug("get_format(%s)" % url)
    process_url = url.split('/')[-1]
    process_url = process_url.split('.')

    for item in process_url:
        if(item == 'ttl'):
            return 'ttl'
        if(item == 'nt'):
            return 'nt'
        if(item == 'n3'):
            return 'n3'
        if(item == 'rdf' or item == 'owl' or item == 'rdfs'):
            return 'rdf'
        if(item == 'nq'):
            return 'nq'
        if(item == 'sparql' or item == 'sparql/'):
            return 'sparql'
        if(item == 'sitemap'):
            return 'sitemap'
    raise NameError("could not guess format")

def get_parser(format):
    
    if format == 'ttl':
        parser = RDF.TurtleParser()
    elif format == 'nt' or format == 'n3': # FIXME: this probably won't do for n3
        parser = RDF.NTriplesParser()
    elif format == 'nq':
        parser = RDF.Parser(name='nquads')
    elif format == 'rdf':
        parser = RDF.Parser(name="rdfxml")
    elif format == 'sparql':
        return None
    elif format == 'sitemap':
        return None
    else:
        raise NameError("unsupported format")

    return parser

def parse_sitemap(url):
    from xml.etree import ElementTree as etree
    from cStringIO import StringIO
    import requests
    
    sitemap = requests.get(url)
    stringio = StringIO(sitemap.text)
    
    tree = etree.parse(stringio)
    context = tree.getiterator()

    datadumps = []
    
    for elem in context:
        if elem.tag == '{http://sw.deri.org/2007/07/sitemapextension/scschema.xsd}dataDumpLocation':
            datadumps.append(elem.text)
    
    return datadumps
