# 🩸 Crimson Docs

A minimal static documentation site generator, written from scratch in Python. It turns a folder of Markdown files into a styled, navigable HTML website with a single command — no frameworks, no build tools, just a script you can read top to bottom.

The default theme is a dark, blood-lit gothic style inspired by *Castlevania*: near-black backgrounds bleeding into deep crimson, bone-white serif headings, and small-caps navigation.

---

## ✨ Features

- **Markdown → HTML** — write pages in plain Markdown, get clean HTML out.
- **Front matter** — set each page's title and sidebar order with a small metadata block.
- **Automatic navigation** — every page is found, sorted, and linked into a shared sidebar.
- **Self-contained build** — one command regenerates the entire site, stylesheet included.
- **Custom gothic theme** — a dark, candlelit aesthetic driven entirely by CSS you can tweak.

---

## 📋 Requirements

- Python 3.8 or newer
- Two libraries:
  - [`markdown`](https://pypi.org/project/Markdown/) — converts Markdown to HTML
  - [`pyyaml`](https://pypi.org/project/PyYAML/) — reads the front-matter metadata

Install them with:

```bash
pip install markdown pyyaml
```

---

## 🚀 Usage

### 1. Add your pages

Put Markdown files inside the `docs/` folder. Each page starts with a **front-matter block** between `---` fences that sets its title and position in the sidebar:

```markdown
---
title: Introduction
order: 1
---
# Introduction

This is my **first** page.
```

- `title` — the name shown in the sidebar and browser tab.
- `order` — controls the page's position in the sidebar (lower numbers appear first). If you leave it out, the page sorts to the bottom.

### 2. Build the site

From the project root, run:

```bash
python build.py
```

This reads every `.md` file in `docs/`, converts it, and writes the finished site into a `site/` folder.

### 3. View it

Open any generated page in your browser:

```
site/index.html
```

(or double-click it in your file manager). Click between pages using the sidebar.

> **Note:** The `site/` folder is fully disposable — it's rebuilt from scratch every time you run `build.py`. Your source of truth is the `docs/` folder and the script. You can safely delete `site/` and regenerate it at any time.

---

## 📁 Project structure

```
mydocs/
├── build.py        # the generator
├── docs/           # your Markdown source pages
│   ├── hello.md
│   └── intro.md
└── site/           # generated output (created by build.py)
    ├── hello.html
    ├── intro.html
    └── style.css
```

---

## 🎨 Customising the theme

All styling lives in a single `css` string near the top of `build.py`. Two accent colours drive most of the mood:

- `#a01420` — the crimson used for rules, borders, and hover highlights
- `#ece3d2` — the warm bone colour used for headings

Change those values and rebuild to make the theme your own. The page background is a layered gradient (a red glow over a black-to-blood-to-black fade) — adjust the colours in the `body` rule to shift the atmosphere.

---

## 🔮 Future features

Planned additions, roughly in order of ambition:

- [ ] **Active page highlighting** — visually mark the page you're currently viewing in the sidebar.
- [ ] **Nested navigation** — let subfolders inside `docs/` become collapsible sidebar sections.
- [ ] **Jinja2 templating** — move the HTML out of Python strings into proper template files for cleaner separation of structure and logic.
- [ ] **Live-reload dev server** — automatically rebuild and refresh the browser when a source file changes.
- [ ] **Diagramming tool** — a custom Markdown block for drawing solution diagrams directly on the page, saved into the Markdown as editable XML and rendered as images.
- [ ] **Syntax highlighting** — colourised code blocks for code-heavy documentation.
- [ ] **Search** — client-side search across all pages.

---

## 📝 Notes

This project was built as a learning exercise — a from-scratch look at how static site generators like DocFX, MkDocs, and Jekyll actually work under the hood. Every line is hand-written and understood rather than pulled from a framework.

---