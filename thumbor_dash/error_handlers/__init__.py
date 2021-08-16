
class Error(Exception):
    '''Base exception class'''
    pass

class BadRequestError(Error):
    '''The syntax was not respected'''
    pass

class UnauthorizedUserError(Error):
    '''The user does not exist'''
    pass

class PaymentError(Error):
    '''Not enough funds on identity'''
    pass

class ForbiddenSignatureError(Error):
    '''The signature is incorrect'''
    pass

class NotFoundError(Error):
    '''The image requested does not exist'''
    pass

class MethodNotAllowedError(Error):
    '''A method other than GET or HEAD was sent for the resource'''
    pass

class UnsupportedMediaTypeError(Error):
    '''The media type specified in the request is not supported'''
    pass

class TooManyRequestsError(Error):
    '''Client is temporarily banned'''
    pass
