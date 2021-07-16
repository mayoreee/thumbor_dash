import grpc

import rpc.grpc.platform_pb2 as platform_pb2
import rpc.grpc.platform_pb2_grpc as platform_pb2_grpc

import cbor2
import base64

GRPC_REQUEST_TIMEOUT = 10000

# Set up connection
channel = grpc.insecure_channel('seed-1.testnet.networks.dash.org:3010')
stub = platform_pb2_grpc.PlatformStub(channel)



def get_documents(contract_id, type, options):
    # Get Document
    contract_id_bytes = contract_id.encode('UTF-8')
    contract_id_base64 = base64.b64encode(contract_id_bytes)

    document_request = platform_pb2.GetDocumentsRequest()
    document_request.data_contract_id = contract_id_base64
    document_request.document_type = type
    document_request.limit = 2
    # document_request.where = # Requires cbor (found in dapi-client)
  
    docs = stub.getDocuments(document_request, GRPC_REQUEST_TIMEOUT)
    # print(docs)
    for d in docs.documents:
        print('Document cbor: {}\n'.format(cbor2.loads(d)))


def main():
    dpns_contract_id = 'ARQGUnPH3YMK8FZuqwUjnTWEF6Zu4Cf3sT6e1Ruu1RXk'
    get_documents(dpns_contract_id, 'note', 'limit = 2')
   
if __name__ == "__main__":
    main()




