import hashlib
import json
import os
from datetime import datetime
from json import dumps, loads
from os.path import dirname, exists, getmtime, splitext
from shutil import move
from typing import ContextManager
from uuid import uuid4
from thumbor import storages

from thumbor.storages import BaseStorage
from thumbor.utils import logger
from thumbor_dash.request_storage import REQUEST_STORAGE_ROOT_PATH
from thumbor.context import Context



class RequestStorage(BaseStorage):
    
    async def put(self, requester_id, file_bytes):
        file_abs = self.path_on_filesystem(requester_id)
        temp_abspath = "%s.%s" % (file_abspath, str(uuid4()).replace("-", ""))
        file_dir_abspath = dirname(file_abspath)

        logger.debug("creating tempfile for %s in %s...", requester_id, temp_abspath)

        self.ensure_dir(file_dir_abspath)

        with open(temp_abspath, "wb") as _file:
            _file.write(file_bytes)

        logger.debug("moving tempfile %s to %s...", temp_abspath, file_abspath)
        move(temp_abspath, file_abspath)

        return requester_id   
    

    def path_on_filesystem(self, requester_id):
        digest = hashlib.sha1(requester_id.encode("utf-8")).hexdigest()
        return "%s/%s/%s" % (
            REQUEST_STORAGE_ROOT_PATH.rstrip("/"),
            digest[:2],
            digest[2:],
        )


    async def get(self, requester_id):
        abs_path = self.path_on_filesystem(requester_id)

        resource_available = await self.exists(requester_id, path_on_filesystem=abs_path)
        if not resource_available:
            return None

        with open(self.path_on_filesystem(requester_id), "rb") as source_file:
            return source_file.read()
    
# #Usage
# data = {"requesterId": "requesterId"}
# file_bytes = json.dumps(data).encode('utf-8')

# print(file_bytes)
# print(type(file_bytes))



