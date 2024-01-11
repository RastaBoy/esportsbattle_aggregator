import quart
import typing
import json

api_v1_blueprint = quart.Blueprint(
    "api_v1",
    __name__
)


@api_v1_blueprint.errorhandler(Exception)
async def error_handler(e : Exception):
    return quart.Response(
        json.dumps({
            "result" : False,
            "error_class" : e.__class__.__name__,
            "error_text" : str(e)
        }), 
        status=500,
        content_type="application/json"
    )
    

def response_wrapper(func : typing.Awaitable):
    async def wrap(*args, **kwargs):
        return quart.Response(
            json.dumps({
                "result" : True,
                "data" : await func(*args, **kwargs)
            }),
            status=200
        )
    return wrap

from .routes import *