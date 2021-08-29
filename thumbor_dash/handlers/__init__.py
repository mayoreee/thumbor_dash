
from thumbor.handlers import ImageApiHandler
from thumbor.engines import BaseEngine
from thumbor_dash.error_handlers import *
from thumbor_dash.error_handlers.sentry import ErrorHandler

##
# Base handler for Image API operations
##
class ThumborDashImageApiHandler(ImageApiHandler):

    def validate(self, body):
        error_handler = ErrorHandler(self.context.config)

        conf = self.context.config
        mime = BaseEngine.get_mimetype(body)

        if mime == "image/gif" and self.context.config.USE_GIFSICLE_ENGINE:
            engine = self.context.modules.gif_engine
        else:
            engine = self.context.modules.engine

        # Check if image is valid
        try:
            engine.load(body, None)
        except IOError:
            error_handler.handle_error(self.context, self, UnsupportedMediaTypeError)
            return False

        # Check weight constraints
        if conf.UPLOAD_MAX_SIZE != 0 and len(self.request.body) > conf.UPLOAD_MAX_SIZE:
            self._error(
                412,
                "Image exceed max weight (Expected : %s, Actual : %s)"
                % (conf.UPLOAD_MAX_SIZE, len(self.request.body)),
            )
            return False

        # Check size constraints
        size = engine.size
        if conf.MIN_WIDTH > size[0] or conf.MIN_HEIGHT > size[1]:
            self._error(
                412,
                "Image is too small (Expected: %s/%s , Actual : %s/%s) % "
                "(conf.MIN_WIDTH, conf.MIN_HEIGHT, size[0], size[1])",
            )
            return False
        return True