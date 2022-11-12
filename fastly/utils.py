import requests

from django.conf import settings


def purge_url(path):
    """
    Purge a Fastly.com URL given a path. path argument must begin with a slash
    """
    if settings.DEBUG:
        return

    if api_key := getattr(settings, 'FASTLY_API_KEY', None):
        return requests.request(
            'PURGE',
            f'https://www.python.org{path}',
            headers={'Fastly-Key': api_key},
        )

    return None
