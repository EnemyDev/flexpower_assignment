from aiohttp import web
from .endpoints import get_pnl, get_volume

def register_routes(app):
    app.add_routes([web.get('/v1/pnl/{strategy_id}', get_pnl)])
    app.add_routes([web.get('/v1/volume/{direction}', get_volume)])