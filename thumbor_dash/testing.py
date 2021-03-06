import mimetypes
import random
from io import BytesIO
from os.path import dirname, join, realpath
from urllib.parse import urlencode

import mock
from PIL import Image
from SSIM_PIL import compare_ssim
from tornado.testing import AsyncHTTPTestCase

from thumbor_dash.app import ThumborDashServiceApp
from thumbor.config import Config
from thumbor_dash.context import *
from thumbor.engines.pil import Engine as PilEngine
from thumbor.importer import Importer
from thumbor.transformer import Transformer


def get_ssim(actual, expected):
    if actual.size[0] != expected.size[0] or actual.size[1] != expected.size[1]:
        raise RuntimeError(
            "Can't calculate SSIM for images of different sizes "
            "(one is %dx%d, the other %dx%d)."
            % (actual.size[0], actual.size[1], expected.size[0], expected.size[1],)
        )

    return compare_ssim(actual, expected)


def encode_multipart_formdata(fields, files):
    boundary = b"thumborUploadFormBoundary"
    crlf = b"\r\n"
    lines = []
    for key, value in fields.items():
        lines.append(b"--" + boundary)
        lines.append(b'Content-Disposition: form-data; name="%s"' % key.encode())
        lines.append(b"")
        lines.append(value)
    for (key, filename, value) in files:
        lines.append(b"--" + boundary)
        lines.append(
            b'Content-Disposition: form-data; name="%s"; filename="%s"'
            % (key.encode(), filename.encode())
        )
        lines.append(
            b"Content-Type: %s" % mimetypes.guess_type(filename)[0].encode()
            or b"application/octet-stream"
        )
        lines.append(b"")
        lines.append(value)
    lines.append(b"")
    lines.append(b"")
    lines.append(b"--" + boundary + b"--")
    body = crlf.join(lines)
    content_type = b"multipart/form-data; boundary=%s" % boundary
    return content_type, body



class TestCase(AsyncHTTPTestCase):
    _multiprocess_can_split_ = True

    def get_app(self):
        self.context = self.get_context()
        return ThumborDashServiceApp(self.context)

    def get_config(self):  # Meant to be overriden pylint: disable=no-self-use
        return Config()

    def get_server(self):  # Meant to be overriden pylint: disable=no-self-use
        return None

    def get_importer(self):
        importer = Importer(self.config)
        importer.import_modules()
        return importer

    def get_request_handler(self,):  # Meant to be overriden pylint: disable=no-self-use
        return None

    def get_context(self):
        self.config = (  # This is a test case pylint: disable=attribute-defined-outside-init
            self.get_config()
        )
        self.server = (  # This is a test case pylint: disable=attribute-defined-outside-init
            self.get_server()
        )
        self.importer = (  # This is a test case pylint: disable=attribute-defined-outside-init
            self.get_importer()
        )
        self.request_handler = (  # This is a test case pylint: disable=attribute-defined-outside-init
            self.get_request_handler()
        )
        self.importer.import_modules()
        return ThumborDashContext(self.server, self.config, self.importer, self.request_handler)

    async def async_fetch(self, path, method="GET", body=None, headers=None):
        return await self.http_client.fetch(
            self.get_url(path),
            method=method,
            body=body,
            headers=headers,
            allow_nonstandard_methods=True,
            raise_error=False,
        )

    async def async_get(self, path, headers=None):
        return await self.async_fetch(
            path, method="GET", body=urlencode({}, doseq=True), headers=headers
        )

    async def async_post(self, path, headers, body):
        return await self.async_fetch(path, method="POST", body=body, headers=headers,)

    async def async_put(self, path, headers, body):
        return await self.async_fetch(path, method="PUT", body=body, headers=headers,)

    async def async_delete(self, path, headers):
        return await self.async_fetch(
            path, method="DELETE", body=urlencode({}, doseq=True), headers=headers,
        )

    async def async_post_files(self, path, data=None, files=None):
        if data is None:
            data = {}
        if files is None:
            files = []
        multipart_data = encode_multipart_formdata(data, files)

        return await self.async_fetch(
            path,
            method="POST",
            body=multipart_data[1],
            headers={"Content-Type": multipart_data[0]},
        )

class FilterTestCase(TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        super().setUp()
        self.context = {}

    def get_filter(self, filter_name, params_string="", config_context=None):
        config = Config(
            FILTERS=[filter_name],
            LOADER="thumbor.loaders.file_loader",
            FILE_LOADER_ROOT_PATH=self.get_fixture_root_path(),
        )
        importer = Importer(config)
        importer.import_modules()

        req = ThumborDashRequestParameters()

        context = ThumborDashContext(config=config, importer=importer)
        context.request = req
        context.request.engine = context.modules.engine

        if config_context is not None:
            config_context(context)

        self.context = context

        fltr = importer.filters[0]
        fltr.pre_compile()

        context.transformer = Transformer(context)

        return fltr(params_string, context=context)

    @staticmethod
    def get_fixture_root_path():
        return join(dirname(realpath(__file__)), "fixtures", "filters")

    def get_fixture_path(self, name):
        return f"{self.get_fixture_root_path()}/{name}"

    def get_fixture(self, name, mode="RGB"):
        image = Image.open(self.get_fixture_path(name))
        return image.convert(mode)

    async def get_filtered(
        self, source_image, filter_name, params_string, config_context=None, mode="RGB",
    ):
        fltr = self.get_filter(filter_name, params_string, config_context)
        image = Image.open(self.get_fixture_path(source_image))
        img_buffer = BytesIO()

        if params_string == "quality(10)":
            image.save(img_buffer, "JPEG", quality=10)
            fltr.engine.load(img_buffer.getvalue(), ".jpg")
        else:
            image.save(img_buffer, "PNG", quality=100)
            fltr.engine.load(img_buffer.getvalue(), ".png")

        fltr.context.transformer.img_operation_worker()

        await fltr.run()

        fltr.engine.image = fltr.engine.image.convert(mode)

        return fltr.engine.image

    @staticmethod
    def get_ssim(actual, expected):
        return get_ssim(actual, expected)

    def debug(self, image):  # pylint: disable=arguments-differ
        image = Image.fromarray(image)
        path = "/tmp/debug_image_%s.jpg" % random.randint(1, 10000)
        image.save(path, "JPEG")
        print("The debug image was in %s." % path)

    @staticmethod
    def debug_size(image):
        loaded = Image.fromarray(image)
        print(
            "Image dimensions are %dx%d (shape is %s)"
            % (loaded.size[0], loaded.size[1], image.shape)
        )


class DetectorTestCase(TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        super().setUp()
        self.context.request = mock.Mock(focal_points=[])
        self.engine = PilEngine(self.context)
        self.context.modules.engine = self.engine