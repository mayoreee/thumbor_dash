from thumbor_dash.verifiers.verifiers import verifyThumbnailSize, verifyURLField
from thumbor.handlers import BaseHandler
from tornado.escape import json_decode
from thumbor_dash.dapi import dapiclient 

class DashAuthHandler(BaseHandler):
    """Custom HTTP request handler class for ``dashauth``"""

    async def prepare(self):  
        request = self.context.request # HTTP request
        config = self.context.config # thumbor config
        body = json_decode(request.body)  # HTTP request body
        
        thumbnail_width = request.width # requested thumbnail width
        thumbnail_height = request.height # requested thumbnail height
        
        MIN_WIDTH = config.MIN_WIDTH  # minimum thumbnail width allowed
        MAX_WIDTH = config.MAX_WIDTH # maximum thumbnail width allowed
        MIN_HEIGHT = config.MIN_HEIGHT  # minimum thumbnail height allowed
        MAX_HEIGHT = config.MAX_HEIGHT # maximum thumbnail height allowed

        requesterId = body["requester"] # identity of whomever is making the request
        contractId = body["contract"] # the contract whose document holds the image URL
        documentType = body["document"] # the document whose instance holds the URL
        field = body["field"] # the field of the URL
        ownerId = body["owner"] # the owner of the document that is being requested
        updatedAt = body["updatedAt"] # the last time the document was updated

        # DAPI thumbnail document request input data
        data = {
            'contract_id': contractId,
            'document_type': documentType,
            'where': [
                ['$ownerId', '==', ownerId],
                ['updatedAt', '==', updatedAt]
            ]
        }


        #TODO: Fix DAPI client 
        thumbnail_document = dapiclient.get_documents(data)

        if verifyURLField(thumbnail_document, field) & verifyThumbnailSize(thumbnail_width, thumbnail_height, MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT):
           super().prepare()
        else:
            #TODO: Handle custom errors
            super().prepare() #remove this when custom errors are available




         