import datetime
import urllib.parse

import logging

logger = logging.getLogger("lodstats")

class CallbackInterface(object):
    def __init__(self):
        #TODO: move to config file
        self.callback_delay = 2
        self.time_of_last_callback = None

    def ratelimited_callback_caller(self, callback_function):
        """helper for callbacks that should only fire every self.callback_delay seconds"""
        if callback_function is None:
            return
        now = datetime.datetime.now()
        if self.time_of_last_callback is None:
            self.time_of_last_callback = now
            callback_function(self)
        else:
            time_delta = (now-self.time_of_last_callback).seconds
            if time_delta >= self.callback_delay:
                callback_function(self)
                self.time_of_last_callback = now

class UriParserInterface(object):
    def __init__(self):
        pass

    def is_remote(self):
        return any(self.uri.lower().startswith(x) for x in ('http://', 'https://'))

    def identify_rdf_format(self, uri):
        rdf_format = None
        rdf_format = self.identify_rdf_format_by_file_extension(uri)

        if(rdf_format is None):
            raise NameError("could not guess format")
        else:
            return rdf_format

    def identify_rdf_format_by_file_extension(self, uri):
        logger.debug("UriParser.get_format: %s" % uri)
        process_uri = uri.split('/')[-1]
        process_uri = process_uri.split('.')

        for item in process_uri:
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
        return None

    def identify_rdf_format_by_magic(self, uri):
        return None

    def identify_compression_format(self, uri):
        """guess compression of resource"""
        logger.debug("UriParser.get_compression: %s" % uri)
        compression_format = None
        if self._has_tar_extension(uri):
            compression_format = 'tar'
        if self._has_zip_extension(uri):
            compression_format = 'zip'
        if self._has_gzip_extension(uri):
            compression_format = 'gz'
        if self._has_bzip2_extension(uri):
            compression_format = 'bz2'
        return compression_format

    def _has_tar_extension(self, uri):
        return any(uri.lower().endswith(x) for x in ('.tgz', '.tar.gz', '.tar.bz2', '.tar'))

    def _has_zip_extension(self, uri):
        return uri.lower().endswith('.zip')

    def _has_gzip_extension(self, uri):
        return uri.lower().endswith('.gz')

    def _has_bzip2_extension(self, uri):
        return uri.lower().endswith('.bz2')

    def identify_filename(self, uri):
        return uri.split('/')[-1]

    def has_scheme(self, uri):
        scheme = self.get_scheme(uri)
        if(scheme is ''):
            return False
        else:
            return True

    def get_scheme(self, uri):
        parsed_uri = urllib.parse.urlparse(uri)
        return parsed_uri.scheme

    def fix_uri(self, uri):
        scheme = self.get_scheme(uri)
        if scheme == "http" or scheme == "https":
            return uri
        elif scheme == "":
            import os
            abs_path = os.path.abspath(uri)
            return "file://%s"%abs_path
        elif scheme == "file":
            return uri

    def get_file_extension(self, filename=None):
        if(filename is None):
            filename = self.filename

        extension = ""
        extension_outer = None
        extension_inner = None
        try:
            extension_outer = filename.split(".")[-1]
            extension_inner = filename.split(".")[-2]
        except IndexError as e:
            logging.error("Could not determine extension %s" % (str(e),))
            return extension

        if(extension_outer is not None and len(extension_outer) < 6):
            extension = extension + "." + extension_inner

        if(extension_inner is not None and len(extension_inner) < 6):
            extension = extension + "." + extension_outer

        extension_question_mark = extension.split("?")
        if(len(extension_question_mark) > 1):
            extension = extension_question_mark[0]

        return extension
