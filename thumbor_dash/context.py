from os.path import abspath, exists

from thumbor.filters import FiltersFactory
from thumbor.metrics.logger_metrics import Metrics
from thumbor.threadpool import ThreadPool
from thumbor.context import *


class ThumborDashContext(Context):
    """
    Class responsible for containing:
    * Server Configuration Parameters (port, ip, key, etc);
    * Configurations read from config file (or defaults);
    * Importer with imported modules (engine, filters, detectors, etc);
    * Request Parameters (width, height, smart, meta, etc).
    Each instance of this class MUST be unique per request.
    This class should not be cached in the server.
    """
    def __init__(self, server=None, config=None, importer=None, request_handler=None):
        self.server = server
        self.config = config
        if importer:
            self.modules = ThumborDashContextImporter(self, importer)
            if importer.metrics:
                self.metrics = importer.metrics(config)
            else:
                self.metrics = Metrics(config)
        else:
            self.modules = None
            self.metrics = Metrics(config)

        self.app_class = "thumbor_dash.app.ThumborDashServiceApp"

        if hasattr(self.config, "APP_CLASS"):
            self.app_class = self.config.APP_CLASS

        if (
            hasattr(self.server, "app_class")
            and self.server.app_class != "thumbor_dash.app.ThumborDashServiceApp"
        ):
            self.app_class = self.server.app_class

        self.filters_factory = FiltersFactory(
            self.modules.filters if self.modules else []
        )
        self.request_handler = request_handler
        self.thread_pool = ThreadPool.instance(
            getattr(config, "ENGINE_THREADPOOL_SIZE", 0)
        )
        self.headers = {}



class ThumborDashContextImporter(ContextImporter):
    def __init__(self, context, importer):
        super().__init__(context, importer)




class ThumborDashRequestParameters(RequestParameters):
    def __init__(
        self,
        debug=False,
        meta=False,
        trim=None,
        crop_left=None,
        crop_top=None,
        crop_right=None,
        crop_bottom=None,
        crop=None,
        adaptive=False,
        full=False,
        fit_in=False,
        stretch=False,
        width=0,
        height=0,
        horizontal_flip=False,
        vertical_flip=False,
        halign="center",
        valign="middle",
        dashauth = None,
        filters=None,
        smart=False,
        quality=80,
        image=None,
        url=None,
        extension=None,  
        buffer=None,  
        focal_points=None,
        unsafe=False,
        hash=None,  
        accepts_webp=False,
        request=None,
        max_age=None,
        auto_png_to_jpg=None,
    ):
        self.debug = bool(debug)
        self.meta = bool(meta)
        self.trim = trim
        if trim is not None:
            trim_parts = trim.split(":")
            self.trim_pos = trim_parts[1] if len(trim_parts) > 1 else "top-left"
            self.trim_tolerance = int(trim_parts[2]) if len(trim_parts) > 2 else 0

        if crop is not None:
            self.crop = {k: self.int_or_0(v) for k, v in crop.items()}
        else:
            self.crop = {
                "left": self.int_or_0(crop_left),
                "right": self.int_or_0(crop_right),
                "top": self.int_or_0(crop_top),
                "bottom": self.int_or_0(crop_bottom),
            }

        self.should_crop = (
            self.crop["left"] > 0
            or self.crop["top"] > 0
            or self.crop["right"] > 0
            or self.crop["bottom"] > 0
        )

        self.adaptive = bool(adaptive)
        self.full = bool(full)
        self.fit_in = bool(fit_in)
        self.stretch = bool(stretch)

        self.width = "orig" if width == "orig" else self.int_or_0(width)
        self.height = "orig" if height == "orig" else self.int_or_0(height)
        self.horizontal_flip = bool(horizontal_flip)
        self.vertical_flip = bool(vertical_flip)
        self.halign = halign or "center"
        self.valign = valign or "middle"
        self.smart = bool(smart)

        if filters is None:
            filters = []

        self.filters = filters
        self.dashauth = dashauth
        self.image_url = image
        self.url = url
        self.detection_error = None
        self.quality = quality
        self.buffer = None

        if focal_points is None:
            focal_points = []

        self.focal_points = focal_points
        self.hash = hash
        self.prevent_result_storage = False
        self.unsafe = unsafe == "unsafe" or unsafe is True
        self.format = None
        self.accepts_webp = accepts_webp
        self.max_bytes = None
        self.max_age = max_age
        self.auto_png_to_jpg = auto_png_to_jpg

        if request:
            self.url = request.path
            self.accepts_webp = "image/webp" in request.headers.get("Accept", "")

    @staticmethod
    def int_or_0(value):
        return 0 if value is None else int(value)