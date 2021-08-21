
from unittest import TestCase

import mock
from preggy import expect

import thumbor_dash.server
from tests.fixtures.custom_error_handler import ErrorHandler as CustomErrorHandler
from thumbor_dash.app import ThumborDashServiceApp
from thumbor.config import Config
from thumbor_dash.server import (
    configure_log,
    get_application,
    get_as_integer,
    get_config,
    get_context,
    get_importer,
    main,
    run_server,
    validate_config,
)


class ServerTestCase(TestCase):
    def test_can_get_value_as_integer(self):
        expect(get_as_integer("1")).to_equal(1)
        expect(get_as_integer("a")).to_be_null()
        expect(get_as_integer("")).to_be_null()
        expect(get_as_integer(None)).to_be_null()

    def test_can_get_config_from_path(self):
        config = get_config("./tests/fixtures/thumbor_config_server_test.conf")

        with mock.patch.dict("os.environ", {"ENGINE": "test"}):
            expect(config).not_to_be_null()
            expect(config.ALLOWED_SOURCES).to_be_like(["mydomain.com"])
            expect(config.ENGINE).to_be_like("thumbor.engines.pil")

    def test_can_get_config_with_env_enabled(self):
        config = get_config("./tests/fixtures/thumbor_config_server_test.conf", True)

        with mock.patch.dict("os.environ", {"ENGINE": "test"}):
            expect(config).not_to_be_null()
            expect(config.ALLOWED_SOURCES).to_be_like(["mydomain.com"])
            expect(config.ENGINE).to_be_like("test")

    @mock.patch("logging.basicConfig")
    def test_can_configure_log_from_config(self, basic_config_mock):
        conf = Config()
        configure_log(conf, "DEBUG")

        params = dict(
            datefmt="%Y-%m-%d %H:%M:%S",
            level=10,
            format="%(asctime)s %(name)s:%(levelname)s %(message)s",
        )

        basic_config_mock.assert_called_with(**params)

    @mock.patch("logging.config.dictConfig")
    def test_can_configure_log_from_dict_config(self, dict_config_mock):
        conf = Config(THUMBOR_LOG_CONFIG={"level": "INFO"})
        configure_log(conf, "DEBUG")

        params = dict(level="INFO",)

        dict_config_mock.assert_called_with(params)

    def test_can_import_default_modules(self):
        conf = Config()
        importer = get_importer(conf)

        expect(importer).not_to_be_null()
        expect(importer.filters).not_to_be_empty()

    def test_can_import_with_custom_error_handler_class(self):
        conf = Config(
            USE_CUSTOM_ERROR_HANDLING=True,
            ERROR_HANDLER_MODULE="tests.fixtures.custom_error_handler",
        )
        importer = get_importer(conf)

        expect(importer).not_to_be_null()
        expect(importer.error_handler_class).not_to_be_null()
        expect(importer.error_handler_class).to_be_instance_of(CustomErrorHandler)

    def test_validate_config_security_key(self):
        server_parameters = mock.Mock(security_key=None)
        conf = Config(SECURITY_KEY=None)

        with expect.error_to_happen(
            RuntimeError,
            message="No security key was found for this instance of thumbor. "
            "Please provide one using the conf file or a security key file.",
        ):
            validate_config(conf, server_parameters)

    def test_validate_config_security_key_from_config(self):
        server_parameters = mock.Mock(security_key=None)
        conf = Config(SECURITY_KEY="something", REQUEST_TIME_LIMIT = 1, USAGE_VIOLATION_LIMIT = 5, BAN_DURATION = 10 )

        validate_config(conf, server_parameters)
        expect(server_parameters.security_key).to_equal("something")

    @mock.patch.object(thumbor_dash.server, "which")
    def test_validate_gifsicle_path(self, which_mock):
        server_parameters = mock.Mock(security_key=None)
        conf = Config(SECURITY_KEY="test", USE_GIFSICLE_ENGINE=True, REQUEST_TIME_LIMIT = 1, USAGE_VIOLATION_LIMIT = 5, BAN_DURATION = 10 )

        which_mock.return_value = "/usr/bin/gifsicle"

        validate_config(conf, server_parameters)
        expect(server_parameters.gifsicle_path).to_equal("/usr/bin/gifsicle")

    @mock.patch.object(thumbor_dash.server, "which")
    def test_validate_null_gifsicle_path(self, which_mock):
        server_parameters = mock.Mock(security_key=None)
        conf = Config(SECURITY_KEY="test", USE_GIFSICLE_ENGINE=True, REQUEST_TIME_LIMIT = 1, USAGE_VIOLATION_LIMIT = 5, BAN_DURATION = 10 )

        which_mock.return_value = None

        with expect.error_to_happen(
            RuntimeError,
            message="If using USE_GIFSICLE_ENGINE configuration to True, "
            "the `gifsicle` binary must be in the PATH and must be an executable.",
        ):
            validate_config(conf, server_parameters)

    def test_get_context(self):
        server_parameters = mock.Mock(
            security_key=None, app_class="thumbor_dash.app.ThumborDashServiceApp"
        )
        conf = Config(SECURITY_KEY="test", REQUEST_TIME_LIMIT = 1, USAGE_VIOLATION_LIMIT = 5, BAN_DURATION = 10 )
        importer = get_importer(conf)
        context = get_context(server_parameters, conf, importer)

        expect(context).not_to_be_null()

    def test_get_application(self):
        server_parameters = mock.Mock(
            security_key=None, app_class="thumbor_dash.app.ThumborDashServiceApp"
        )
        conf = Config(SECURITY_KEY="test", REQUEST_TIME_LIMIT = 1, USAGE_VIOLATION_LIMIT = 5, BAN_DURATION = 10 )
        importer = get_importer(conf)
        context = get_context(server_parameters, conf, importer)
        app = get_application(context)

        expect(app).not_to_be_null()
        expect(app).to_be_instance_of(ThumborDashServiceApp)