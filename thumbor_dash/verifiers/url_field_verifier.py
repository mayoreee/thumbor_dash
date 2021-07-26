
def verifyURLField(doc, field):
    ''' Checks whether the url is in the right field'''
    print("Thumbor DASH STATUS: Verifying url field........" )
    if doc['field'] == field :
        return True
        print("Thumbor DASH STATUS: Successfully verified url field........" )
    else:
        print("Thumbor DASH STATUS: Error verifying url field........" )
        return False