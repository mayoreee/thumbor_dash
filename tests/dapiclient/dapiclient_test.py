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
        'contract_id': base58.b58decode('D6tjxCZzZobDQztc4S1PK7EDwm4CegLARpiKZn6jQc1R'),
        'document_type': 'thumbnailField',
        'where': cbor2.dumps([
            ['ownerId', '==', base58.b58decode('26AxVi5bvYYaC94GmeTmqX21vzsSxar2a4imxSE8ULUQ')],
            ['$updatedAt', '==', 1627948894242],
        ]),
    }
    result = getDocuments(data)    
    print(result)
    
   
if __name__ == "__main__":
    main()




