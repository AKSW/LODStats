virtenv_path = '/home/ivan/.virtualenvs/lodstats/src/LODStats/test/resources/'

rdf_test_file_uri = 'file://' + virtenv_path + 'heb-original.rdf'
rdf_test_file_uri_head = 'file://' + virtenv_path + 'heb-head-original.nt'
rdf_test_file_uri_tail = 'file://' + virtenv_path + 'heb-tail-original.nt'
rdf_test_file_name = virtenv_path + 'heb-original.rdf'
rdf_test_file_name_head = virtenv_path + 'heb-head-original.nt'
rdf_test_file_name_head_ttl = virtenv_path + 'heb-head-original.ttl'
rdf_test_file_name_tail = virtenv_path + 'heb-tail-original.nt'

def callback_function_archive_extraction(object):
    print(object.bytes_extracted)

def callback_function_download(object):
    print(object.bytes_downloaded)

def callback_function_statistics(object):
    print(object.get_no_of_triples())

def callback_function_conversion(object):
    print(object.bytes_converted)

import logging
logging.basicConfig(format = '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                level = logging.DEBUG)

def enable_debug():
    logging.disable(logging.NOTSET)

def disable_debug():
    logging.disable(logging.CRITICAL)
