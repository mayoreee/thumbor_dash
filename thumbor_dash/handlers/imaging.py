from urllib.parse import quote, unquote
from thumbor_dash.error_handlers import *
from thumbor_dash.context import ThumborDashRequestParameters
from thumbor_dash.verifiers import access_status_verifier, url_field_verifier, image_size_verifier, thumbnail_size_verifier
from thumbor_dash.dapiclient import dapiclient
from thumbor_dash.utils import dashauthParametersToJson
from thumbor_dash.utils import normalize_url
from thumbor.handlers.imaging import ImagingHandler
from thumbor_dash.error_handlers.sentry import ErrorHandler
import base58
import base64
import cbor2
import json
import random
import os


class ThumborDashImagingHandler(ImagingHandler):

    async def check_image(self, kwargs):
        config = self.context.config # thumbor config
        error_handler = ErrorHandler(config)
       
        MN_IP = None
        SEED_IP = None
         
        if config.get("MN_LIST") is not None:      
             MN_LIST = str(config.get("MN_LIST")).split(",")              
             MN_IP = random.choice(MN_LIST) 
        elif config.get("SEED_IP") is not None:
            SEED_IP=config.get("SEED_IP")
        else:
             if os.getenv("MN_LIST") is not None:
                 MN_LIST = str(os.getenv("MN_LIST")).split(",")              
                 MN_IP = random.choice(MN_LIST) 
             else:
                 SEED_IP=os.getenv("SEED_IP")   
        

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
             identity_key = dapiclient.getIdentityKey(self, requesterId, seed_ip=SEED_IP, mn_ip=MN_IP)
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

             if 1>0:
                 # DAPI thumbnail document request input data
                 data = {
                 'contract_id': base58.b58decode(contractId),
                 'document_type': documentType,
                 'where': cbor2.dumps([
                     ['$ownerId', '==', base58.b58decode(ownerId)]
                     ]),
                }  

                 try:
                     # Query DAPI for avatar url
                     avatar_url = dapiclient.getAvatarUrl(self, data, seed_ip=SEED_IP, mn_ip=MN_IP)
                     isAvatarUrlMatching = normalize_url(avatar_url) == normalize_url(request.image_url)
                     
                 except Exception as e:
                     print(e)
                     error_handler.handle_error(self.context, self, DashPlatformError)
                     return
                 else:

                     if (request.width < MIN_WIDTH or request.width > MAX_WIDTH or request.height < MIN_HEIGHT or request.height > MAX_HEIGHT) or (isAvatarUrlMatching == False):
                         error_handler.handle_error(self.context, self, BadRequestError)
                         return
             else:
                 error_handler.handle_error(self.context, self, TooManyRequestsError)
                 return
       
             return await self.execute_image_operations()        
        