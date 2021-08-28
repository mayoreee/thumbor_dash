import datetime

from thumbor.engines import BaseEngine
from thumbor_dash.handlers import ThumborDashImageApiHandler
from thumbor_dash.error_handlers import *
from thumbor_dash.error_handlers.sentry import ErrorHandler

##
# Handler to retrieve or modify existing images
# This handler support GET, PUT and DELETE method to manipulate existing images
##
class ThumborDashImageResourceHandler(ThumborDashImageApiHandler):
    async def check_resource(self, file_id):
        error_handler = ErrorHandler(self.context.config)

        file_id = file_id[: self.context.config.MAX_ID_LENGTH]
        # Check if image exists
        exists = await self.context.modules.storage.exists(file_id)

        if exists:
            body = await self.context.modules.storage.get(file_id)
            self.set_status(200)

            mime = BaseEngine.get_mimetype(body)
            if mime:
                self.set_header("Content-Type", mime)

            max_age = self.context.config.MAX_AGE
            if max_age:
                self.set_header("Cache-Control", "max-age=" + str(max_age) + ",public")
                self.set_header(
                    "Expires",
                    datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                )
            self.write(body)
            self.finish()
        else:
            error_handler.handle_error(self.context, self, NotFoundError)

    async def put(self, file_id):
        error_handler = ErrorHandler(self.context.config)

        file_id = file_id[: self.context.config.MAX_ID_LENGTH]
        # Check if image overwriting is allowed
        if not self.context.config.UPLOAD_PUT_ALLOWED:
            error_handler.handle_error(self.context, self, MethodNotAllowedError)
            return

        # Check if the image uploaded is valid
        if self.validate(self.request.body):
            await self.write_file(file_id, self.request.body)
            self.set_status(204)

    async def delete(self, file_id):
        error_handler = ErrorHandler(self.context.config)

        file_id = file_id[: self.context.config.MAX_ID_LENGTH]
        # Check if image deleting is allowed
        if not self.context.config.UPLOAD_DELETE_ALLOWED:
            error_handler.handle_error(self.context, self, MethodNotAllowedError)
            return

        # Check if image exists
        exists = await self.context.modules.storage.exists(file_id)
        if exists:
            await self.context.modules.storage.remove(file_id)
            self.set_status(204)
        else:
            error_handler.handle_error(self.context, self, NotFoundError)

    async def get(self, file_id):
        await self.check_resource(file_id)

    async def head(self, file_id):
        await self.check_resource(file_id)