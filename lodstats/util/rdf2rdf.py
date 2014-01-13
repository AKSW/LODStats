import subprocess
import tempfile
import os

import lodstats.config

from lodstats.util.interfaces import UriParserInterface
from lodstats.util.interfaces import CallbackInterface

import logging

logger = logging.getLogger("lodstats")

class RDF2RDF(CallbackInterface, UriParserInterface):
    def __init__(self, uri, callback_function=None):
        super(RDF2RDF, self).__init__()
        self.uri = uri
        self.filename = self.identify_filename(self.uri)
        self.bytes_converted = 0
        self.callback_function = callback_function
        self.rdf2rdf_path = ""
        if(self.is_remote()):
            logger.error("Can not process URI, is remote: %s" % self.uri)

    def convert_n3_to_nt(self, uri=None):
        pass

    def convert_ttl_to_nt(self, uri=None):
        if(uri is None):
            uri = self.uri

        input_file_path = uri[7:]
        output_file_path = input_file_path+".nt"

        command = "any23 rover -e rdf-turtle -f ntriples -o %s %s" % (output_file_path, input_file_path)
	print command

        pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = pipe.stdout, pipe.stderr

        for data in stderr:
            logger.debug(str(data))

        for data in stdout:
            logger.debug(str(data))

        return "file://%s" % output_file_path

if __name__ == "__main__":
    #traces conversion process
    callback_function = lodstats.config.callback_function_conversion
    virtenv_path = lodstats.config.virtenv_path

    file_uri = 'file://'+virtenv_path+'heb-head-original.ttl'

    rdf2rdf = RDF2RDF(file_uri, callback_function=callback_function)
    print rdf2rdf.convert_ttl_to_nt(file_uri)
