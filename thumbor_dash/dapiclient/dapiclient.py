from dapiclient.client import DAPIClient
from thumbor_dash.error_handlers.sentry import ErrorHandler
from thumbor_dash.error_handlers import *
from thumbor_dash.dapiclient.decode import * 

import cbor2
import base58
import base64
import binascii
import struct


def getAvatarUrl(handler, data, seed_ip=None, mn_ip=None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip=mn_ip)
    error_handler = ErrorHandler(handler.context.config)

    try:
        docs = client.getDocuments(
            data_contract_id=data['contract_id'],
            document_type=data['document_type'],
            where=data['where'],
            limit=2,  # Only one document
            prove=False
        )
        doc = docs.documents[0]
        decoded_doc = decode_doc_byte_string(doc) 

    except Exception as e:
        print(e)
        error_handler.handle_error(handler.context, handler, DashPlatformError)
        return
    else:
        return decoded_doc


def getIdentity(handler, ownerId, seed_ip=None, mn_ip=None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip=mn_ip)
    error_handler = ErrorHandler(handler.context.config)

    try:
        identity = client.getIdentity(id=ownerId, prove=False)
    except Exception as e:
        error_handler.handle_error(handler.context, handler, DashPlatformError)
        return

    else:
        return identity  # Return the identity


def getIdentityKey(handler, ownerId, seed_ip=None, mn_ip=None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip=mn_ip)
    error_handler = ErrorHandler(handler.context.config)

    try:
        identity_keys = client.getIdentityKeys(id=ownerId, prove=False)
        identity_key = decode_byte_string(identity_keys[0])
    except Exception as e:
        error_handler.handle_error(handler.context, handler, DashPlatformError)
        return

    else:
        return identity_key['data']  # Return the identity_key
