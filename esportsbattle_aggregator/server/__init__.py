import quart
import hypercorn

from hypercorn.asyncio import serve

from .blueprints.api.v1 import api_v1_blueprint
from .blueprints.webgui import webgui_blueprint

def build_server(
        is_dev : bool = False
    ) -> quart.Quart:
    app = quart.Quart(__name__)

    app.register_blueprint(webgui_blueprint)
    app.register_blueprint(api_v1_blueprint)

    if is_dev:
        import quart_cors
        app = quart_cors.cors(app, allow_origin="*")

    
    return app


async def run_server(
        server_port : int = 11011,
        is_dev : bool = False
    ):
    cfg = hypercorn.config.Config()
    cfg.bind = f"0.0.0.0:{server_port}"

    return await serve(
        app=build_server(is_dev),
        config=cfg
    )
