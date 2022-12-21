from django.conf import settings
import os

def get_ipfs_url(path):
    if settings.DEBUG:
        return os.path.join('http://localhost:5001', path)

    host = os.environ.get('IPFS_HOST', 'http://ipfs:5001')
    return os.path.join(host, path)
