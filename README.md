# thumbor_dash
A thumbor server extension for DASH


# Usage

#### Requirements
- Python >= 3.9
- Thumbor >= 7.0.0
- pip >= 21.1

#### 1. Install thumbor_dash
`pip install thumbor_dash`

#### 2. Create a configuration file
  `thumbor-config > thumbor.conf`

#### 3. Add to `thumbor.conf` file

```python

import thumbor_dash
from thumbor.handler_lists import BUILTIN_HANDLERS


HANDLER_LISTS = BUILTIN_HANDLERS + [
    'thumbor_dash.handler_lists.dashauth'
]

DASHAUTH_ROUTE = '/dashauth'

URL_SIGNER = 'thumbor_dash.url_signers.base64_hmac_sha1'

ALLOW_UNSAFE_URL = False 

# Set allowed thumbnail size
MIN_WIDTH = 1 
MIN_HEIGHT = 1
MAX_WIDTH = 1200
MAX_HEIGHT = 800
```

#### 4. Run thumbor server with the configuration file
  `thumbor --conf=thumbor.conf`