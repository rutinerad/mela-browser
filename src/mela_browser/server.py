from __future__ import annotations

from flask import Flask

from mela_browser.routes import image as image_route
from mela_browser.routes import list as list_route
from mela_browser.routes import melarecipe as melarecipe_route
from mela_browser.routes import recipe as recipe_route
from mela_cli.store import MelaStore


def create_app(store: MelaStore) -> Flask:
    app = Flask(__name__)
    app.jinja_env.add_extension("pypugjs.ext.jinja.PyPugJSExtension")
    app.config["STORE"] = store
    app.register_blueprint(list_route.bp)
    app.register_blueprint(recipe_route.bp)
    app.register_blueprint(image_route.bp)
    app.register_blueprint(melarecipe_route.bp)
    return app


def serve(store: MelaStore, host: str = "127.0.0.1", port: int = 8080, debug: bool = False) -> None:
    app = create_app(store)
    if debug:
        app.run(host=host, port=port, threaded=False, debug=True)
    else:
        from waitress import serve as waitress_serve
        waitress_serve(app, host=host, port=port, threads=1)
