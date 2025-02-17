from aiohttp import web
from .routes import register_routes

if __name__ == '__main__':
    app = web.Application()
    register_routes(app)
    web.run_app(app,port=8080)
    