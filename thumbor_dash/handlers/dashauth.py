from thumbor.handlers import BaseHandler
from tornado.escape import json_decode
from thumbor_dash.dapi import dapiclient 

class DashAuthHandler(BaseHandler):
    """Custom HTTP request handler class for ``dashauth``"""

    async def prepare(self):  
        request = self.context.request # HTTP request
        config = self.context.config # thumbor config
        body = json_decode(request.body)  # HTTP request body
        
        imageWidth = request.width # requested thumbnail width
        imageHeight = request.height # requested thumbnail height
        
        MIN_WIDTH = config.MIN_WIDTH  # minimum thumbnail width allowed
        MAX_HEIGHT = config.MAX_HEIGHT # maximum thumbnail height allowed

        requesterId = body["requester"] # identity of whomever is making the request
        contractId = body["contract"] # the contract whose document holds the image URL
        documentType = body["document"] # the document whose instance holds the URL
        field = body["field"] # the field of the URL
        ownerId = body["owner"] # the owner of the document that is being requested
        updatedAt = body["updatedAt"] # the last time the document was updated


        #TODO: Fix DAPI query
        #result = dapiclient.get_documents()
        
        super().prepare()

        

        

