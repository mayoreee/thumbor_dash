from dapiclient.client import DAPIClient
from thumbor_dash.error_handlers.sentry import ErrorHandler
from thumbor_dash.error_handlers import *

import cbor2
import base58



def getDocuments(handler, data, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)
    error_handler = ErrorHandler(handler.context.config)
    
    try:
        docs = client.getDocuments(
             data['contract_id'],
             data['document_type'],
             data['where'],
             limit=2, # Only one document
        )
    except Exception as e:
        error_handler.handle_error(handler.context, handler, DashPlatformError)
        return 
    else:
        return docs[0]# Return the only document in the list


def getIdentity(handler, ownerId, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)
    error_handler = ErrorHandler(handler.context.config)

    try:
        identity = client.getIdentity(ownerId)
    except Exception as e:
        error_handler.handle_error(handler.context, handler, DashPlatformError)
        return

    else:   
        return identity # Return the identity


