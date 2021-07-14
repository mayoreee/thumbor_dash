from typing import Any, cast 

from thumbor.handler_lists import HandlerList 
from thumbor_dash.handlers.dashauth import DashAuthHandler 

def get_handlers(context: Any) -> HandlerList: 
    url = cast(str, context.config.DASHAUTH_ROUTE)
    return [
        (url, DashAuthHandler)
    ]