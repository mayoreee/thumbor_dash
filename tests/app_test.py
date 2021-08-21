from thumbor_dash.url import ThumborDashUrl
from preggy import expect

from thumbor_dash.app import ThumborDashServiceApp
from thumbor_dash.testing import TestCase


class AppTestCase(TestCase):
    def test_can_create_app(self):
        app = ThumborDashServiceApp(self.context)
        expect(app).not_to_be_null()
        expect(app.context).to_equal(self.context)

    def test_can_get_handlers(self):
        ctx = self.get_context()
        ctx.config.UPLOAD_ENABLED = False
        ctx.config.USE_BLACKLIST = False
        ctx.config.HEALTHCHECK_ROUTE = "/health"
        app = ThumborDashServiceApp(ctx)

        handlers = app.get_handlers()
        expect(handlers).to_length(2)
        expect(handlers[0][0]).to_equal(r"/health")
        expect(handlers[1][0]).to_equal(ThumborDashUrl.regex())

    def test_can_get_handlers_with_upload(self):
        ctx = self.get_context()
        ctx.config.UPLOAD_ENABLED = True
        ctx.config.USE_BLACKLIST = False
        app = ThumborDashServiceApp(ctx)

        handlers = app.get_handlers()
        expect(handlers).to_length(4)

    def test_can_get_handlers_with_blacklist(self):
        ctx = self.get_context()
        ctx.config.UPLOAD_ENABLED = False
        ctx.config.USE_BLACKLIST = True
        app = ThumborDashServiceApp(ctx)

        handlers = app.get_handlers()
        expect(handlers).to_length(3)