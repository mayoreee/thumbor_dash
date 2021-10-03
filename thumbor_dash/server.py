import sys
from thumbor_dash.app import ThumborDashServiceApp

import tornado.ioloop
from tornado.httpserver import HTTPServer
import warnings
from PIL import Image

from shutil import which
from thumbor.console import get_server_parameters
from thumbor.signal_handler import setup_signal_handler
from thumbor.server import run_server, get_importer, get_config, configure_log, get_context, get_as_integer

def get_application(context):
    return ThumborDashServiceApp(context)

def validate_config(config, server_parameters):
    if server_parameters.security_key is None:
        server_parameters.security_key = config.SECURITY_KEY

    if not isinstance(server_parameters.security_key, (bytes, str)):
        raise RuntimeError(
            "No security key was found for this instance of thumbor. "
            + "Please provide one using the conf file or a security key file."
        )

    if config.ENGINE or config.USE_GIFSICLE_ENGINE:
        # Error on Image.open when image pixel count is above MAX_IMAGE_PIXELS
        warnings.simplefilter("error", Image.DecompressionBombWarning)

    if config.USE_GIFSICLE_ENGINE:
        server_parameters.gifsicle_path = which("gifsicle")
        if server_parameters.gifsicle_path is None:
            raise RuntimeError(
                "If using USE_GIFSICLE_ENGINE configuration to True,"
                " the `gifsicle` binary must be in the PATH "
                "and must be an executable."
            )

    # Validate thumbor_dash user moderation settings
    if config.get("REQUEST_TIME_LIMIT") is None:
        raise RuntimeError(
            "Thumbor_Dash Error: Request time limit is not set. Please provide a time value for REQUEST_TIME_LIMIT in .conf file"
        )
 
    if config.get("USAGE_VIOLATION_LIMIT") is None:
        raise RuntimeError(
            "Thumbor_Dash Error: Usage violation limit is not set. Please provide a value for USAGE_VIOLATION_LIMIT in .conf file"
        )   

    if config.get("BAN_DURATION") is None:
        raise RuntimeError(
            "Thumbor_Dash Error: Ban duration is not set. Please provide a time value for BAN_DURATION in .conf file"
        )   

def main(arguments=None):
    """Runs thumbor server with the specified arguments."""
    if arguments is None:
        arguments = sys.argv[1:]

    server_parameters = get_server_parameters(arguments)
    config = get_config(
        server_parameters.config_path, server_parameters.use_environment
    )

    configure_log(config, server_parameters.log_level.upper())

    validate_config(config, server_parameters)

    importer = get_importer(config)

    with get_context(server_parameters, config, importer) as context:
        application = get_application(context)
        server = run_server(application, context)
        setup_signal_handler(server, config)
        tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main(sys.argv[1:])