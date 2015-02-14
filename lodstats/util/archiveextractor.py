import tempfile
import gzip
import bz2
import tarfile
import zipfile
import os

import logging
logger = logging.getLogger("lodstats")

import lodstats.util
import lodstats.config
from lodstats.util.interfaces import CallbackInterface
from lodstats.util.interfaces import UriParserInterface

class ArchiveExtractor(CallbackInterface, UriParserInterface):
    def __init__(self, uri, callback_function=None, remote_file=None, rdf_format=None):
        super(ArchiveExtractor, self).__init__()
        self.uri = uri
        self.rdf_format = rdf_format
        self.remote_file = remote_file
        self.original_file_size = 0
        if(self.remote_file is not None):
            self.original_file_size = remote_file.get_bytes_downloaded()
        self.filename = self.identify_filename(uri)
        self.filepath = uri[7:] #omitting file://
        self.compression_format = self.identify_compression_format(self.uri)

        self.bytes_extracted = 0 # was self.bytes

        self.extracted_file_uri_list = self.extract_archive(uri, self.filepath, self.compression_format, callback_function)
        self.extracted_file_path_list = self.set_extracted_file_path(self.extracted_file_uri_list)

        logger.debug("File is extracted to %s" % self.extracted_file_path_list)

    def get_compression_format(self):
        if(self.compression_format is None):
            return "None"
        return self.compression_format

    def get_filepath(self):
        return self.filepath

    def get_uri(self):
        return self.uri

    def get_extracted_file_path_list(self):
        return self.extracted_file_path_list

    def get_extracted_file_uri_list(self):
        return self.extracted_file_uri_list

    def print_extracted_file_uri_list(self):
        output = ''
        for uri in self.extracted_file_uri_list:
            output += uri + "\n"
        return output

    def print_extracted_file_path_list(self):
        output = ''
        for name in self.extracted_file_path_list:
            output += name + "\n"
        return output

    def set_extracted_file_path(self, extracted_file_uri_list):
        result = []
        for uri in extracted_file_uri_list:
            result.append(uri[7:])
        return result

    def get_info(self):
        output = "file uri: "+self.get_uri() + "\n"
        output += "file path: "+self.get_filepath() + "\n"
        output += "compression format: "+self.get_compression_format() +"\n"
        output += "extracted file uri: "+self.print_extracted_file_uri_list()+"\n"
        output += "extracted file name: "+self.print_extracted_file_path_list()+"\n"
        return output

    def extract_archive(self, uri, filepath, compression_format, callback_function):

        if self.rdf_format == "sparql" or self.rdf_format == "sitemap":
            return [uri]

        f = open(filepath, 'rU')
        if compression_format is None:
            extracted_file_uri = [uri]
        elif compression_format == 'gz':
            extracted_file_uri = self.decompress_gzip(filepath, callback_function)
        elif compression_format == 'bz2':
            extracted_file_uri = self.decompress_bz2(filepath, callback_function)
        elif compression_format == 'tar':
            extracted_file_uri = self.decompress_tar(filepath, callback_function)
        elif compression_format == 'zip':
            extracted_file_uri = self.decompress_zip(filepath, callback_function)
        f.close()
        # call back one last time to push final numbers
        if callback_function is not None:
            callback_function(self)

        logging.debug("File %s has been successfully extracted to %s" % (filepath, extracted_file_uri))
        #return an array of uris
        return extracted_file_uri

    def get_filesize(self, path_to_file):
        return os.path.getsize(path_to_file)

    def decompress_gzip(self, input_file, callback_function):
        output_file = tempfile.NamedTemporaryFile(prefix='lodstats_gzip_decompressed', suffix=self.filename, delete=False)
        gzip_file = gzip.GzipFile(input_file, mode='rb')
        try:
            for data in gzip_file:
                self.bytes_extracted += len(data)
                output_file.write(data)
                self.ratelimited_callback_caller(callback_function)
        except IOError as e:
            logger.error(str(e))
        output_file.flush()
        output_file.close()
        gzip_file.close()

        result_uri = ["file://%s" % output_file.name]
        if(self.get_filesize(output_file.name) < self.get_filesize(self.filepath)):
            result_uri = self.uri


        return result_uri

    def decompress_bz2(self, input_file, callback_function):
        output_file = tempfile.NamedTemporaryFile(prefix='lodstats_bzip2_decompressed', suffix=self.filename, delete=False)
        bz2_file = bz2.BZ2File(input_file)
        for data in bz2_file:
            self.bytes_extracted += len(data)
            output_file.write(data)
            self.ratelimited_callback_caller(callback_function)
        output_file.flush()
        output_file.close()
        bz2_file.close()

        return ["file://%s" % output_file.name]

    def decompress_tar(self, input_file, callback_function):
        archive = tarfile.open(input_file, 'r')
        extracted_uri_list = []
        #process file by file
        for tar_entry in archive.getmembers():
            if tar_entry.isfile():
                # skip files with unknown extensions unless format is known
                if not any(tar_entry.name.lower().endswith(x) for x in lodstats.util.rdf_extensions):
                    continue

                tar_content = archive.extractfile(tar_entry)
                output_file = tempfile.NamedTemporaryFile(prefix='lodstats_tar_entry', suffix=self.filename, delete=False)
                for data in tar_content:
                    self.bytes_extracted += len(data)
                    output_file.write(data)
                    self.ratelimited_callback_caller(callback_function)
                output_file.flush()
                #self.parse_tempurl()
                #self.do_stats(callback_function)
                output_file.close()
                extracted_uri_list.append("file://%s" % output_file.name)
        return extracted_uri_list

    def decompress_zip(self, input_file, callback_function):
        import os
        extracted_uri_list = []
        archive = zipfile.ZipFile(input_file, 'r')
        for zip_entry in archive.infolist():
            # do not handle directories at all
            if not zip_entry.filename.endswith(os.sep):
                # skip files with unknown extensions unless format is known
                if not any(zip_entry.filename.lower().endswith(x) for x in lodstats.util.rdf_extensions):
                    continue

                zip_content = archive.open(zip_entry)
                output_file = tempfile.NamedTemporaryFile(prefix='lodstats_zip_entry', suffix=self.filename, delete=False)
                for data in zip_content:
                    self.bytes_extracted += len(data)
                    output_file.write(data)
                    self.ratelimited_callback_caller(callback_function)
                output_file.flush()
                output_file.close()
                extracted_uri_list.append("file://%s" % output_file.name)
        return extracted_uri_list
