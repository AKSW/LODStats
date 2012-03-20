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
"""Parse RDF and do some stats"""
import RDF
import os
import datetime
import gzip
import bz2
import tarfile
import zipfile
import tempfile
import urllib2
import requests # FIXME: kick out urllib2 and only use requests
import warnings
import lodstats.stats as custom_stats
import lodstats.util as util
import exceptions

class RDFStats(object):
    """Get some interesting numbers from RDFish resources"""
    def __init__(self, rdfurl, format = None, do_custom_stats = True,
            compression = None, callback_delay_seconds = 2, stats=None,
            new_stats=None):
        self.url = rdfurl
        self.tempurl = None
        self.lowerurl = self.url.lower()
        self.format = format
        self.parser = None
        self.stream = None
        self.no_of_statements = 0
        self.literals = 0
        self.stats_to_do = None
        self.custom_stats = do_custom_stats
        if self.custom_stats and stats is None:
            self.stats_results = custom_stats.init_stats()
        elif self.custom_stats:
            self.stats_results = custom_stats.init_stats(stats)
        if new_stats:
            custom_stats.stats_to_do.append(new_stats[0](self.stats_results, new_stats[1]))
        self.compression = compression
        self.warnings = 0
        self.last_warning = None
        self.start_time = None
        self.end_time = None
        # will hold size of file from http-header / stat() (if local)
        self.content_length = 0
        # bytes downloaded (if remote)
        self.bytes_download = 0
        # bytes after decompression
        self.bytes = 0
        # when last callback was done
        self.last_callback = None
        self.callback_delay = callback_delay_seconds
        # archives
        self.archive = None
        # archives: file entries
        self.file_entries = None
        # archives: files handled
        self.files_handled = 0
        # will hold date of last modification from stat / http header
        self.last_modified = None
    
    """file extensions that will be processed"""
    rdf_extensions = ('.nt', '.rdf', '.ttl', '.n3', '.nq', '.owl', '.rdfs')
    
    def get_compression(self):
        """guess compression of resource"""
        if self.compression is None:
            # archives first
            if any(self.lowerurl.endswith(x) for x in ('.tgz', '.tar.gz', '.tar.bz2')):
                self.compression = 'tar'
            elif self.lowerurl.endswith('.zip'):
                self.compression = 'zip'
            elif self.lowerurl.endswith(".gz"):
                self.lowerurl = self.lowerurl[:-len('.gz')]
                self.compression = 'gz'
            elif self.lowerurl.endswith('.bz2'):
                self.lowerurl = self.lowerurl[:-len('.bz2')]
                self.compression = 'bz2'
    
    def get_format(self):
        # guess format
        if self.format is None:
            self.format = util.format.get_format(self.lowerurl)
        # get parser
        self.parser = util.format.get_parser(self.lowerurl, self.format)
    
    def parse(self, callback_fun = None, if_modified_since = None):
        """parse to redland::Stream"""
        self.start_time = datetime.datetime.now()
        if self.format == 'sparql':
            # FIXME: check availability and support for count() of SPARQL endpoint here
            return
        # local/remote, decompress
        self.get_compression()
        # handle everything http(s) or using some form of archive/compression via urllib2
        if any(self.url.lower().startswith(x) for x in ('http://', 'https://')) or self.compression is not None:
            # check if modified since last visit, TODO: really use http if-modified-since, etags
            last_modified = None
            if any(self.url.lower().startswith(x) for x in ('http://', 'https://')):
                last_modified_request = requests.head(self.url)
                last_modified = last_modified_request.headers.get('last-modified')
            if last_modified is not None:
                self.last_modified = datetime.datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
                if if_modified_since is not None:
                    if self.last_modified == if_modified_since:
                        raise exceptions.NotModified, 'resource has not been modified'
            self.tempfile = tempfile.NamedTemporaryFile(prefix='lodstats')
            remote_resource = urllib2.urlopen(self.url)
            content_length = remote_resource.info().getheader('Content-Length')
            if not content_length is None:
                self.content_length = int(content_length)
            # do not download files bigger than free space/3
            statvfs_out = os.statvfs(tempfile.tempdir)
            free_space = statvfs_out.f_bavail * statvfs_out.f_frsize / 3
            if self.content_length > free_space:
                raise Exception, "file too large (> free space / 3)"
            if not callback_fun is None:
                callback_fun(self)
            # FIXME: take mime-type into account?
            if self.compression == 'gz':
                # gzip does not work on the fly up to 3.2
                gz_tempfile = tempfile.NamedTemporaryFile(prefix='lodstats_gz')
                for data in remote_resource:
                    self.bytes_download += len(data)
                    gz_tempfile.write(data)
                    self.ratelimited_callback_caller(callback_fun)
                gz_tempfile.seek(0)
                gz_temp_decomp = gzip.GzipFile(fileobj=gz_tempfile, mode='rb')
                for data in gz_temp_decomp:
                    self.bytes += len(data)
                    self.tempfile.write(data)
                    self.ratelimited_callback_caller(callback_fun)
                gz_temp_decomp.close()
                gz_tempfile.close()
            elif self.compression == 'bz2':
                decompressor = bz2.BZ2Decompressor()
                for data in remote_resource:
                    self.bytes_download += len(data)
                    decompressed_data = decompressor.decompress(data)
                    self.bytes += len(decompressed_data)
                    self.tempfile.write(decompressed_data)
                    self.ratelimited_callback_caller(callback_fun)
            elif self.compression == 'tar':
                # tar does not seem to work on the fly, like gzip
                tar_tempfile = tempfile.NamedTemporaryFile(prefix='lodstats_tar')
                for data in remote_resource:
                    self.bytes_download += len(data)
                    tar_tempfile.write(data)
                    self.ratelimited_callback_caller(callback_fun)
                tar_tempfile.seek(0)
                self.archive = tarfile.open(fileobj=tar_tempfile, mode='r')
                self.file_entries = self.archive.getmembers()
                self.tempfile.close()
                return
            elif self.compression == 'zip':
                # zip does not seem to work on the fly, like gzip
                zip_tempfile = tempfile.NamedTemporaryFile(prefix='lodstats_zip')
                for data in remote_resource:
                    self.bytes_download += len(data)
                    zip_tempfile.write(data)
                    self.ratelimited_callback_caller(callback_fun)
                zip_tempfile.seek(0)
                self.archive = zipfile.ZipFile(zip_tempfile, 'r')
                self.file_entries = self.archive.infolist()
                self.tempfile.close()
                return
            else:
                for data in remote_resource:
                    self.bytes += len(data)
                    self.bytes_download = self.bytes
                    self.tempfile.write(data)
                    self.ratelimited_callback_caller(callback_fun)
            self.tempfile.flush()
            self.tempurl = "file://%s" % self.tempfile.name
            # call back one last time to push final numbers
            if not callback_fun is None:
                callback_fun(self)
        else:
            self.tempurl = self.url
        self.parse_tempurl()
    
    def parse_tempurl(self):
        self.get_format()
        if self.format == 'sparql':
            return
        self.stream = self.parser.parse_as_stream(self.tempurl)

    def warn_handler(self, message, category, filename, lineno, file=None, line=None):
        self.warnings += 1
        self.last_warning = message
    
    def do_stats(self, callback_fun = None):
        """do the real work"""
        if self.compression in ('tar', 'zip'):
            self.do_archive_stats(callback_fun)
        if self.format != 'sparql':
            with warnings.catch_warnings():
                warnings.showwarning = self.warn_handler
                for statement in self.stream:
                    # count statements
                    self.no_of_statements += 1
            
                    # do custom counting
                    if self.custom_stats:
                        self.do_custom_stats(statement)
                
                    # optional callback (eg for status stuff) every 5000 triples
                    if callback_fun != None and self.no_of_statements % 5000 == 0:
                        callback_fun(self)
        else:
            self.do_sparql_stats()
        
        # post-processing
        if self.custom_stats:
            custom_stats.postproc()
        
        self.end_time = datetime.datetime.now()
        if self.no_of_statements == 0:
            raise Exception, "zero triples"
    
    def do_archive_stats(self, callback_fun):
        """do stats for archives"""
        if self.compression == 'tar':
            for tar_entry in self.file_entries:
                if tar_entry.isfile():
                    # skip files with unknown extensions unless format is known
                    if self.format is None and not any(tar_entry.name.lower().endswith(x) for x in self.rdf_extensions):
                        continue
                    tar_content = self.archive.extractfile(tar_entry)
                    self.tempfile = tempfile.NamedTemporaryFile(prefix='lodstats_tar_entry')
                    for data in tar_content:
                         self.bytes += len(data)
                         self.tempfile.write(data)
                         self.ratelimited_callback_caller(callback_fun)
                    # guess format later if necessary
                    if self.format is None:
                        self.lowerurl = tar_entry.name.lower()
                    # parse and to stats
                    self.tempfile.flush()
                    self.compression = None
                    self.tempurl = "file://%s" % self.tempfile.name
                    self.parse_tempurl()
                    self.do_stats(callback_fun)
                    self.tempfile.close()
                    self.compression = 'tar'
                    self.files_handled += 1
            if self.files_handled == 0:
                raise Exception, "no RDF-ish files found in archive"
            # tar_tempfile.close()
            # tar_file.close()
        elif self.compression == 'zip':
            for zip_entry in self.file_entries:
                # do not handle directories at all
                if not zip_entry.filename.endswith(os.sep):
                    # skip files with unknown extensions unless format is known
                    if self.format is None and not any(zip_entry.filename.lower().endswith(x) for x in self.rdf_extensions):
                        continue
                    zip_content = self.archive.open(zip_entry)
                    self.tempfile = tempfile.NamedTemporaryFile(prefix='lodstats_zip_entry')
                    for data in zip_content:
                        self.bytes += len(data)
                        self.tempfile.write(data)
                        self.ratelimited_callback_caller(callback_fun)
                    # guess format later if necessary
                    if self.format is None:
                        self.lowerurl = zip_entry.filename.lower()
                    # parse and to stats
                    self.tempfile.flush()
                    self.compression = None
                    self.tempurl = "file://%s" % self.tempfile.name
                    self.parse_tempurl()
                    self.do_stats(callback_fun)
                    self.tempfile.close()
                    self.compression = 'zip'
                    self.files_handled += 1
            if self.files_handled == 0:
                raise Exception, "no RDF-ish files found in archive"
            # zip_tempfile.close()
            # zip_file.close()
        else:
            raise Exception, "unknown archive - this should not happen"
    
    def do_sparql_stats(self):
        """do stats via SPARQL"""
        from SPARQLWrapper import SPARQLWrapper, JSON
        sparql = SPARQLWrapper(self.url)
        sparql.setQuery("SELECT (count(*) AS ?triples) WHERE { ?s ?p ?o }")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        self.no_of_statements = int(results['results']['bindings'][0]['triples']['value'])
        
        custom_stats.run_stats_sparql(self.url)
    
    def do_custom_stats(self, statement):
        """call custom stats"""
        # make various things available to the custom code, triple is already there
        results = self.stats_results
        s_blank = statement.subject.is_blank()
        if s_blank:
            s = str(statement.subject)
        else:
            s = str(statement.subject.uri)
        p = str(statement.predicate.uri)
        o_l = statement.object.is_literal()
        o_blank = statement.object.is_blank()
        if o_l or o_blank:
            o = str(statement.object)
        else:
            o = str(statement.object.uri)
        
        custom_stats.run_stats(s, p, o, s_blank, o_l, o_blank, statement)
    
    def ratelimited_callback_caller(self, callback_fun):
        """helper for callbacks that should only fire every self.callback_delay seconds"""
        if callback_fun is None:
            return
        now = datetime.datetime.now()
        if self.last_callback is None:
            self.last_callback = now
            callback_fun(self)
        else:
            time_delta = (now-self.last_callback).seconds
            if time_delta >= self.callback_delay:
                callback_fun(self)
                self.last_callback = now

    # accessors for statistics here
    
    def no_of_triples(self):
        """docstring for notriples"""
        return self.no_of_statements
    
    def no_of_namespaces(self):
        """docstring for noofnamespaces"""
        if self.format != 'sparql':
            return len(self.parser.namespaces_seen())
    
    def voidify(self, serialize_as = "ntriples"):
        """present stats in VoID (http://www.w3.org/TR/void/)"""
        results = self.stats_results
        void_model = RDF.Model()
        ns_void = RDF.NS("http://rdfs.org/ns/void#")
        ns_rdf = RDF.NS("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        ns_xs = RDF.NS("http://www.w3.org/2001/XMLSchema#")
        ns_qb = RDF.NS("http://purl.org/linked-data/cube#")
        ns_stats = RDF.NS("http://example.org/XStats#")
        # FIXME?: our dataset
        dataset = RDF.Uri(self.url)
        dataset_ns = RDF.NS("%s#" % self.url)
        # we're talking about datasets here
        void_model.append(RDF.Statement(dataset,ns_rdf.type,ns_void.Dataset))
        
        # basic stuff: no of triples, ...
        result_node = RDF.Node(literal=str(self.no_of_statements), datatype=ns_xs.integer.uri)
        void_model.append(RDF.Statement(dataset, ns_void.triples, result_node))
        
        # void:observation extension stuff
        void_model.append(RDF.Statement(ns_stats.value, ns_rdf.type, ns_qb.MeasureProperty))
        void_model.append(RDF.Statement(ns_stats.subjectsOfType, ns_rdf.type, ns_qb.DimensonProperty))
        void_model.append(RDF.Statement(ns_stats.schema, ns_rdf.type, ns_qb.AttributeProperty))
        
        # voidify results from custom stats
        for stat in custom_stats.stats_to_do:
            stat.voidify(void_model, dataset)

        # serialize to string and return
        serializer = RDF.Serializer(name=serialize_as)
        serializer.set_namespace("void", "http://rdfs.org/ns/void#")
        serializer.set_namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        serializer.set_namespace("qb", "http://purl.org/linked-data/cube#")
        serializer.set_namespace("xstats", "http://example.org/XStats#")
        #serializer.set_namespace("thisdataset", dataset_ns._prefix)
        return serializer.serialize_model_to_string(void_model)

