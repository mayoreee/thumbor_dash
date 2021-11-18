from urllib.parse import quote, unquote
from thumbor_dash.error_handlers import *
from thumbor_dash.context import ThumborDashRequestParameters
from thumbor_dash.verifiers import access_status_verifier, url_field_verifier, image_size_verifier, thumbnail_size_verifier
from thumbor_dash.dapiclient import dapiclient
from thumbor_dash.utils import dashauthParametersToJson
from thumbor.handlers.imaging import ImagingHandler
from thumbor_dash.error_handlers.sentry import ErrorHandler

import base58
import base64
import cbor2
import random
import os


class ThumborDashImagingHandler(ImagingHandler):

    async def check_image(self, kwargs):
        config = self.context.config # thumbor config
        error_handler = ErrorHandler(config)
       
        MN_IP = None
        SEED_IP=config.get("SEED_IP")   
        MN_LIST=config.get("MN_LIST")
        

        if ((config.get("SEED_IP") is None)  or (os.getenv("SEED_IP") is None)) or (MN_LIST is not None):   
             CONVERTED_MN_LIST = str(config.get("MN_LIST")).split(",")              
             MN_IP = random.choice(CONVERTED_MN_LIST) 
        

        if self.context.config.MAX_ID_LENGTH > 0:
            # Check if an image with an uuid exists in storage
            exists = await self.context.modules.storage.exists(
                kwargs["image"][: self.context.config.MAX_ID_LENGTH]
            )
            if exists:
                kwargs["image"] = kwargs["image"][: self.context.config.MAX_ID_LENGTH]

        url = self.request.path

        kwargs["image"] = quote(kwargs["image"].encode("utf-8"))
        if not self.validate(kwargs["image"]):
            error_handler.handle_error(self.context, self, UnspecifiedImageError)
            return

        kwargs["request"] = self.request
        self.context.request = ThumborDashRequestParameters(**kwargs)
        request = self.context.request # HTTP request


        has_none = not self.context.request.unsafe and not self.context.request.hash
        has_both = self.context.request.unsafe and self.context.request.hash

        if has_none or has_both:
            error_handler.handle_error(self.context, self, UnsignedURLError)
            return

        if self.context.request.unsafe and not self.context.config.ALLOW_UNSAFE_URL:
            error_handler.handle_error(self.context, self, UnsafeURLError)
            return

        if self.context.config.USE_BLACKLIST:
            blacklist = await self.get_blacklist_contents()
            if self.context.request.image_url in blacklist:
                error_handler.handle_error(self.context, self, BlacklistedSourceError)
                return

        url_signature = self.context.request.hash

        identity_key = None
        try:
             # Identity key retrieval from DAPI
             requesterId = base58.b58decode(dashauthParametersToJson(request.dashauth)["requester"])
             identity =  dapiclient.getIdentity(self, requesterId, seed_ip=SEED_IP, mn_ip=MN_IP)
             identity_key = (base64.b64encode(identity['publicKeys'][0]['data'])).decode('utf-8')
        except Exception as e:
             return
        else:
             if url_signature:
                 # Verify signature using identity key
                 signer = self.context.modules.url_signer(identity_key) 

                 try:
                     quoted_hash = quote(self.context.request.hash)
                 except KeyError:
                     error_handler.handle_error(self.context, self, ForbiddenSignatureError)
                     return

                 url_to_validate = url.replace(
                "/%s/" % self.context.request.hash, ""
            ).replace("/%s/" % quoted_hash, "")

                 valid = signer.validate(unquote(url_signature).encode(), url_to_validate)

                 if not valid and self.context.config.STORES_CRYPTO_KEY_FOR_EACH_IMAGE:
                     # Retrieves security key for this image if it has been seen before
                     security_key = await self.context.modules.storage.get_crypto(
                    self.context.request.image_url
                )
                     if security_key is not None:
                         signer = self.context.modules.url_signer(security_key)
                         valid = signer.validate(url_signature.encode(), url_to_validate)

                 if not valid:
                     error_handler.handle_error(self.context, self, ForbiddenSignatureError)
                     return


        # <--------------------- Dash Platform Request Verification  ------------------------->
        
      
             body = dashauthParametersToJson(request.dashauth) 
        
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
             checkAccessStatus = await access_status_verifier.verifyUserAccessStatus(requesterId, config)

             if checkAccessStatus:
                 # DAPI thumbnail document request input data
                 data = {
                 'contract_id': base58.b58decode(contractId),
                 'owner_id': base58.b58decode(ownerId),
                 'document_type': documentType,
                 'where': cbor2.dumps([
                     ['ownerId', '==', base58.b58decode(ownerId)],
                     ['$updatedAt', '==', updatedAt],
                     ]),
                }  

                 try:
                     # Query DAPI for thumbnail document data
                     thumbnail_document = dapiclient.getDocuments(self, data, seed_ip=SEED_IP, mn_ip=MN_IP)


                 except Exception as e:
                     error_handler.handle_error(self.context, self, DashPlatformError)
                     return
                 else:
                     #Request verification
                     MIN_RESIZE_WIDTH = thumbnail_document["resizeValues"][0]
                     MIN_RESIZE_HEIGHT = thumbnail_document["resizeValues"][1]
                     MAX_RESIZE_WIDTH = thumbnail_document["resizeValues"][2]
                     MAX_RESIZE_HEIGHT = thumbnail_document["resizeValues"][3]
                
                     checkURLField = url_field_verifier.verifyURLField(thumbnail_document, field) # Verify url field
                     checkThumbnailSize = thumbnail_size_verifier.verifyThumbnailSize(thumbnail_width, thumbnail_height, MIN_RESIZE_WIDTH, MIN_RESIZE_HEIGHT, MAX_RESIZE_WIDTH, MAX_RESIZE_HEIGHT) # Verify requested thumbnail size
                     checkImageSize = image_size_verifier.verifyImageSize(thumbnail_width, thumbnail_height, MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT) # Verify image size
      
                     if (checkURLField and checkThumbnailSize and checkImageSize) == False:
                         error_handler.handle_error(self.context, self, BadRequestError)
                         return
             else:
                 error_handler.handle_error(self.context, self, TooManyRequestsError)
                 return
       
             return await self.execute_image_operations()        
        