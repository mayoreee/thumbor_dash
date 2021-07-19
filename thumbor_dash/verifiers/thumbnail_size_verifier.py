''' Check whether the requested thumbnail size is within allowed bounds'''
def verifyThumbnailSize(thumbnail_width, thumbnail_height, MIN_WIDTH, MIN_HEIGHT, MAX_WIDTH, MAX_HEIGHT):
    if thumbnail_width >= MIN_WIDTH & thumbnail_width <= MAX_WIDTH & thumbnail_height >= MIN_HEIGHT & thumbnail_height <= MAX_HEIGHT:
        return True
    else:
        return False 