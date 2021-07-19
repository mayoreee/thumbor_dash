from thumbor_dash.verifiers import url_field_verifier, image_size_verifier, access_status_verifier, thumbnail_size_verifier
from thumbor.handlers import BaseHandler
from tornado.escape import json_decode
from thumbor_dash.dapiclient import dapiclient 
import base58
import cbor2

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

        # Verify user access status
        checkAccessStatus = access_status_verifier.verifyUserAccessStatus(requesterId)


        if checkAccessStatus:

             # DAPI thumbnail document request input data
             data = {
                 'contract_id': base58.b58decode(contractId),
                 'document_type': documentType,
                 'where': cbor2.dumps([
                     ['$ownerId', '==', base58.b58decode(ownerId)],
                     ['$updatedAt', '==', updatedAt],
                     ]),
                }  
             # Query DAPI for thubmnail document data
             thumbnail_document = dapiclient.get_documents(data)

             #Request verification
             checkURLField = url_field_verifier.verifyURLField(thumbnail_document, field) # Verify url field
             checkThumbnailSize = thumbnail_size_verifier.verifyThumbnailSize(thumbnail_width, thumbnail_height, MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT) # Verify requested thumbnail size
             checkImageSize = image_size_verifier.verifyImageSize() #TODO: #TODO: Remove this check permanently. Since Thumbor does this check by default, this verification is only redundant.
      
        
             if checkURLField & checkThumbnailSize & checkImageSize:
                 super().prepare()
             else:
                 #TODO: Handle custom errors as regards bad/unallowed request types
                 super().prepare() #remove this when custom errors are available

        else:
             #TODO: Handle custom errors as regards user moderation
                 super().prepare() #remove this when custom errors are available




         