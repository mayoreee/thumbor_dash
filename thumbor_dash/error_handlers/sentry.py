from thumbor_dash.error_handlers import *


class ErrorHandler:
    '''Custom error handler for thumbor_dash'''

    def __init__(self, config):
        self.config = config
        self.BAN_DURATION = config.BAN_DURATION #Ban duration in minutes


    def handle_error(self, context, handler, exception):
        # context is thumbor_dash's context for the current request
        # handler is tornado's request handler for the current request
        # exception is the error that occurred

        # Custom error messages for thumbor_dash server
        self.ERROR_MESSAGES = {
        BadRequestError: "400 (bad request): the syntax was not respected",
        UnsignedURLError: "400 (unsigned request): URL does not have hash or unsafe, or has both",
        UnsafeURLError: "400 (unsafe request) URL has unsafe but unsafe is not allowed by the config",
        UnspecifiedImageError: "400 (unspecified image) No original image was specified in the given URL",
        BlacklistedSourceError: "400 (blacklisted source) Source image url has been blacklisted",
        UnknownUserError: "401 (unauthorized): the user does not exist",
        PaymentError: "402 (payment required): in phase 2 only -> not enough funds on identity",
        ForbiddenSignatureError: "403 (forbidden): the signature is incorrect",
        NotFoundError: "404 (not found): the image requested does not exist",
        MethodNotAllowedError: "405 (method not allowed): a method other than GET or HEAD was sent for the resource",
        UnsupportedMediaTypeError: "415 (unsupported media type): client should not request again",
        TooManyRequestsError: "429 (too many requests): client should stop making requests for a {} min period".format(self.BAN_DURATION),
        DashPlatformError: "503 (Dash Platform Service Error): Dash platform service is not available. Please retry later",
        }
        
        exception_code_switcher = {
        BadRequestError: 400,
        UnsignedURLError: 400,
        UnsafeURLError: 400,
        UnspecifiedImageError: 400,
        BlacklistedSourceError: 400,
        UnknownUserError: 401,
        PaymentError: 402,
        ForbiddenSignatureError: 403,
        NotFoundError: 404,
        MethodNotAllowedError: 405,
        UnsupportedMediaTypeError: 415,
        TooManyRequestsError: 429,
        DashPlatformError: 503
        }

        error_status_code = exception_code_switcher.get(exception, BadRequestError)

        handler.clear()
        handler.set_status(error_status_code)
        handler.finish("<html><body>{}</body></html>".format(self.ERROR_MESSAGES[exception])
        )

