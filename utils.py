import re
from urllib.parse import urlparse, urlunparse


def url_to_filename(url):
    # Remove the protocol (http:// or https://)
    url_without_protocol = re.sub(r'^https?://', '', url)

    # Replace non-alphanumeric characters with underscores
    safe_filename = re.sub(r'[^A-Za-z0-9]+', '_', url_without_protocol)

    # Truncate the filename if it's too long (e.g., for very long URLs)
    max_filename_length = 255  # Adjust as needed
    if len(safe_filename) > max_filename_length:
        safe_filename = safe_filename[:max_filename_length]

    return safe_filename


def normalize_url(url):
    parsed_url = urlparse(url)

    if not parsed_url.scheme or parsed_url.scheme is not 'https':
        scheme = 'https'
    else:
        scheme = parsed_url.scheme
    normalized_url = urlunparse((scheme, parsed_url.netloc, parsed_url.path,
                                 parsed_url.params, parsed_url.query, parsed_url.fragment))
    return str(normalized_url).replace('www.', '')


def sample_list(original_list, rate):
    import random

    # Calculate the number of elements to sample (10% of the list)
    sample_size = int(len(original_list) * rate)

    return random.sample(original_list, sample_size)
