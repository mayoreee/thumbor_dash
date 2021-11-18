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
        identity = client.getIdentity(ownerId)
    except Exception as e:
        return e
    else:   
        return identity # Return the only document in the list




def main():

# Test getIdentity
    ownerId = base58.b58decode("G75gKVaN7BAz8GhKp9qk18o9Mf2JgCpRxLtzYGNs68Wa")
    identity = getIdentity(None,ownerId=ownerId,seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)
    print(str(identity))

# Test getDocuments
    data = {
        'contract_id': base58.b58decode('HPvdCZ3sr2ACdSW6VeNVKKiYjUBnS4YkMv3sexzzTABJ'),
        'document_type': 'thumbnailField',
        'where': cbor2.dumps([
            ['ownerId', '==', base58.b58decode('G75gKVaN7BAz8GhKp9qk18o9Mf2JgCpRxLtzYGNs68Wa')],
            ['$updatedAt', '==', 1634748218973],
        ]),
    }
    docs = getDocuments(ErrorHandler,data,seed_ip='seed-1.testnet.networks.dash.org', mn_ip=None)    
    print(str(docs))


   
if __name__ == "__main__":
    main()




