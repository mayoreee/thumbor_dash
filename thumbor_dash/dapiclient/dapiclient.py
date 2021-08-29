from dapiclient.client import DAPIClient
import cbor2
from thumbor_dash.error_handlers.sentry import ErrorHandler
from thumbor_dash.error_handlers import *

client = DAPIClient()


def getDocuments(handler, data):
    error_handler = ErrorHandler(handler.context.config)

    try:
        identity = client.getIdentity(data['owner_id'])

    except Exception as e:
        error_handler.handle_error(handler.context, handler, UnknownUserError)
        return

    else:
        docs = client.getDocuments(
            data['contract_id'],
            data['document_type'],
            data['where'],
            limit=2, # Only one document
            )

        documents = []
    
        for  doc in docs:
           documents.append(cbor2.loads(doc))
    
        return documents[0] # Return the only document in the list



