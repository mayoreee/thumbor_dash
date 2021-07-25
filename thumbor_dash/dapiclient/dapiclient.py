from dapiclient.client import DAPIClient
import cbor2

client = DAPIClient()


def getDocuments(data):
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



