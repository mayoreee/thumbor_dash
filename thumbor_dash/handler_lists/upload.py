from typing import Any, cast

from thumbor.handler_lists import HandlerList
from thumbor_dash.handlers.image_resource import ThumborDashImageResourceHandler
from thumbor.handlers.upload import ImageUploadHandler


def get_handlers(context: Any) -> HandlerList:
    is_upload_enabled = cast(bool, context.config.UPLOAD_ENABLED)
    if not is_upload_enabled:
        return []

    return [
        (r"/image", ImageUploadHandler, {"context": context}),
        (r"/image/(.*)", ThumborDashImageResourceHandler, {"context": context}),
    ]