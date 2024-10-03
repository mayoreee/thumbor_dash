from datetime import datetime
from urllib.parse import unquote, urlparse, urlunparse
import re

def dashauthParametersToJson(params):
    temp = re.split(r':(?![//\d])', params)
    result = {}
   
    for p in temp:
        key_value_pair = p.split("(")
        key = key_value_pair[0]

        temp_value = key_value_pair[1]
        value = temp_value[0:- 1]
        real_value = int(value) if key == "updatedAt" else value

        result[key] = real_value
    
    return result


def datetimeToMillisecondsSinceEpoch(dt):
    epoch = datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds() * 1000.0


def normalize_url(url):
    # Decode percent-encoded characters
    decoded_url = unquote(url)
    
    # Parse the URL into components
    parsed_url = urlparse(decoded_url)
    
    # Normalize scheme and netloc (lowercase)
    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc.lower()
    
    # Remove trailing slashes
    path = parsed_url.path.rstrip('/')
    
    # Reconstruct the URL without query parameters and fragments for a simpler comparison
    normalized_url = urlunparse((scheme, netloc, path, '', '', ''))
    
    return normalized_url