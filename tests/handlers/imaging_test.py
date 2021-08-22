from thumbor import importer
from thumbor_dash.storages.request_storage import RequestStorage
from unittest import TestCase

import mock
from preggy import expect
from thumbor_dash.server import get_importer

from thumbor_dash.handlers.imaging import ThumborDashImagingHandler
from thumbor_dash.context import ThumborDashContext
from thumbor.config import Config
from thumbor_dash.verifiers import access_status_verifier, image_size_verifier, thumbnail_size_verifier, url_field_verifier


class ImagingHandlerTestCase(TestCase):
    def setUp(self):
        self.config = Config(
            MIN_WIDTH = 1,
            MIN_HEIGHT = 1,
            MAX_WIDTH = 1200,
            MAX_HEIGHT = 800,
            SECURITY_KEY = "MY-SECURITY-KEY",
            ALLOW_UNSAFE_URL = False,
            REQUEST_TIME_LIMIT = 1,
            USAGE_VIOLATION_LIMIT = 5,
            BAN_DURATION = 10
        )

        self.context = ThumborDashContext(
            server=None,
            config= self.config,
            importer= get_importer(self.config),
            request_handler=None
        )

        self.image = "myserver.com/myimg.jpg"

        self.imaging_handler = ThumborDashImagingHandler


    def test_check_image_with_uuid_exists_in_storage(self):
        with mock.patch.dict("os.environ", {"ENGINE": "test"}):
            expect(self.config).not_to_be_null()
            expect(self.context).not_to_be_null()
            expect(self.context.config.MAX_ID_LENGTH).to_be_greater_than(0)
    
    def test_ensure_image_is_specified(self):
        expect(self.imaging_handler.validate(self, self.image)).to_be_true()
        with mock.patch.dict("os.environ", {"ENGINE": "test"}):
            expect(self.config).not_to_be_null()
            expect(self.context).not_to_be_null()

    async def test_user_access_status_verification(self):
        requester_id = "REQUESTER_ID"
        checkAccessStatus = await access_status_verifier.verifyUserAccessStatus(requester_id, self.config)
        expect(checkAccessStatus).to_be_true()

    def test_verify_url_field(self):
        thumbnail_document = {
            'field': 'Field Value'
        }
        field = 'Field Value'
        expect(url_field_verifier.verifyURLField(thumbnail_document, field)).to_be_true()

    def test_verify_thumbnail_size(self):
        expect(thumbnail_size_verifier.verifyThumbnailSize(200, 600, 200, 400, 1200,800)).to_be_true()
        expect(thumbnail_size_verifier.verifyThumbnailSize(-1, 600, 200, 400, 1200,800)).to_be_false()
        expect(thumbnail_size_verifier.verifyThumbnailSize(1200, 900, 200, 300, 400,800)).to_be_false()
        expect(thumbnail_size_verifier.verifyThumbnailSize(500, 500, 200, 400, 1200,800)).to_be_true()

    def test_verify_thumbnail_size(self):
        expect(image_size_verifier.verifyImageSize(0, -1, 700, 500, 1200,800)).to_be_false()
        expect(image_size_verifier.verifyImageSize(300, 300, 200, 200, 1200,800)).to_be_true()
