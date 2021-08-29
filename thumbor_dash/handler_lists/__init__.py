from tornado.routing import _RuleList

BUILTIN_HANDLERS = [
    "thumbor.handler_lists.healthcheck",
    "thumbor_dash.handler_lists.upload",
    "thumbor.handler_lists.blacklist",
]

HandlerList = _RuleList