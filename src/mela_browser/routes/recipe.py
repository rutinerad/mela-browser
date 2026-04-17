from __future__ import annotations

from urllib.parse import urlparse

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
    time_fields = [("Prep", recipe.prep_time), ("Cook", recipe.cook_time), ("Total", recipe.total_time)]
    meta = " · ".join(f"{label}: {val}" for label, val in time_fields if val)
    link = recipe.link or ""
    parsed = urlparse(link)
    source_url = link if parsed.scheme in ("http", "https") else None
    netloc = parsed.netloc.removeprefix("www.")
    source_label = netloc or link or None
    return render_template(
        "recipe.pug", recipe=recipe, meta=meta,
        source_url=source_url, source_label=source_label, yield_value=recipe.yield_value,
    )
