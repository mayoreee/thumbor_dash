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
        'contract_id': base58.b58decode('4sTfrKQfPCvutR7XG4Hgj3vMB22VP86RthcMnicwgGLu'),
        'document_type': 'documents',
        'where': cbor2.dumps([
            ['$ownerId', '==', base58.b58decode('HWnTMizyGZbbEFrMvPPEJa3JoGyb5TCMiGEEZaom9Dbq')],
            ['$updatedAt', '==', 1626652853407],
        ]),
    }
    result = getDocuments(data)    
    print(result)
    
   
if __name__ == "__main__":
    main()


