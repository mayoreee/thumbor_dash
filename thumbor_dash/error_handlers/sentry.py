from thumbor_dash.error_handlers import BadRequestError, UnauthorizedUserError, PaymentError, ForbiddenSignatureError, NotFoundError, MethodNotAllowedError, UnsupportedMediaTypeError, TooManyRequestsError


class ErrorHandler:
    '''Custom error handler for thumbor_dash'''

    def __init__(self, config):
        self.config = config
        self.BAN_DURATION = config.BAN_DURATION #Ban duration in minutes
        
        # Custom error messages for thumbor_dash server
        self.ERROR_MESSAGES = {
        400: "401 (bad request): the syntax was not respected",
        401: "401 (unauthorized): the user does not exist",
        402: "402 (payment required): in phase 2 only -> not enough funds on identity",
        403: "403 (forbidden): the signature is incorrect",
        404: "404 (not found): the image requested does not exist",
        405: "405 (method not allowed): a method other than GET or HEAD was sent for the resource",
        415: "415 (unsupported media type): client should not request again",
        429: "429 (too many requests): client should stop making requests for a {} min period".format(self.BAN_DURATION),
        }


    def handle_error(self, context, handler, exception):
        # context is thumbor_dash's context for the current request
        # handler is tornado's request handler for the current request
        # exception is the error that occurred
        
        exception_switcher = {
        BadRequestError: 400,
        UnauthorizedUserError: 401,
        PaymentError: 402,
        ForbiddenSignatureError: 403,
        NotFoundError: 404,
        MethodNotAllowedError: 405,
        UnsupportedMediaTypeError: 415,
        TooManyRequestsError: 429
        }

        error_status_code = exception_switcher.get(exception, BadRequestError)

        handler.clear()
        handler.set_status(error_status_code)
        handler.finish("<html><body>{}</body></html>".format(self.ERROR_MESSAGES[error_status_code])
        )

