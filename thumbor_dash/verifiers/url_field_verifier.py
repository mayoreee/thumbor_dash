
def verifyURLField(doc, field):
    ''' Checks whether the url is in the right field'''
    if doc['field'] == field :
        return True
    else:
        return False