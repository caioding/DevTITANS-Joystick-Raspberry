"""Exporta um GitHub Project (v2) PÚBLICO sem login: lê os dados que a própria página embute
(blocos <script id="memex-...">) e salva JSON + CSV + Markdown.

Uso: python exportar_board.py https://github.com/users/OWNER/projects/N PASTA_SAIDA
"""
import csv
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

url, out = sys.argv[1], Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
page = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "backup-script"})).read().decode()

blocks = {}
for sid, body in re.findall(r'<script type="application/json" id="(memex-[a-z-]+)">(.*?)</script>', page, re.S):
    if sid in ("memex-data", "memex-columns-data", "memex-paginated-items-data", "memex-views", "memex-charts-data",
               "memex-owner", "memex-creator"):
        blocks[sid] = json.loads(html.unescape(body))
        (out / f"{sid}.json").write_text(json.dumps(blocks[sid], ensure_ascii=False, indent=2), encoding="utf-8")

cols = blocks["memex-columns-data"]
items_data = blocks["memex-paginated-items-data"]
# Itens agrupados pela visão (groupedItems[*].nodes) ou numa lista simples (nodes).
if "groupedItems" in items_data:
    items = [n for g in items_data["groupedItems"] for n in g["nodes"]]
else:
    items = items_data.get("nodes", [])

col_by_id = {str(c["id"]): c for c in cols}


def value(col, raw):
    """Converte o valor bruto de um campo no texto que aparece no board."""
    if raw is None:
        return ""
    dt = col.get("dataType")
    if dt == "singleSelect":
        opts = {o["id"]: o["name"] for o in col.get("settings", {}).get("options", [])}
        return opts.get(raw.get("id") if isinstance(raw, dict) else raw, str(raw))
    if dt == "iteration":
        conf = col.get("settings", {}).get("configuration", {})
        its = {i["id"]: i for i in conf.get("iterations", []) + conf.get("completedIterations", [])}
        it = its.get(raw.get("id") if isinstance(raw, dict) else raw)
        return f"{it['title']} ({it['startDate']}, {it['duration']} dias)" if it else str(raw)
    if dt == "title":
        return (raw.get("title") or {}).get("raw", "") if isinstance(raw, dict) else str(raw)
    if dt == "assignees":
        return ", ".join(a.get("login", "") for a in raw)
    if dt == "labels":
        return ", ".join(l.get("name", "") for l in raw)
    if isinstance(raw, dict):
        return str(raw.get("raw", raw.get("name", raw.get("title", raw))))
    if isinstance(raw, list):
        return ", ".join(str(x.get("name", x.get("login", x)) if isinstance(x, dict) else x) for x in raw)
    return str(raw)


visible = [c for c in cols if c.get("dataType") not in ("tracks", "trackedBy", "subIssuesProgress", "parentIssue",
                                                         "linkedPullRequests", "reviewers")]
rows = []
for it in items:
    title_val = next((v.get("value") for v in it.get("memexProjectColumnValues", [])
                      if v.get("memexProjectColumnId") == "Title"), None) or {}
    row = {"#": title_val.get("number", "")}
    for c in visible:
        raw = it.get("memexProjectColumnValues")
        raw = next((v.get("value") for v in raw if str(v.get("memexProjectColumnId")) == str(c["id"])), None) \
            if isinstance(raw, list) else None
        row[c["name"]] = value(c, raw)
    rows.append(row)

with open(out / "board.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["#"])
    w.writeheader()
    w.writerows(rows)

title = blocks["memex-data"].get("title", "Board")
status_col = next((c for c in cols if c["name"] == "Status"), None)
order = [o["name"] for o in status_col["settings"]["options"]] if status_col else []
md = [f"# Board: {title}", "", f"Original: {url}", "", f"{len(rows)} itens. Campos: {', '.join(c['name'] for c in visible)}.", ""]
for st in order + [""]:
    group = [r for r in rows if r.get("Status", "") == st]
    if not group:
        continue
    md += [f"## {st or '(sem status)'} ({len(group)})", "",
           "| # | Título | Responsáveis | " + " | ".join(k for k in rows[0] if k not in ("#", "Title", "Assignees", "Status")) + " |",
           "|---|---|---|" + "---|" * (len(rows[0]) - 4)]
    for r in group:
        md.append(f"| {r['#']} | {r.get('Title', '')} | {r.get('Assignees', '')} | "
                  + " | ".join(r[k] for k in r if k not in ("#", "Title", "Assignees", "Status")) + " |")
    md.append("")
md += ["## Visões (views) do board", ""]
for v in blocks.get("memex-views", []):
    md.append(f"- **{v.get('name')}** ({v.get('layout')})")
(out / "BOARD.md").write_text("\n".join(md), encoding="utf-8")
print(f"{title}: {len(rows)} itens, {len(cols)} campos, {len(blocks.get('memex-views', []))} visões")
for r in rows:
    print(" ", r["#"], "|", r.get("Status", ""), "|", r.get("Title", ""), "|", r.get("Assignees", ""))
