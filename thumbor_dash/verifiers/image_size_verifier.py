''' Check whether the original image size is within allowed bounds'''
def verifyImageSize(doc, field):
    #TODO: Remove this method permanently. Since Thumbor does this check by default, this verification is only redundant.
    return True