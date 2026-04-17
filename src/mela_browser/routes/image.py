from __future__ import annotations

from flask import Blueprint, Response, abort, current_app, make_response

from mela_cli.store import AmbiguousRecipeError, MelaStore, RecipeNotFoundError

bp = Blueprint("image", __name__)


@bp.route("/recipe/<selector>/image/<int:index>")
def show(selector: str, index: int) -> Response:
    store: MelaStore = current_app.config["STORE"]
    try:
        recipe = store.get_recipe(selector)
    except (RecipeNotFoundError, AmbiguousRecipeError):
        abort(404)
    matches = [img for img in recipe.images if img.index == index]
    if not matches:
        abort(404)
    image = matches[0]
    response = make_response(image.data)
    response.headers["Content-Type"] = image.media_type
    response.headers["Cache-Control"] = "private, max-age=3600"
    return response
