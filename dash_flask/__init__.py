from flask import Flask
from flask_assets import Environment

def init_app():

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)

    with app.app_context():
        from . import routes
        from .assets import compile_static_assets

        from .plotlydash.pg_trimestral import init_trimestral
        from .plotlydash.pg_analistas import init_analistas
        from .plotlydash.pg_aging import init_aging

        app = init_trimestral(app)
        app = init_analistas(app)
        app = init_aging(app)

        compile_static_assets(assets)

        return app