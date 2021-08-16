
def verifyThumbnailSize(thumbnail_width, thumbnail_height, MIN_RESIZE_WIDTH, MIN_RESIZE_HEIGHT, MAX_RESIZE_WIDTH, MAX_RESIZE_HEIGHT):
    ''' Checks whether the requested thumbnail size is within allowed bounds'''
    if thumbnail_width >= MIN_RESIZE_WIDTH and thumbnail_width <= MAX_RESIZE_WIDTH and thumbnail_height >= MIN_RESIZE_HEIGHT and thumbnail_height <= MAX_RESIZE_HEIGHT:
        return True
    else:
        return False 