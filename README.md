# thumbor_dash
A thumbor server extension for DASH
# Usage

Add to thumbor server config file

```python
from thumbor.handler_lists import BUILTIN_HANDLERS


HANDLER_LISTS = BUILTIN_HANDLERS + [
    "thumbor_dash.handler_lists.dashauth"
]

DASHAUTH_ROUTE = '/dashauth'

URL_SIGNER = 'thumbor_dash.url_signers.base64_hmac_sha1'

# Set allowed thumbnail size
MIN_WIDTH = 1 
MIN_HEIGHT = 1
MAX_WIDTH = 1200
MAX_HEIGHT = 800
```
