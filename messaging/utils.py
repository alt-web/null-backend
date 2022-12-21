from django.conf import settings
import os
import urllib.parse

def get_ipfs_url(path):
    if settings.DEBUG:
        return urllib.parse.urljoin('http://localhost:5001', path)

    host = os.environ.get('IPFS_HOST', 'http://ipfs:5001')
    return urllib.parse.urljoin(host, path)
