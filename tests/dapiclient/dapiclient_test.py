from dapiclient.client import DAPIClient
import cbor2
import base58


client = DAPIClient()

def getDocuments(data):
    docs = client.getDocuments(
        data['contract_id'],
        data['document_type'],
        data['where'],
        limit=2,
    )

    documents = []
    
    for  doc in docs:
        documents.append(cbor2.loads(doc))
    
    return documents[0] # Only one document


def main():
    data = {
        'contract_id': base58.b58decode('En3GRoMNAnt69firp32h3NEBxyveLcHQMUbwhDW2UqoX'),
        'document_type': 'thumbnailField',
        'where': cbor2.dumps([
            ['ownerId', '==', base58.b58decode('GCAFKUdw7PtUcDEG8j3sicMJ4ngx1aTqCdb4HD5n5WZ7')],
            ['$updatedAt', '==', 1627076771396],
        ]),
    }
    result = getDocuments(data)    
    print(result)
    
   
if __name__ == "__main__":
    main()




