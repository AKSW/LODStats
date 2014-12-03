import tempfile
import os
import requests
import exceptions
import datetime
import uuid

import logging
logger = logging.getLogger("lodstats")

import lodstats.config
from lodstats.util.interfaces import CallbackInterface
from lodstats.util.interfaces import UriParserInterface

class RemoteFile(CallbackInterface, UriParserInterface):
    def __init__(self, uri, if_modified_since=None, callback_function=None, rdf_format=None):
        super(RemoteFile, self).__init__()
        self.uri = uri
        self.filename = self.identify_filename(self.uri)
        self.if_modified_since = if_modified_since
        self.callback_function = callback_function
        self.last_modified = None
        self.rdf_format = rdf_format
        self.content_length = 0
        self.bytes_downloaded = 0

    def get_bytes_downloaded(self):
        return self.bytes_downloaded

    def set_last_modified(self, last_modified):
        self.last_modified = last_modified

    def get_last_modified(self):
        return self.last_modified

    def set_content_length(self, content_length):
        self.content_length = content_length

    def get_content_length(self):
        return self.content_length

    def get_downloaded_file_uri(self):
        if(self.is_remote()):
            downloaded_file_uri = self.download()
            return downloaded_file_uri
        else:
            logging.debug("File is local, returning original URI")
            return self.uri

    def get_free_diskspace(self, p):
        """
            Returns the number of free bytes on the drive that p is on
        """
        s = os.statvfs(p)
        return s.f_bsize * s.f_bavail

    def get_local_free_diskspace(self):
        return self.get_free_diskspace(tempfile.gettempdir())

    def generate_uuid_for_filename(self, filename=None):
        if(filename is None):
            filename = self.filename

        namespace = uuid.NAMESPACE_URL
        unique_id = str(uuid.uuid5(namespace, filename)) + self.get_file_extension()

        return unique_id

    def download(self):

        if(self.rdf_format == "sparql" or self.rdf_format == "sitemap"):
            return self.uri

	try:
	    r = requests.get(self.uri, stream=True, timeout=5)
        except requests.exceptions.Timeout as e:
            raise e

        last_modified = r.headers.get('last-modified')
        if last_modified is not None:
            last_modified = datetime.datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
            if self.if_modified_since is not None and last_modified == self.if_modified_since:
                raise exceptions.NotModified, 'resource has not been modified'

        content_length = r.headers.get('content-length', 0)
        if content_length is not 0:
            self.set_content_length(int(content_length))

        free_diskspace = self.get_local_free_diskspace()
        if self.content_length > free_diskspace:
            raise Exception, "file too large (> free space)"

        if self.callback_function is not None:
            self.callback_function(self)

	#Check if file is accessible

        #Download file
        output_file = tempfile.NamedTemporaryFile(prefix='lodstats',
                                                  suffix=self.generate_uuid_for_filename(),
                                                  delete=False)
        #chunk_size = "16"
        for data in r.iter_content(chunk_size=512):
            self.bytes_downloaded += len(data)
            output_file.write(data)
            self.ratelimited_callback_caller(self.callback_function)

        if(self.callback_function is not None):
            self.callback_function(self)

        logger.debug("File is downloaded to %s" % output_file.name)

        return "file://%s" % output_file.name

if __name__ == "__main__":
    uri = "https://premium.scraperwiki.com/dtuaora/91bafd103a364fc/http/__status.csv"
    uri = "http://uccaribe.eagle-i.net/sparqler/sparql?view=published-resources&format=text/turtle&query=PREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E+PREFIX+%3A+%3Chttp%3A%2F%2Feagle-i.org%2Font%2Frepo%2F1.0%2F%3E+construct+%7B%3Fs+%3Fp+%3Fo+.+%3Fs+a+%3Ftype+.+%3Ftype+rdfs%3Alabel+%3Ftype_label+.+%3Fp+rdfs%3Alabel+%3Fp_label+.+%3Fo+rdfs%3Alabel+%3Fo_label%7D+where+%7Bgraph+%3ANG_Published%7B%3Fs+%3Fp+%3Fo%7D+.+optional%7B%3Fs+a+%3Ftype%7D+.+optional%7B%3Ftype+rdfs%3Alabel+%3Ftype_label%7D+.+optional%7B%3Fp+rdfs%3Alabel+%3Fp_label+%7D+.+optional%7B+%3Fo+rdfs%3Alabel+%3Fo_label%7D%7D+"
    uri = "http://mlode.nlp2rdf.org/datasets/semanticquran.ttl.gz"
    uri = "http://prelex.publicdata.eu/model/export/?m=http%3A%2F%2Fprelex.publicdata.eu%2F&f=rdfxml"
    remote_file = RemoteFile(uri, callback_function=lodstats.config.callback_function_download)
    #remote_file.download()
    print remote_file.get_downloaded_file_uri()
