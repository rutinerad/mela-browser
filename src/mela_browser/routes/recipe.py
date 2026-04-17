from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template

from mela_cli.store import AmbiguousRecipeError, MelaStore, RecipeNotFoundError

bp = Blueprint("recipe", __name__)


@bp.route("/recipe/<selector>")
def show(selector: str) -> str:
    store: MelaStore = current_app.config["STORE"]
    try:
        recipe = store.get_recipe(selector)
    except (RecipeNotFoundError, AmbiguousRecipeError):
        abort(404)
    return render_template("recipe.pug", recipe=recipe)
