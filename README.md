# thumbor_dash
A thumbor server extension for DASH


## Setup

#### Requirements

- Python >= 3.9
- Pip >= 21.1
- Thumbor == 7.0.0a5

See the requirements for setting up `thumbor` in the [documentation](https://thumbor.readthedocs.io/en/latest/installing.html)

#### 1. Install thumbor_dash

`pip install thumbor_dash`

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
MN_LIST =  '34.219.81.129,34.221.42.205,34.208.88.128,54.189.162.193,34.220.124.90,54.201.242.241,54.68.10.46,34.210.81.39,18.237.47.243'

```

## Usage

#### 1. Start thumbor_dash server

   `thumbor_dash --conf=thumbor.conf`

#### 2. Sign image URL

   ```python

   thumbor_dash-url --key="<Requester Identity Key>" --width=<width> --height=<height> --dashauth="requester(<requesterId>):contract(<contractId>):document(<documentType>):field(<avatarUrl>):owner(<ownerId>):updatedAt(<updatedAt>)" --filters="<filters>" <imageURL>

   ```

`output:`

   ```python

   /<signature>/<width>x<height>/dashauth:requester(<requesterId>):contract(<contractId>):document(<documentType>):field(<field>):owner(<ownerId>):updatedAt(<updatedAt>)/filters:format(<format>)/<encodedImageUrl>

   ```

#### 3. Thumbor_dash image retrieval URL

   ```python
   http://<thumbor_dash-server>/<signature>/<width>x<height>/dashauth:requester(<requesterId>):contract(<contractId>):document(<documentType>):field(<field>):owner(<ownerId>):updatedAt(<updatedAt>)/filters:format(<format>)/<encodedImageUrl>
   
   ```

   Note: If running the server locally, `<thumbor_dash-server>` should be `localhost:8888`


## Example

 This is a signed `thumbor_dash url`. Simply run `thumbor_dash` and paste this link in your browser.

   ```python
   
http://localhost:8888/U6lnOyBbSbRmZoxIgj81unAoR-V2GhJj1lAAQ0846Nw=/1200x800/dashauth:requester(856aSH6uEBaHpndZYXDk72NJbZqXokNSPGrs8nKbd7QL):contract(DbBHu3Ct1zD1AYAiw58V7QXT22B3k7qRLDLfaXqiRQp5):document(thumbnailField):field(avatarUrl):owner(856aSH6uEBaHpndZYXDk72NJbZqXokNSPGrs8nKbd7QL):updatedAt(1654864287788)/filters:format(jpeg)/https%3A//github.com/thumbor/thumbor/raw/master/example.jpg


   
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
MN_LIST=34.219.81.129,34.221.42.205,34.208.88.128,54.189.162.193,34.220.124.90,54.201.242.241,54.68.10.46,34.210.81.39,18.237.47.243

```

#### 2. Start thumbor_dash server in Docker

   `docker run -p 80:80 --env-file thumbor.env.txt mayoreee/thumbor_dash`
When your environment is not ARM-based, add the option `--platform linux/arm64/v8`

Note: If running in Docker, `<thumbor_dash-server>` in the image request URL should be set to `localhost:80` instead of `localhost:8888`.
   



