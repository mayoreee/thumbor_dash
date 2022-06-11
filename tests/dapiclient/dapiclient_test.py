from logging import Handler
from dapiclient.client import DAPIClient
import cbor2
import base58
from thumbor.handlers.imaging import ImagingHandler
from thumbor_dash.error_handlers.sentry import ErrorHandler
from thumbor_dash.error_handlers import *


def getDocuments(handler, data, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)

    try:
        docs = client.getDocuments(
             data['contract_id'],
             data['document_type'],
             data['where'],
             limit=2, # Only one document
        )
    except Exception as e:
        return e
    else:
        return docs[0]# Return the only document in the list


def getIdentity(handler, ownerId, seed_ip = None, mn_ip = None):
    client = DAPIClient(seed_ip=seed_ip, mn_ip = mn_ip)

    try:
        identity = client.getIdentity(id=ownerId, prove=False)
    except Exception as e:
        return e
    else:   
        return identity # Return the only document in the list




def main():

# Test getIdentity
    ownerId = base58.b58decode("856aSH6uEBaHpndZYXDk72NJbZqXokNSPGrs8nKbd7QL")
    identity = getIdentity(None,ownerId=ownerId,seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)
    print(str(identity))

# Test getDocuments
    data = {
        'contract_id': base58.b58decode('DbBHu3Ct1zD1AYAiw58V7QXT22B3k7qRLDLfaXqiRQp5'),
        'document_type': 'thumbnailField',
        'where': cbor2.dumps([
            ['ownerId', '==', base58.b58decode('856aSH6uEBaHpndZYXDk72NJbZqXokNSPGrs8nKbd7QL')],
            ['$updatedAt', '==', 1654864287788],
        ]),
    }
    docs = getDocuments(ErrorHandler,data,seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)    
    print(str(docs))


   
if __name__ == "__main__":
    main()




