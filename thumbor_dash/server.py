import sys
from thumbor_dash.app import ThumborDashServiceApp

import tornado.ioloop

from thumbor.console import get_server_parameters
from thumbor.signal_handler import setup_signal_handler
from thumbor.server import run_server, get_importer, get_config, configure_log, validate_config, get_context, get_as_integer

def get_application(context):
    return ThumborDashServiceApp(context)

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