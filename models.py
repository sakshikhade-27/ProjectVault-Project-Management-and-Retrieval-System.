import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT NOT NULL UNIQUE COLLATE NOCASE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL,
    parent_id INTEGER REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS projects (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT NOT NULL,
    developed_by TEXT NOT NULL,
    description  TEXT,
    project_date TEXT NOT NULL,
    category_id  INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    file_name    TEXT,
    file_path    TEXT,
    created_by   INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at   TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(SCHEMA)
    db.commit()


def build_tree():
    """Return root categories as nested dicts: children, projects and a total count."""
    db = get_db()
    cats = db.execute(
        "SELECT id, name, parent_id FROM categories ORDER BY name COLLATE NOCASE"
    ).fetchall()
    projects = db.execute(
        "SELECT id, title, category_id FROM projects ORDER BY title COLLATE NOCASE"
    ).fetchall()

    nodes = {
        c["id"]: {"id": c["id"], "name": c["name"], "parent_id": c["parent_id"],
                  "children": [], "projects": [], "total": 0}
        for c in cats
    }
    roots = []
    for node in nodes.values():
        parent = nodes.get(node["parent_id"])
        if parent:
            parent["children"].append(node)
        else:
            roots.append(node)

    for p in projects:
        nodes[p["category_id"]]["projects"].append(dict(p))

    def count(node):
        node["total"] = len(node["projects"]) + sum(count(c) for c in node["children"])
        return node["total"]

    for root in roots:
        count(root)
    return roots


def category_options():
    """Flat, ordered list of categories for dropdowns, with the full path of each."""
    options = []

    def walk(nodes, prefix):
        for node in nodes:
            path = prefix + [node["name"]]
            options.append({
                "id": node["id"],
                "path": " > ".join(path),
                "label": "\u00a0\u00a0\u00a0" * (len(path) - 1) + node["name"],
            })
            walk(node["children"], path)

    walk(build_tree(), [])
    return options


def category_path_map():
    return {o["id"]: o["path"] for o in category_options()}


def subtree_ids(category_id):
    rows = get_db().execute(
        """
        WITH RECURSIVE sub(id) AS (
            SELECT id FROM categories WHERE id = ?
            UNION ALL
            SELECT c.id FROM categories c JOIN sub ON c.parent_id = sub.id
        )
        SELECT id FROM sub
        """,
        (category_id,),
    ).fetchall()
    return [r["id"] for r in rows]
