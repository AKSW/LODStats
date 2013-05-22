"""
Copyright 2013 AKSW research group -- http://aksw.org/

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
import logging

logger = logging.getLogger("lodstats")

class RDFStats(object):
    """file extensions that will be processed"""
    rdf_extensions = ('.nt', '.rdf', '.ttl', '.n3', '.nq', '.owl', '.rdfs')

    """Get some interesting numbers from RDFish resources"""
    def __init__(self, rdfurl, do_custom_stats = True,
            stats=None, new_stats=None):

        # URI of the file (local file:// or remote http:// https://
        # TODO: url -> uri
        self.url = rdfurl

        # URI of temp file in /temp folder 
        self.tempurl = None

        # RDF format (n3, nt, rdf/xml etc.)
        # Format will be autodetected
        self.format = None 

        # compression of the file .tar, .gz etc.
        # compression is also autodetected
        self.compression_format = self.get_compression()

        # Redland Parser Object
        self.parser = None

        # Stream Object from Redland Parser
        self.stream = None

        # TODO: no_of_statements -> triples_number
        self.no_of_statements = 0

        # not used
        self.literals = 0
        self.stats_to_do = None

        # stats=available_stats object - from lodstats.stats import available_stats, vocab_stats, lodstats, ParsedVocabulary 
        if stats is None:
            self.stats_results = custom_stats.init_stats()
        else:
            self.stats_results = custom_stats.init_stats(stats)

        # this is a hook for parsing vocabulary
        # new_stats = [ParsedVocabulary, options.rdf_model]
        if new_stats:
            custom_stats.stats_to_do.append(new_stats[0](self.stats_results, new_stats[1]))

        # used by warn_handler
        self.warnings = 0
        self.last_warning = None

        # defined in parse()
        self.start_time = None

        # defined in do_stats()
        self.end_time = None

        # will hold size of file from http-header / stat() (if local)
        # content_length = remote_resource.info().getheader('Content-Length')
        self.content_length = 0

        # bytes downloaded (if remote)
        self.bytes_download = 0
        # bytes after decompression
        self.bytes = 0

        # callback functions
        self.callback_parse = None
        self.callback_stats = None
        # when last callback was done
        self.last_callback = None

        #TODO: should be modifiable through config file (in seconds)
        self.callback_delay = 2

        # archives
        self.archive = None
        # archives: file entries
        self.file_entries = None
        # archives: files handled
        self.files_handled = 0
        # will hold date of last modification from stat / http header
        self.last_modified = None
    
    def sitemap(self, sitemapurl, callback_parse=None, callback_stats=None):
        """process datadumps from a sitemap.xml as per http://XXX"""
        logger.debug("processing sitemap %s" % sitemapurl)
        datadumps = util.format.parse_sitemap(sitemapurl)
        
        if callback_parse is None:
            callback_parse = self.callback_parse
        if callback_stats is None:
            callback_stats = self.callback_stats
        
        for datadump in datadumps:
            self.next_file(datadump)
            self.parse(callback_parse)
            self.do_stats(callback_stats)
    
    def get_compression(self):
        """guess compression of resource"""
        logger.debug("get_compression()")
        compression_format = 'tar' if self.is_tar() else None
        compression_format = 'zip' if self.is_zip() else None
        compression_format = 'gz' if self.is_gzip() else None
        compression_format = 'bz2' if self.is_bzip2() else None
        return compression_format

            #elif self.is_gzip():
                #self.lowerurl = self.lowerurl[:-len('.gz')]
                #self.compression_format = 'gz'
            #elif self.is_bzip2():
                #self.lowerurl = self.lowerurl[:-len('.bz2')]
                #self.compression_format = 'bz2'
    
    def get_format(self):
        logger.debug("get_format()")
        if self.format is None:
            self.format = util.format.get_format(self.url.lower())

    def get_parser(self):
        self.parser = util.format.get_parser(self.url.lower(), self.format)
    
    def is_remote(self):
        return any(self.url.lower().startswith(x) for x in ('http://', 'https://'))

    def is_tar(self):
        return any(self.url.lower().endswith(x) for x in ('.tgz', '.tar.gz', '.tar.bz2'))

    def is_zip(self):
        return self.url.lower().endswith('.zip')

    def is_gzip(self):
        return self.url.lower().endswith('.gz')

    def is_bzip2(self):
        return self.url.lower().endswith('.bz2')

    def get_freespace(self, p):
        """
            Returns the number of free bytes on the drive that p is on
        """
        s = os.statvfs(p)
        return s.f_bsize * s.f_bavail

    def parse(self, callback_function = None, if_modified_since = None):
        """parse to redland::Stream"""
        logger.debug("parsing url %s, format %s" % (self.url, self.format))

        self.measure_execution_time_start()
        self.callback_parse = callback_function
        self.tempurl = self.url #changes if file is archive

        if self.format == 'sparql':
            return
        if self.format == 'sitemap':
            return

        # check if modified since last visit, 
        # TODO: really use http if-modified-since, etags
        last_modified = None
        if self.is_remote():
            r = requests.get(self.url)

            last_modified = r.headers.get('last-modified')
            if last_modified is not None:
                self.last_modified = datetime.datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
                if if_modified_since is not None and last_modified == if_modified_since:
                        raise exceptions.NotModified, 'resource has not been modified'

            content_length = r.headers.get('Content-Length')
            if content_length is not None:
                self.content_length = int(content_length)

            tempfile = tempfile.NamedTemporaryFile(prefix='lodstats')

            # do not download files bigger than freespace
            freespace = self.get_freespace(tempfile.tempdir)
            if self.content_length > freespace:
                raise Exception, "file too large (> free space)"

            if callback_function is not None:
                callback_function(self)

            #Download file
            for data in r:
                self.bytes_download += len(data)
                tempfile.write(data)
                self.ratelimited_callback_caller(callback_function)
            tempfile.seek(0)

            if self.compression_format is not None:
                if self.compression_format == 'gz':
                    gz_temp_decomp = gzip.GzipFile(fileobj=tempfile, mode='rb')
                    for data in gz_temp_decomp:
                        self.bytes += len(data)

                        tempfile.write(data)
                        self.ratelimited_callback_caller(callback_function)
                    gz_temp_decomp.close()
                elif self.compression_format == 'bz2':
                    decompressor = bz2.BZ2Decompressor()
                    for data in tempfile:
                        decompressed_data = decompressor.decompress(data)

                        self.bytes_download += len(data)
                        self.bytes += len(decompressed_data)

                        tempfile.write(decompressed_data)
                        self.ratelimited_callback_caller(callback_function)
                elif self.compression_format == 'tar':
                    self.archive = tarfile.open(fileobj=tempfile, mode='r')
                    self.file_entries = self.archive.getmembers()
                elif self.compression_format == 'zip':
                    self.archive = zipfile.ZipFile(tempfile, 'r')
                    self.file_entries = self.archive.infolist()
                tempfile.flush()
                self.tempurl = "file://%s" % tempfile.name
                # call back one last time to push final numbers
                if callback_function is not None:
                    callback_function(self)
            tempfile.close()
        self.parse_tempurl()
    
    def parse_tempurl(self):
        logger.debug("parse_tempurl()")
        self.get_format()
        self.get_parser()
        if self.format == 'sparql':
            return
        if self.format == 'sitemap':
            return
        self.stream = self.parser.parse_as_stream(self.tempurl)

    def warn_handler(self, message, category, filename, lineno, file=None, line=None):
        self.warnings += 1
        self.last_warning = message
    
    def do_stats(self, callback_function = None):
        """do the real work"""
        logger.debug("do_stats()")
        self.callback_stats = callback_function
        if self.compression_format in ('tar', 'zip'):
            self.do_archive_stats(callback_function)
        if self.format == 'sitemap':
            self.sitemap(self.url)
            return
        if self.format != 'sparql':
            with warnings.catch_warnings():
                warnings.showwarning = self.warn_handler
                for statement in self.stream:
                    # count statements
                    self.no_of_statements += 1
            
                    # do custom counting
                    self.do_custom_stats(statement)
                
                    # optional callback (eg for status stuff) every 5000 triples
                    if callback_function != None and self.no_of_statements % 5000 == 0:
                        callback_function(self)
        else:
            self.do_sparql_stats()
        
        # post-processing
        custom_stats.postproc()
        
        self.measure_execution_time_stop()

        if self.no_of_statements == 0:
            raise Exception, "zero triples"
    
    def do_archive_stats(self, callback_function):
        """do stats for archives"""
        logger.debug("do_archive_stats()")
        if self.compression_format == 'tar':
            for tar_entry in self.file_entries:
                if tar_entry.isfile():
                    # skip files with unknown extensions unless format is known
                    if self.format is None and not any(tar_entry.name.lower().endswith(x) for x in self.rdf_extensions):
                        continue
                    supplied_format = self.format
                    tar_content = self.archive.extractfile(tar_entry)
                    tempfile = tempfile.NamedTemporaryFile(prefix='lodstats_tar_entry')
                    for data in tar_content:
                         self.bytes += len(data)
                         tempfile.write(data)
                         self.ratelimited_callback_caller(callback_function)
                    # guess format later if necessary
                    if self.format is None:
                        self.lowerurl = tar_entry.name.lower()
                    # parse and to stats
                    tempfile.flush()
                    self.compression_format = None
                    self.tempurl = "file://%s" % tempfile.name
                    self.parse_tempurl()
                    self.do_stats(callback_function)
                    tempfile.close()
                    self.compression_format = 'tar'
                    self.format = supplied_format
                    self.files_handled += 1
            if self.files_handled == 0:
                raise Exception, "no RDF-ish files found in archive"
            # tar_tempfile.close()
            # tar_file.close()
        elif self.compression_format == 'zip':
            for zip_entry in self.file_entries:
                # do not handle directories at all
                if not zip_entry.filename.endswith(os.sep):
                    # skip files with unknown extensions unless format is known
                    if self.format is None and not any(zip_entry.filename.lower().endswith(x) for x in self.rdf_extensions):
                        continue
                    supplied_format = self.format
                    zip_content = self.archive.open(zip_entry)
                    tempfile = tempfile.NamedTemporaryFile(prefix='lodstats_zip_entry')
                    for data in zip_content:
                        self.bytes += len(data)
                        tempfile.write(data)
                        self.ratelimited_callback_caller(callback_function)
                    # guess format later if necessary
                    if self.format is None:
                        self.lowerurl = zip_entry.filename.lower()
                    # parse and to stats
                    tempfile.flush()
                    self.compression_format = None
                    self.tempurl = "file://%s" % tempfile.name
                    self.parse_tempurl()
                    self.do_stats(callback_function)
                    tempfile.close()
                    self.compression_format = 'zip'
                    self.format = supplied_format
                    self.files_handled += 1
            if self.files_handled == 0:
                raise Exception, "no RDF-ish files found in archive"
            # zip_tempfile.close()
            # zip_file.close()
        else:
            raise Exception, "unknown archive - this should not happen"
    
    def do_sparql_stats(self):
        """do stats via SPARQL"""
        logger.debug("do_sparql_stats()")
        from SPARQLWrapper import SPARQLWrapper, JSON
        sparql = SPARQLWrapper(self.url)
        sparql.setQuery("SELECT (count(*) AS ?triples) WHERE { ?s ?p ?o }")
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if not isinstance(results, dict):
            raise Exception, "unknown response content type"
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
    
    def ratelimited_callback_caller(self, callback_function):
        """helper for callbacks that should only fire every self.callback_delay seconds"""
        if callback_function is None:
            return
        now = datetime.datetime.now()
        if self.last_callback is None:
            self.last_callback = now
            callback_function(self)
        else:
            time_delta = (now-self.last_callback).seconds
            if time_delta >= self.callback_delay:
                callback_function(self)
                self.last_callback = now

    # accessors for statistics here
    
    def no_of_triples(self):
        """docstring for notriples"""
        return self.no_of_statements
    
    def no_of_namespaces(self):
        """docstring for noofnamespaces"""
        if self.format != 'sparql':
            return len(self.parser.namespaces_seen())

    def measure_execution_time_start(self):
        self.start_time = datetime.datetime.now()

    def measure_execution_time_stop(self):
        self.end_time = datetime.datetime.now()
        pass
    
    def voidify(self, serialize_as = "ntriples"):
        """present stats in VoID (http://www.w3.org/TR/void/)"""
        results = self.stats_results
        
        #Namespaces
        rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        void = "http://rdfs.org/ns/void#"
        void_ext = "http://stats.lod2.eu/rdf/void-ext/"
        qb = "http://purl.org/linked-data/cube#"
        dcterms = "http://purl.org/dc/terms/"
        ls_void = "http://stats.lod2.eu/rdf/void/"
        ls_qb = "http://stats.lod2.eu/rdf/qb/"
        ls_cr = "http://stats.lod2.eu/rdf/qb/criteria/"
        xsd = "http://www.w3.org/2001/XMLSchema#"
        stats = "http://example.org/XStats#"

        # setup serializar
        serializer = RDF.Serializer(name=serialize_as)
        serializer.set_namespace("rdf", rdf)
        serializer.set_namespace("void", void)
        serializer.set_namespace("void-ext", void_ext)
        serializer.set_namespace("qb", qb)
        serializer.set_namespace("dcterms", dcterms)
        serializer.set_namespace("ls-void", ls_void)
        serializer.set_namespace("ls-qb", ls_qb)
        serializer.set_namespace("ls-cr", ls_cr)
        serializer.set_namespace("xsd", xsd)
        serializer.set_namespace("xstats", stats)

        #Define namespaces with Redland
        ns_rdf = RDF.NS(rdf)
        ns_void = RDF.NS(void)
        ns_void_ext = RDF.NS(void_ext)
        ns_qb = RDF.NS(qb)
        ns_dcterms = RDF.NS(dcterms)
        ns_ls_void = RDF.NS(ls_void)
        ns_ls_qb = RDF.NS(ls_qb)
        ns_ls_cr = RDF.NS(ls_cr)
        ns_xsd = RDF.NS(xsd)
        ns_stats = RDF.NS(stats)

        # FIXME?: our dataset
        dataset_ns = RDF.NS("%s#" % self.url)

        void_model = RDF.Model()

        #Defining the Dataset
        source_uri = self.url
        dataset_uri = ls_void + "?source=" + source_uri
        dataset_entity = RDF.Uri(dataset_uri)
        source_entity = RDF.Uri(source_uri)

        void_model.append(RDF.Statement(dataset_entity,ns_rdf.type,ns_void.Dataset))
        void_model.append(RDF.Statement(dataset_entity,ns_dcterms.source,source_entity))
        #void-ext:observation ls-qb:hash1; ...hash2 etc.

        #Statistics from the stat
        number_of_triples_node = RDF.Node(literal=str(self.no_of_statements), datatype=ns_xsd.integer.uri)
        void_model.append(RDF.Statement(dataset_entity, ns_void.triples, number_of_triples_node))
        
        # voidify results from custom stats
        for stat in custom_stats.stats_to_do:
            stat.voidify(void_model, dataset_entity)

        # qb dataset
        lodstats_qb_dataset_label = "LODStats DataCube Dataset"
        lodstats_qb_dataset_label_node = RDF.Node(literal=lodstats_qb_dataset_label, datatype=ns_xsd.string.uri) 
        void_model.append(RDF.Statement(ns_ls_qb.LODStats, ns_rdf.type, ns_qb.Dataset))
        void_model.append(RDF.Statement(ns_ls_qb.LODStats, ns_qb.structure, ns_ls_qb.LODStatsStructure))
        void_model.append(RDF.Statement(ns_ls_qb.LODStats, ns_rdf.label, lodstats_qb_dataset_label_node))

        #qb datastructure
        lodstats_qb_dsd_label = "LODStats DataCube Structure Definition"
        lodstats_qb_dsd_label_node = RDF.Node(literal=lodstats_qb_dsd_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_rdf.type, ns_qb.DataStructureDefinition))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.timeOfMeasureSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.sourceDatasetSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.statisticalCriterionSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.valueSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, ns_ls_qb.unitSpec))
        void_model.append(RDF.Statement(ns_ls_qb.LODStatsStructure, ns_qb.component, lodstats_qb_dsd_label_node))

        #qb components
        timeOfMeasureSpec_label = "Time of Measure (Component Specification)"
        timeOfMeasureSpec_label_node = RDF.Node(literal=timeOfMeasureSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasureSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasureSpec, ns_qb.dimension, ns_ls_qb.timeOfMeasure))
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasureSpec, ns_rdf.label, timeOfMeasureSpec_label_node))

        sourceDatasetSpec_label = "Source Dataset which is observerd (Component Specification)"
        sourceDatasetSpec_label_node = RDF.Node(literal=sourceDatasetSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.sourceDatasetSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.sourceDatasetSpec, ns_qb.dimension, ns_ls_qb.sourceDataset))
        void_model.append(RDF.Statement(ns_ls_qb.sourceDatasetSpec, ns_rdf.label, sourceDatasetSpec_label_node))

        statisticalCriterionSpec_label = "Statistical Criterion (Component Specification)"
        statisticalCriterionSpec_label_node = RDF.Node(literal=statisticalCriterionSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterionSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterionSpec, ns_qb.dimension, ns_ls_qb.statisticalCriterion))
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterionSpec, ns_rdf.label, statisticalCriterionSpec_label_node))

        valueSpec_label = "Measure of Observation (Component Specification)"
        valueSpec_label_node = RDF.Node(literal=valueSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.valueSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.valueSpec, ns_qb.measure, ns_ls_qb.value))
        void_model.append(RDF.Statement(ns_ls_qb.valueSpec, ns_rdf.label, valueSpec_label_node))

        unitSpec_label = "Unit of Measure (Component Specification)"
        unitSpec_label_node = RDF.Node(literal=unitSpec_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.unitSpec, ns_rdf.type, ns_qb.ComponentSpecification))
        void_model.append(RDF.Statement(ns_ls_qb.unitSpec, ns_qb.attribute, ns_ls_qb.unit))
        void_model.append(RDF.Statement(ns_ls_qb.unitSpec, ns_rdf.label, unitSpec_label_node))

        # dimention properties
        timeOfMeasure_label = "Time of Measure"
        timeOfMeasure_label_node = RDF.Node(literal=timeOfMeasure_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasure, ns_rdf.type, ns_qb.DimensionProperty))
        void_model.append(RDF.Statement(ns_ls_qb.timeOfMeasure, ns_rdf.label, timeOfMeasure_label_node))

        sourceDataset_label = "Source Dataset"
        sourceDataset_label_node = RDF.Node(literal=sourceDataset_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.sourceDataset, ns_rdf.type, ns_qb.DimensionProperty))
        void_model.append(RDF.Statement(ns_ls_qb.sourceDataset, ns_rdf.label, sourceDataset_label_node))

        statisticalCriterion_label = "Statistical Criterion"
        statisticalCriterion_label_node = RDF.Node(literal=statisticalCriterion_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterion, ns_rdf.type, ns_qb.DimensionProperty))
        void_model.append(RDF.Statement(ns_ls_qb.statisticalCriterion, ns_rdf.label, statisticalCriterion_label_node))

        value_label = "Measure of Observation"
        value_label_node = RDF.Node(literal=value_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.value, ns_rdf.type, ns_qb.MeasureProperty))
        void_model.append(RDF.Statement(ns_ls_qb.value, ns_rdf.label, value_label_node))

        unit_label = "Unit of Measure"
        unit_label_node = RDF.Node(literal=unit_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.unit, ns_rdf.type, ns_qb.AttributeProperty))
        void_model.append(RDF.Statement(ns_ls_qb.unit, ns_rdf.label, unit_label_node))

        StatisticalCriterion_label = "Statistical Criterion"
        StatisticalCriterion_label_node = RDF.Node(literal=StatisticalCriterion_label, datatype=ns_xsd.string.uri)
        void_model.append(RDF.Statement(ns_ls_qb.StatisticalCriterion, ns_rdf.type, ns_qb.AttributeProperty))
        void_model.append(RDF.Statement(ns_ls_qb.StatisticalCriterion, ns_rdf.label, StatisticalCriterion_label_node))

        # voidify results from custom stats
        #for stat in custom_stats.stats_to_do:
            #stat.qbify(void_model, dataset_entity)

        # void:observation extension stuff
        #void_model.append(RDF.Statement(ns_stats.value, ns_rdf.type, ns_qb.MeasureProperty))
        #void_model.append(RDF.Statement(ns_stats.subjectsOfType, ns_rdf.type, ns_qb.DimensonProperty))
        #void_model.append(RDF.Statement(ns_stats.schema, ns_rdf.type, ns_qb.AttributeProperty))
        
        #serializer.set_namespace("thisdataset", dataset_ns._prefix)
        return serializer.serialize_model_to_string(void_model)

