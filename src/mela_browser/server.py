from __future__ import annotations

import html
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from mela_cli.store import AmbiguousRecipeError, MelaStore, RecipeNotFoundError

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>
  body {{ font-family: sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }}
  a {{ color: #c0392b; }}
  h1 {{ border-bottom: 1px solid #eee; padding-bottom: .5rem; }}
  ul {{ list-style: none; padding: 0; }}
  li {{ padding: .3rem 0; border-bottom: 1px solid #f5f5f5; }}
  pre {{ white-space: pre-wrap; line-height: 1.6; }}
  .back {{ display: inline-block; margin-bottom: 1rem; }}
  .meta {{ color: #888; font-size: .9rem; margin-bottom: 1.5rem; }}
</style>
</head>
<body>
{body}
</body>
</html>"""


def _page(title: str, body: str) -> bytes:
    return PAGE.format(title=html.escape(title), body=body).encode("utf-8")


def make_handler(store: MelaStore) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            path = urlparse(self.path).path.rstrip("/") or "/"
            if path == "/":
                self._serve_list()
            elif path.startswith("/recipe/"):
                self._serve_recipe(path[len("/recipe/"):])
            else:
                self._send(404, _page("Not found", "<h1>Not found</h1>"))

        def _serve_list(self) -> None:
            recipes = store.list_recipes()
            items = "\n".join(
                f'<li><a href="/recipe/{r.pk}">{html.escape(r.title)}</a>'
                + (f' <span class="meta">{html.escape(", ".join(r.tags))}</span>' if r.tags else "")
                + "</li>"
                for r in recipes
            )
            body = f"<h1>Recipes ({len(recipes)})</h1><ul>{items}</ul>"
            self._send(200, _page("Recipes", body))

        def _serve_recipe(self, selector: str) -> None:
            try:
                recipe = store.get_recipe(selector)
            except (RecipeNotFoundError, AmbiguousRecipeError) as exc:
                self._send(404, _page("Not found", f"<h1>Not found</h1><p>{html.escape(str(exc))}</p>"))
                return

            meta_parts = []
            if recipe.tags:
                meta_parts.append(", ".join(html.escape(t) for t in recipe.tags))
            times = " · ".join(
                f"{label}: {html.escape(val)}"
                for label, val in [("Prep", recipe.prep_time), ("Cook", recipe.cook_time), ("Total", recipe.total_time)]
                if val
            )
            if times:
                meta_parts.append(times)
            if recipe.yield_value:
                meta_parts.append(f"Yield: {html.escape(recipe.yield_value)}")

            parts = ['<a class="back" href="/">← All recipes</a>']
            parts.append(f"<h1>{html.escape(recipe.title)}</h1>")
            if meta_parts:
                parts.append(f'<p class="meta">{" &nbsp;·&nbsp; ".join(meta_parts)}</p>')
            if recipe.ingredients:
                parts.append(f"<h2>Ingredients</h2><pre>{html.escape(recipe.ingredients)}</pre>")
            if recipe.instructions:
                parts.append(f"<h2>Instructions</h2><pre>{html.escape(recipe.instructions)}</pre>")
            if recipe.notes:
                parts.append(f"<h2>Notes</h2><pre>{html.escape(recipe.notes)}</pre>")
            if recipe.link:
                parts.append(f'<p><a href="{html.escape(recipe.link)}" target="_blank">Source ↗</a></p>')

            self._send(200, _page(recipe.title, "\n".join(parts)))

        def _send(self, status: int, body: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:  # noqa: A002
            pass  # suppress per-request noise; the caller prints a startup URL

    return Handler


def serve(store: MelaStore, host: str = "127.0.0.1", port: int = 8080) -> None:
    server = HTTPServer((host, port), make_handler(store))
    print(f"Serving at http://{host}:{port}/  (Ctrl-C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
