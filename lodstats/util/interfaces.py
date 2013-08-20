import datetime
import urlparse

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
    def __init__(self, uri):
        self.uri = uri

    def identify_rdf_format(self):
        uri = self.uri
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
        raise NameError("could not guess format")

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
        parsed_uri = urlparse.urlparse(uri)
        if(parsed_uri.scheme is ''):
            return False
        else:
            return True

    def fix_uri(self, uri):
        fixed_uri = uri
        if(self.has_scheme(uri)):
            return fixed_uri
        else:
            return "file://%s"%fixed_uri

