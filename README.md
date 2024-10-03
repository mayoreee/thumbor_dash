# thumbor_dash
A thumbor server extension for DASH


## Setup

#### Requirements

- Python <= 3.11
- Thumbor == 7.7.4

See the requirements for setting up `thumbor` in the [documentation](https://thumbor.readthedocs.io/en/latest/installing.html)

#### 1. Install thumbor_dash

```
git clone https://github.com/mayoreee/thumbor_dash.git && cd thumbor_dash
```

```
python3 -m pip install .
```

Note: thumbor_dash, thumbor, and other required dependencies will be installed

#### 2. Create a thumbor configuration file
  
`thumbor-config > thumbor.conf`

#### 3. Add these lines to `thumbor.conf` file

```python
# Set allowed dimensions
MIN_WIDTH = 1
MIN_HEIGHT = 1
MAX_WIDTH = 1200
MAX_HEIGHT = 800

# Use custom Url signing method (sha256)
URL_SIGNER = 'thumbor_dash.url_signers.base64_hmac_sha256'

# Allow only signed URL
ALLOW_UNSAFE_URL = False

# Set user moderation rules
REQUEST_TIME_LIMIT = 1 # time between requests in minutes
USAGE_VIOLATION_LIMIT = 5 # total number of times a requester can violate the time limit before ban
BAN_DURATION = 10 # requester ban duration in minutes

# Use custom error handling
USE_CUSTOM_ERROR_HANDLING = True
ERROR_HANDLER_MODULE = 'thumbor_dash.error_handlers.sentry'

# User-defined MN and IP list
SEED_IP = 'seed-1.testnet.networks.dash.org'
MN_LIST =  '35.165.50.126,52.10.229.11,54.149.33.167,52.24.124.162,54.187.14.232'

```

## Usage

#### 1. Start thumbor_dash server

   `thumbor_dash --conf=thumbor.conf`

#### 2. Sign image URL

   ```python

   thumbor_dash-url --key="<Requester Identity Key>" --width=<width> --height=<height> --dashauth="requester(<requesterId>):contract(<contractId>):document(thumbnail):field(avatarUrl):owner(<ownerId>):updatedAt(<updatedAt>)" --filters="<filters>" <imageURL>

   ```

`output:`

   ```python

   /<signature>/<width>x<height>/dashauth:requester(<requesterId>):contract(<contractId>):document(thumbnail):field(avatarUrl):owner(<ownerId>):updatedAt(<updatedAt>)/filters:format(<format>)/<encodedImageUrl>

   ```

#### 3. Thumbor_dash image retrieval URL

   ```python
   http://<thumbor_dash-server>/<signature>/<width>x<height>/dashauth:requester(<requesterId>):contract(<contractId>):document(thumbnail):field(avatarUrl):owner(<ownerId>):updatedAt(<updatedAt>)/filters:format(<format>)/<encodedImageUrl>
   
   ```


## Example

 This is a signed `thumbor_dash url`. Simply run `thumbor_dash` and paste this link in your browser.

   ```python
   
http://localhost:8888/wQ71tyl2OvFRVvHkrEWnbZp4dxE1E0fhaLcqbYgp8Uw=/1200x800/dashauth:requester(CbmEawiuxwJZPp3aJJkuM8Pw5CnMAkQvaQmTouLHcH2Q):contract(CubPbDcDPCi3HhbSNRQfkZDYU6R2yPsPveHrWoCKJr1P):document(thumbnail):field(avatarUrl):owner(CbmEawiuxwJZPp3aJJkuM8Pw5CnMAkQvaQmTouLHcH2Q):updatedAt(1727625029657)/filters:format(jpeg)/https%3A//raw.githubusercontent.com/thumbor/thumbor/master/example.jpg

   ```

# Running thumbor_dash in Docker

This is the fastest way to run `thumbor_dash`

#### 1. Create a `thumbor.env.txt` file containing the environment variables

```python

MIN_WIDTH=1
MIN_HEIGHT=1
MAX_WIDTH=1200
MAX_HEIGHT=800
REQUEST_TIME_LIMIT=1 
USAGE_VIOLATION_LIMIT=5
BAN_DURATION=10
USE_CUSTOM_ERROR_HANDLING=True
ALLOW_UNSAFE_URL=False
URL_SIGNER=thumbor_dash.url_signers.base64_hmac_sha256
ERROR_HANDLER_MODULE=thumbor_dash.error_handlers.sentry
SEED_IP=seed-1.testnet.networks.dash.org
MN_LIST=35.165.50.126,52.10.229.11,54.149.33.167,52.24.124.162,54.187.14.232

```

#### 2. Start thumbor_dash server in Docker

   `docker run -p 80:80 --env-file thumbor.env.txt mayoreee/thumbor_dash`

   



