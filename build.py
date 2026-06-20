import markdown
import yaml
from pathlib import Path

# Make the output folder once, before the loop.
Path("site").mkdir(exist_ok=True)

# First pass: collect info about every page.
# We can't build a sidebar while coverting a single page, because that
# page needs links to ALL pages, including ones we haven't read yet.
# So we loop once just to gather title/url/order for every file first.
pages = []

for md_file in Path("docs").glob("*.md"):
    with open(md_file) as f:
        text = f.read()

    parts = text.split("---")
    meta = yaml.safe_load(parts[1])
    body = parts[2].strip()

    pages.append({
        "title": meta["title"],
        "url": md_file.stem + ".html",
        # .get() with a fallback: if a page forgot to set order
        # use 999 so it sorts to the bottom instead of crashing.
        "order": meta.get("order", 999),
        "html": markdown.markdown(body),
    })

# Sort pages by their order number.
pages.sort(key=lambda p: p["order"])

# Build the sidebar navigation HTML once, from the sorted list.
# Single quotes outside so the double quotes in href="" don't collide.
# Second pass: write each page out, using the data we already collected.
# markdown.markdown() only returns a fragement (e.g. <h1>..</h1>, not a full
# page. Wrap it in a complete HTML skeleton and slot in the title + body.
# f-string: {meta["title"]} and {html} get replaced with those variable values.
nav = ""
for p in pages:
    nav += f'<a href="{p["url"]}">{p["title"]}</a><br>'

for p in pages:
    page = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{p["title"]}</title>
</head>
<body>
<nav>
{nav}
</nav>
    {p["html"]}
</body>
</html>"""

    with open("site/" + p["url"], "w") as f:
        f.write(page)

    print("Wrote site/" + p["url"])