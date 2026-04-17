from __future__ import annotations

from flask import Blueprint, current_app, render_template

from mela_cli.store import MelaStore

bp = Blueprint("list", __name__)


@bp.route("/")
def index() -> str:
    store: MelaStore = current_app.config["STORE"]
    recipes = store.list_recipes()
    return render_template("list.pug", recipes=recipes)
