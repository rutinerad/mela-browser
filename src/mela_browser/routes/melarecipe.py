from __future__ import annotations

from flask import Blueprint, Response, abort, current_app

from mela_cli.store import AmbiguousRecipeError, MelaStore, RecipeNotFoundError
from mela_cli.utils import json_dumps, slugify

bp = Blueprint("melarecipe", __name__)


@bp.route("/recipe/<selector>/melarecipe")
def download(selector: str) -> Response:
    store: MelaStore = current_app.config["STORE"]
    try:
        recipe = store.get_recipe(selector)
    except (RecipeNotFoundError, AmbiguousRecipeError):
        abort(404)
    filename = f"{slugify(recipe.title)}.melarecipe"
    return Response(
        json_dumps(recipe.to_melarecipe_dict()),
        mimetype="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
