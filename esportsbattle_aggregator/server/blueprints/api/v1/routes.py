from . import api_v1_blueprint, response_wrapper

@api_v1_blueprint.get('/matches/get_all')
async def get_all_matches():
    
    ...