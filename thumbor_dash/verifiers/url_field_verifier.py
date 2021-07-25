''' Check whether the url is in the right field'''
def verifyURLField(doc, field):
    if doc['field'] == field :
        return True
    else:
        return False