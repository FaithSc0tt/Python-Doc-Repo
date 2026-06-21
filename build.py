import markdown
import yaml
from pathlib import Path
import shutil

# Start each build from a clean slate so old/renamed files don't linger.
if Path("site").exists():
    shutil.rmtree("site")
Path("site").mkdir()

# The site's stylesheet, written out fresh on every build.
css = """
/* ── Design tokens: tweak these to restyle everything at once ── */
:root {
  --bg-0: #131313;          /* deepest background (near-black) */
  --bg-1: #1a0307;          /* page background, very dark red */
  --card:  #2a0610;         /* card surface, deep crimson-brown */
  --card-edge: #7a0213;     /* card border, dark blood red */
  --ink:   #f7f1f2;         /* primary text, warm off-white */
  --ink-soft: #c08a92;      /* secondary text, muted rose */
  --accent: #cd0c2b;        /* the bright accent — signal red */
  --accent-soft: rgba(205, 12, 43, 0.16);
  --radius: 16px;
}

* { box-sizing: border-box; }

/* Page: deep red that lifts toward the top. */
body {
  margin: 0;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  background:
    radial-gradient(ellipse at 70% 0%, #7a0213 0%, transparent 55%),
    linear-gradient(180deg, var(--bg-1) 0%, var(--bg-0) 100%);
  background-attachment: fixed;
  color: var(--ink);
  line-height: 1.7;
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}

/* Sidebar: a flush dark rail. */
nav {
  position: fixed;
  top: 0;
  left: 0;
  width: 240px;
  height: 100vh;
  box-sizing: border-box;
  padding: 28px 16px;
  background: var(--bg-0);
  border-right: 1px solid var(--card-edge);
  overflow-y: auto;
}

/* Nav links: pill-shaped, soft until hovered. */
nav a {
  display: block;
  padding: 10px 14px;
  margin-bottom: 2px;
  border-radius: 10px;
  color: var(--ink-soft);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
  letter-spacing: 0.01em;
  transition: all 0.15s ease;
}
nav a:hover {
  color: var(--ink);
  background: var(--accent-soft);
}

/* Folder headings: small, muted, spaced labels. */
nav .nav-group {
  margin: 22px 0 8px;
  padding: 0 14px;
  color: var(--ink-soft);
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  opacity: 0.7;
}

/* Content area: the markdown sits inside a centred card. */
main {
  margin-left: 240px;
  padding: 48px;
  display: flex;
  justify-content: center;
}

/* The content card: lifts off the page with surface, border, padding. */
.card {
  background: var(--card);
  border: 1px solid var(--card-edge);
  border-radius: var(--radius);
  padding: 40px 44px;
  max-width: 820px;
  width: 100%;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.35);
}

/* Typography hierarchy. */
h1, h2, h3 { color: var(--ink); letter-spacing: -0.01em; font-weight: 700; }
h1 {
  font-size: 2.1rem;
  margin: 0 0 8px;
  padding-bottom: 18px;
  border-bottom: 1px solid var(--card-edge);
}
h2 { font-size: 1.4rem; margin: 32px 0 12px; }
h3 { font-size: 1.1rem; margin: 24px 0 8px; }

p, ul, ol { color: var(--ink); max-width: 680px; }

/* Content links: accent colour, underline grows on hover. */
main a {
  color: var(--accent);
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.15s ease;
}
main a:hover { border-bottom-color: var(--accent); }

/* Code. */
code {
  background: var(--bg-0);
  color: #f0b49a;
  padding: 2px 7px;
  border-radius: 6px;
  font-size: 0.86em;
}
pre {
  background: var(--bg-0);
  border: 1px solid var(--card-edge);
  border-radius: 12px;
  padding: 18px 20px;
  overflow-x: auto;
}
pre code { background: none; padding: 0; color: var(--ink); }
"""

with open("site/style.css", "w") as f:
    f.write(css)

# First pass: collect info about every page.
# rglob (recursive) finds .md files in docs/ AND all its subfolders.
pages = []

for md_file in Path("docs").rglob("*.md"):
    with open(md_file) as f:
        text = f.read()

    parts = text.split("---")
    meta = yaml.safe_load(parts[1])
    body = parts[2].strip()

    # rel is the path from docs/ (e.g. guide/setup.md); folder is just the
    # subfolder ("." for top-level, "guide" for a subfolder).
    rel = md_file.relative_to("docs")
    folder = md_file.parent.relative_to("docs")

    pages.append({
        "title": meta["title"],
        "url": str(rel.with_suffix(".html")),   # guide/setup.html (or hello.html)
        # .get() with a fallback: if a page forgot to set order,
        # use 999 so it sorts to the bottom instead of crashing.
        "order": meta.get("order", 999),
        "html": markdown.markdown(body),
        "folder": str(folder),
    })

# Sort pages by their order number.
pages.sort(key=lambda p: p["order"])

# Group pages by their folder: {folder_name: [pages in it]}
# Classic group idiom: if the key isn't there yet, start a list, then append.
groups = {}
for p in pages:
    folder = p["folder"]
    if folder not in groups:
        groups[folder] = []
    groups[folder].append(p)

# Second pass: write each page, building its nav with the right path prefix.
for p in pages:
    # How deep is this page? Count the slashes in its url.
    depth = p["url"].count("/")
    prefix = "../" * depth          # "", "../", "../../", ...

    # Build this page's sidebar fresh, prefixing every link so it resolves
    # correctly no matter how deep the current page sits.
    nav = ""
    # Top-level pages first (folder "."), if any.
    for top in groups.get(".", []):
        nav += f'<a href="{prefix}{top["url"]}">{top["title"]}</a><br>'
    # Then each subfolder as a titled section.
    for folder, folder_pages in groups.items():
        if folder == ".":
            continue
        nav += f'<div class="nav-group">{folder}</div>'
        for fp in folder_pages:
            nav += f'<a href="{prefix}{fp["url"]}">{fp["title"]}</a><br>'

    # Build the full page.
    page = f"""<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{p["title"]}</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
    <link rel="stylesheet" href="{prefix}style.css">
</head>
<body>
<nav>
{nav}
</nav>
<main>
<div class="card">
{p["html"]}
</div>
</main>
</body>
</html>"""

    # Write it, creating the page's folder if needed.
    out_path = Path("site") / p["url"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        f.write(page)

    print("Wrote site/" + p["url"])