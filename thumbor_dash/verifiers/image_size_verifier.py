
def verifyImageSize(thumbnail_width, thumbnail_height, MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT):
    ''' Checks whether the original image size is within allowed bounds'''
    if thumbnail_width >= MIN_WIDTH and thumbnail_width <= MAX_WIDTH and thumbnail_height >= MIN_HEIGHT and thumbnail_height <= MAX_HEIGHT:
        return True
    else:
        return False 