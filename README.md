# thumbor_dash
A thumbor server extension for DASH


# Usage

#### Requirements
- Python >= 3.9
- pip >= 21.1

#### 1. Clone the repo
`git clone https://github.com/mayoreee/thumbor_dash.git`

`cd thumbor_dash`

#### 2. Create a virtual environment
`python3 -m venv /path/to/new/virtual/environment`

Then, activate the virtual environment as described [here](https://docs.python.org/3/library/venv.html)

#### 3. Install thumbor_dash and its dependencies
  `pip install .    `

#### 4. Create a configuration file
  `thumbor-config > thumbor.conf`

#### 5. Add to `thumbor.conf` file

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

#### 6. Run thumbor server with the configuration file
  `thumbor --conf=thumbor.conf`
