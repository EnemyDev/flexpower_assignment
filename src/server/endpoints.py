from aiohttp import web
import datetime
from ..analysis.pnl import strategy_pnl
from ..analysis.total_volume import volume_sum

# ==> Task 1.3
async def get_pnl(request):
    strategy_id = request.match_info.get('strategy_id', "strategy_1")
    results = {"strategy": strategy_id,
               "value": strategy_pnl(strategy_id),
               "unit": "euro",
               "capture_time": datetime.datetime.utcnow().isoformat() + 'Z'}
    return web.json_response(results)

# adding endpoint for prev tasks
async def get_volume(request):
    direction = request.match_info.get('direction', "buy")
    results = {"value": volume_sum(direction),
               "capture_time": datetime.datetime.utcnow().isoformat() + 'Z'}
    return web.json_response(results)