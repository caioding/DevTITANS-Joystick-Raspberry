"""Exporta issues, comentários, labels e milestones de um repositório público do GitHub (API REST, sem login).

Uso: python exportar_issues.py OWNER/REPO PASTA_SAIDA
Gera: issues.json, comentarios.json, labels.json, milestones.json e ISSUES.md (versão legível).
"""
import json
import sys
import urllib.request
from pathlib import Path

repo, out = sys.argv[1], Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
API = f"https://api.github.com/repos/{repo}"


def get_all(path):
    items, page = [], 1
    while True:
        sep = "&" if "?" in path else "?"
        req = urllib.request.Request(f"{API}{path}{sep}per_page=100&page={page}",
                                     headers={"Accept": "application/vnd.github+json", "User-Agent": "backup-script"})
        with urllib.request.urlopen(req) as r:
            batch = json.load(r)
        items += batch
        if len(batch) < 100:
            return items
        page += 1


issues = get_all("/issues?state=all&direction=asc")
comments = get_all("/issues/comments?direction=asc")
labels = get_all("/labels")
milestones = get_all("/milestones?state=all")

for name, data in (("issues", issues), ("comentarios", comments), ("labels", labels), ("milestones", milestones)):
    (out / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

by_issue = {}
for c in comments:
    by_issue.setdefault(c["issue_url"].rsplit("/", 1)[1], []).append(c)

md = [f"# Issues de {repo}", "", f"Exportado da API do GitHub. {len(issues)} itens, {len(comments)} comentários.", ""]
for i in issues:
    kind = "PR" if "pull_request" in i else "Issue"
    md += [f"## #{i['number']} {i['title']}", "",
           f"- {kind}, estado: **{i['state']}**, criada por @{i['user']['login']} em {i['created_at'][:10]}"
           + (f", fechada em {i['closed_at'][:10]}" if i.get("closed_at") else ""),
           f"- Labels: {', '.join(l['name'] for l in i['labels']) or '—'}",
           f"- Responsáveis: {', '.join('@' + a['login'] for a in i['assignees']) or '—'}",
           f"- Milestone: {i['milestone']['title'] if i.get('milestone') else '—'}",
           f"- Original: {i['html_url']}", "", (i.get("body") or "_(sem descrição)_").strip(), ""]
    for c in by_issue.get(str(i["number"]), []):
        md += [f"> **@{c['user']['login']}** em {c['created_at'][:10]}:", ">",
               *["> " + line for line in (c.get("body") or "").splitlines()], ""]
(out / "ISSUES.md").write_text("\n".join(md), encoding="utf-8")

prs = sum("pull_request" in i for i in issues)
print(f"issues: {len(issues) - prs}  PRs: {prs}  comentários: {len(comments)}  labels: {len(labels)}  "
      f"milestones: {len(milestones)}  abertas: {sum(i['state'] == 'open' for i in issues)}")
