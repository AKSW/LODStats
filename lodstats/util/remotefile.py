import tempfile
import os
import requests
import exceptions
import datetime
import logging

import lodstats.config
from lodstats.util.interfaces import CallbackInterface
from lodstats.util.interfaces import UriParserInterface

class RemoteFile(CallbackInterface, UriParserInterface):
    def __init__(self, uri, if_modified_since=None, callback_function=None):
        super(RemoteFile, self).__init__()
        self.uri = uri
        self.filename = self.identify_filename(self.uri)
        self.if_modified_since = if_modified_since
        self.callback_function = callback_function
        self.last_modified = None
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
        if(self._is_remote()):
            downloaded_file_uri = self.download()
            return downloaded_file_uri
        else:
            logging.debug("File is local, returning original URI")
            return self.uri

    def _is_remote(self):
        return any(self.uri.lower().startswith(x) for x in ('http://', 'https://'))

    def get_free_diskspace(self, p):
        """
            Returns the number of free bytes on the drive that p is on
        """
        s = os.statvfs(p)
        return s.f_bsize * s.f_bavail

    def get_local_free_diskspace(self):
        return self.get_free_diskspace(tempfile.gettempdir())

    def download(self):
        r = requests.get(self.uri)

        last_modified = r.headers.get('last-modified')
        if last_modified is not None:
            last_modified = datetime.datetime.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z')
            if self.if_modified_since is not None and last_modified == self.if_modified_since:
                raise exceptions.NotModified, 'resource has not been modified'

        content_length = r.headers['content-length']
        if content_length is not None:
            self.set_content_length(int(content_length))

        free_diskspace = self.get_local_free_diskspace()
        if self.content_length > free_diskspace:
            raise Exception, "file too large (> free space)"

        if self.callback_function is not None:
            self.callback_function(self)

        #Download file
        output_file = tempfile.NamedTemporaryFile(prefix='lodstats', suffix=self.filename, delete=False)
        for data in r.content:
            self.bytes_downloaded += len(data)
            output_file.write(data)
            self.ratelimited_callback_caller(self.callback_function)

        if(self.callback_function is not None):
            self.callback_function(self)

        return "file://%s" % output_file.name

if __name__ == "__main__":
    uri = "https://premium.scraperwiki.com/dtuaora/91bafd103a364fc/http/__status.csv"
    remote_file = RemoteFile(uri, callback_function=lodstats.config.callback_function_download)
    print remote_file.get_downloaded_file_uri()
