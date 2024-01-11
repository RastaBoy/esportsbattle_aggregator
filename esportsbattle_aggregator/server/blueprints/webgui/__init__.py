import os
import quart

webgui_blueprint = quart.Blueprint(
    name='webgui',
    import_name=__name__,
    static_folder=os.path.join(os.getcwd(), 'static')
)


@webgui_blueprint.route('/', defaults={'path': ''})
@webgui_blueprint.route('/<path:path>')
async def index(path):
    if not ('.' in path):
        return await webgui_blueprint.send_static_file('index.html')
    else:
        return await webgui_blueprint.send_static_file(path)
