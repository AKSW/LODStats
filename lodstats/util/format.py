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
import logging
logger = logging.getLogger("lodstats.format")

def parse_sitemap(url):
    from xml.etree import ElementTree as etree
    from io import StringIO
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
