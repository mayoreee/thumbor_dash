
class LoaderResult:

    ERROR_NOT_FOUND = "404 (not found): the image requested does not exist"
    ERROR_UPSTREAM = "upstream"
    ERROR_TIMEOUT = "timeout"

    def __init__(self, buffer=None, successful=True, error=None, metadata=None):
        """
        :param buffer: The media buffer

        :param successful: True when the media has been loaded.
        :type successful: bool

        :param error: Error code
        :type error: str

        :param metadata: Dictionary of metadata about the buffer
        :type metadata: dict
        """

        if metadata is None:
            metadata = {}

        self.buffer = buffer
        self.successful = successful
        self.error = error
        self.metadata = metadata
