"""Encrypted URLs for thumbor encryption."""

import base64

from libthumbor.crypto import CryptoURL
from six import PY3, b, text_type
from thumbor_dash.url import plain_image_url, unsafe_url

class ThumborDashCryptoURL(CryptoURL):
     """Class responsible for generating encrypted URLs for thumbor"""

     def generate_new(self, options):
        url = plain_image_url(**options)
        _hmac = self.hmac.copy()
        _hmac.update(text_type(url).encode("utf-8"))
        signature = base64.urlsafe_b64encode(_hmac.digest())

        if PY3:
            signature = signature.decode("ascii")
        return "/%s/%s" % (signature, url)

     def generate(self, **options):
         """Generates an encrypted URL with the specified options"""
         if options.get("unsafe", False):
             return unsafe_url(**options)
         return self.generate_new(options)