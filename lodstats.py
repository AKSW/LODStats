#!/usr/bin/env python
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

import os
import sys
import datetime
from optparse import OptionParser

from lodstats import RDFStats
from lodstats.stats import available_stats, vocab_stats, lodstats, ParsedVocabulary

parser = OptionParser(usage="usage: %prog [options] [-m model.{rdf,nt,...}] file/URI")
parser.add_option('-f', '--format', help='format (nt/rdf/ttl/n3/nq, guessed by default)')
parser.add_option('-v', '--void', action='store_true', help='generate VoID')
parser.add_option('-c', '--count', action='store_true', help='just count triples, no statistics')
parser.add_option('-p', '--progress', action='store_true', help='show progress')
parser.add_option('-a', '--all-stats', action='store_true', help='do all available statistics')
parser.add_option('-l', '--lod-stats', action='store_true', help='do statistics for lodstats')
parser.add_option('-i', '--intermediate-stats', action='store_true', help='print intermediate statistics every 100k triples')
parser.add_option('-m', '--rdf-model', help='parse and do stats for everything that isDefinedBy supplied model')
parser.add_option('-s', '--schema-syntax-owl', action='store_true', help='do stats for RDF-Schema, -Syntax, Owl')
(options, args) = parser.parse_args()

if len(args) == 0 or len(args) > 1:
    parser.print_help()
    exit(2)
resource = args[0]
is_remote = resource.lower().startswith('http://') or resource.lower().startswith('https://')
if not is_remote and not os.access(resource, os.R_OK):
    print("File not found/unreadable")
    exit(3)
if not is_remote:
    resource = "file://%s" % os.path.realpath(resource)

if options.rdf_model:
    options.all_stats = False
    options.count = False
    options.void = False
    model_stats = [ParsedVocabulary, options.rdf_model]
    a = RDFStats(resource, format=options.format, stats=[], new_stats=model_stats)
elif options.schema_syntax_owl:
    a = RDFStats(resource, format=options.format, stats=vocab_stats)
elif options.all_stats:
    options.count = False
    a = RDFStats(resource, format=options.format, stats=available_stats)
elif options.lod_stats:
    options.count = False
    a = RDFStats(resource, format=options.format, stats=lodstats)
else:
    a = RDFStats(resource, format=options.format, do_custom_stats=not options.count)
    
def callback_parser(rdfdocstat):
    now = datetime.datetime.now()
    time_delta = (now-rdfdocstat.start_time).seconds
    if time_delta > 0:
        print("\r%d of %d KB loaded, %d KB/s, %d KB uncomp." % (rdfdocstat.bytes_download/1024,
        rdfdocstat.content_length/1024, (rdfdocstat.bytes_download/1024)/time_delta, rdfdocstat.bytes/1024)),
        sys.stdout.flush()
    else:
        print("\r%d of %d KB loaded, %d KB uncomp." % (rdfdocstat.bytes_download/1024,
        rdfdocstat.content_length/1024, rdfdocstat.bytes/1024)),
        sys.stdout.flush()

if options.progress:
    a.parse(callback_parser)
else:
    a.parse()
if is_remote and options.progress:
    #clear console
    manyspaces = ' '*72
    print("\r%s" % manyspaces),
    sys.stdout.flush()
    now = datetime.datetime.now()
    time_delta = (now-a.start_time).seconds
    if time_delta > 0:
        print("\rFetch done, %d of %d KB loaded, %d KB/s, %d KB uncomp." % (a.bytes_download/1024,
            a.content_length/1024, (a.bytes_download/1024)/time_delta, a.bytes/1024))
    else:
        print("\rFetch done, %d of %d KB loaded, %d KB uncomp." % (a.bytes_download/1024,
            a.content_length/1024, a.bytes/1024))

def callback(rdfdocstat):
    if rdfdocstat.no_of_statements > 0:
        now = datetime.datetime.now()
        time_delta = (now-rdfdocstat.start_time).seconds
        if time_delta > 0:
            print("\r%d triples done, %d/s, %d warnings" % (rdfdocstat.no_of_statements,
            rdfdocstat.no_of_statements/time_delta, rdfdocstat.warnings)),
        else:
            print("\r%d triples done, %d warnings" % (rdfdocstat.no_of_statements,
            rdfdocstat.warnings)),
        if rdfdocstat.files_handled > 0:
            print("%d files" % (rdfdocstat.files_handled+1)),
        sys.stdout.flush()
        if not options.count and options.intermediate_stats and rdfdocstat.no_of_statements % 100000 == 0:
            print("Results (from custom code):")
            for stat_name,stat_dict in rdfdocstat.stats_results.iteritems():
                print("\t%s" % stat_name)
                for subname, result in stat_dict.iteritems():
                    if type(result) == dict or type(result) == list:
                        print("\t\tlen(%s): %d" % (subname, len(result)))
                    else:
                        print("\t\t%s: %s" % (subname, result))

if options.progress:
    a.do_stats(callback)
else:
    a.do_stats()
if options.progress:
    #clear console
    manyspaces = ' '*72
    print("\r%s" % manyspaces),
    sys.stdout.flush()
    # print status one final time
    time_delta = (datetime.datetime.now()-a.start_time).seconds
    if time_delta > 0:
        print("\r%d triples done, %d/s, %d warnings" % (a.no_of_statements,
        a.no_of_statements/time_delta, a.warnings))

if options.void:
    # make void
    print(a.voidify("turtle"))

if not options.void:
    print("Basic stats: %s triples, %s warnings" % (a.no_of_triples(), a.warnings))
    if not options.count:
        print("Results (from custom code):")
        for stat_name,stat_dict in a.stats_results.iteritems():
            print("\t%s" % stat_name)
            for subname, result in stat_dict.iteritems():
                if type(result) == dict or type(result) == list:
                    if subname in ('s','p','o', 'namespacelinks'):
                        print("\t\t%s:" % subname)
                        for subsubname, subresult in result.iteritems():
                            if subresult > 0:
                                print("\t\t%s: %s" % (subsubname, subresult))
                    else:
                        print("\t\tlen(%s): %d" % (subname, len(result)))
                else:
                    print("\t\t%s: %s" % (subname, result))

