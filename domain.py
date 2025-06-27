from urllib.parse import urlparse

# This module provides functions to extract domain and subdomain names from URLs
# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        if get_sub_domain_name(url).find('.br') == -1:
            return results[-2] + '.' + results[-1]
        else:
            return results[-3] + '.' + results[-2] + '.' + results[-1]
    except:
        return ''

# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''