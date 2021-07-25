import tornado.ioloop
import tornado.web

from thumbor_dash.url import ThumborDashUrl
from thumbor_dash.handlers.imaging import ThumborDashImagingHandler
from thumbor.app import ThumborServiceApp


class ThumborDashServiceApp(ThumborServiceApp):

    def get_handlers(self):
        handlers = []
        for handler_list in self.context.modules.importer.handler_lists:
            get_handlers = getattr(handler_list, "get_handlers", None)
            if get_handlers is None:
                continue
            handlers.extend(get_handlers(self.context))

        # Imaging handler (GET)
        handlers.append((ThumborDashUrl.regex(), ThumborDashImagingHandler, {"context": self.context}))

        return handlers