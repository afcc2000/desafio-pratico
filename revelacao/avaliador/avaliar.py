"""Avalia as saídas das equipes contra o gabarito de 15 itens e gera o placar.

Uso:
    python avaliador/avaliar.py                  # avalia equipes/ da branch atual
    python avaliador/avaliar.py --branches       # avalia todas as branches origin/equipe/*
    python avaliador/avaliar.py --arquivo x.html --desafio A   # testa um HTML solto

Gera em resultados/: <equipe>.json, <equipe>.md (texto do comentário no PR),
screenshots, PLACAR.md e placar.html.
"""
import argparse
import base64
import html as h
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checks_a  # noqa: E402
import checks_b  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "resultados"
CHECKS = {"A": checks_a, "B": checks_b}
NOMES = {"A": "Painel da Estella", "B": "Chamado no GLPI"}


def git(*args, cwd=RAIZ):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def avaliar_html(browser, arquivo, desafio, png=None):
    res, pagina = CHECKS[desafio].avaliar(browser, arquivo)
    if png:
        pagina.page.screenshot(path=str(png))
    pagina.fechar()
    return res


def avaliar_equipe(browser, pasta, origem):
    info = json.loads((pasta / "equipe.json").read_text(encoding="utf-8"))
    nome, desafio = info.get("equipe") or pasta.name, (info.get("desafio") or "").upper()
    dados = {"equipe": nome, "desafio": desafio, "integrantes": info.get("integrantes", []), "origem": origem, "versoes": {}}
    if desafio not in CHECKS:
        dados["erro"] = "equipe.json sem desafio A ou B"
        return dados
    destino = SAIDA / nome
    destino.mkdir(parents=True, exist_ok=True)
    for v in ("v1", "v2"):
        html_v = pasta / "saida" / v / "index.html"
        exec_json = pasta / "saida" / v / "execucao.json"
        if not html_v.exists() and not exec_json.exists():
            continue
        registro = json.loads(exec_json.read_text(encoding="utf-8")) if exec_json.exists() else {}
        if not html_v.exists():
            dados["versoes"][v] = {"nota": 0, "itens": [], "registro": registro, "erro": "a execução não gerou HTML"}
            continue
        png = destino / f"{v}.png"
        res = avaliar_html(browser, html_v, desafio, png)
        dados["versoes"][v] = {
            "nota": sum(r.ok for r in res),
            "itens": [r.__dict__ for r in res],
            "registro": registro,
            "screenshot": f"{nome}/{v}.png",
        }
    v1, v2 = dados["versoes"].get("v1"), dados["versoes"].get("v2")
    if v1 and v2 and v1["itens"] and v2["itens"]:
        dados["regressoes"] = [a["item"] for a, b in zip(v1["itens"], v2["itens"]) if a["ok"] and not b["ok"]]
        dados["melhorias"] = [a["item"] for a, b in zip(v1["itens"], v2["itens"]) if not a["ok"] and b["ok"]]
    return dados


def comentario(d):
    """Texto em Markdown para o comentário no Pull Request."""
    linhas = [f"## Avaliação · equipe `{d['equipe']}` · Desafio {d['desafio']} ({NOMES.get(d['desafio'], '?')})", ""]
    if d.get("erro"):
        return "\n".join(linhas + [f"⚠️ {d['erro']}"])
    vs = [v for v in ("v1", "v2") if v in d["versoes"]]
    if not vs:
        return "\n".join(linhas + ["Ainda não há saída para avaliar."])
    linhas.append("| Versão | Nota | Duração | Briefing colado |")
    linhas.append("| --- | --- | --- | --- |")
    for v in vs:
        r = d["versoes"][v].get("registro", {})
        linhas.append(f"| {v} | **{d['versoes'][v]['nota']}/15** | {r.get('duracao_s', '?')} s | {r.get('briefing_colado_pct', '?')}% |")
    linhas += ["", "| # | Item | " + " | ".join(vs) + " |", "| --- | --- | " + " | ".join("---" for _ in vs) + " |"]
    base = next((d["versoes"][v]["itens"] for v in vs if d["versoes"][v]["itens"]), [])
    for k, item in enumerate(base):
        marcas = []
        for v in vs:
            its = d["versoes"][v]["itens"]
            if not its:
                marcas.append("—")
                continue
            r = its[k]
            marca = "✅" if r["ok"] else "❌"
            if v == "v2" and k + 1 in d.get("regressoes", []):
                marca = "🔻 quebrou"
            marcas.append(f"{marca} <sub>{h.escape(r['detalhe'])}</sub>")
        linhas.append(f"| {item['item']} | {h.escape(item['descricao'])} | " + " | ".join(marcas) + " |")
    if "regressoes" in d:
        linhas += ["", f"**Rodada 2:** {len(d['melhorias'])} item(ns) melhoraram e {len(d['regressoes'])} quebraram."]
        if d["regressoes"]:
            linhas.append("Itens que passavam na v1 e falharam na v2 são **prompt drift**: é o que o STRAGO existe para evitar.")
    return "\n".join(linhas)


def placar(todas):
    ordem = sorted(todas, key=lambda d: (-max([v["nota"] for v in d["versoes"].values()] or [0]), d["equipe"]))
    md = ["# Placar do desafio", "", "| Equipe | Desafio | v1 | v2 | Melhoraram | Quebraram |", "| --- | --- | --- | --- | --- | --- |"]
    for d in ordem:
        v1 = d["versoes"].get("v1", {}).get("nota", "—")
        v2 = d["versoes"].get("v2", {}).get("nota", "—")
        md.append(f"| {d['equipe']} | {d['desafio']} | {v1} | {v2} | {len(d.get('melhorias', [])) if 'melhorias' in d else '—'} | {len(d.get('regressoes', [])) if 'regressoes' in d else '—'} |")
    # Itens que mais falharam por desafio
    for des in ("A", "B"):
        cont = {}
        for d in todas:
            if d["desafio"] != des or "v1" not in d["versoes"]:
                continue
            for it in d["versoes"]["v1"]["itens"]:
                if not it["ok"]:
                    cont[it["descricao"]] = cont.get(it["descricao"], 0) + 1
        if cont:
            md += ["", f"### Desafio {des}: itens que mais falharam na v1", ""]
            md += [f"- {n}× {desc}" for desc, n in sorted(cont.items(), key=lambda kv: -kv[1])[:5]]
    (SAIDA / "PLACAR.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    cards = []
    for d in ordem:
        imgs = ""
        for v in ("v1", "v2"):
            ver = d["versoes"].get(v)
            if not ver:
                continue
            png = SAIDA / ver.get("screenshot", "x")
            src = "data:image/png;base64," + base64.b64encode(png.read_bytes()).decode() if png.exists() else ""
            imgs += f'<figure><img src="{src}" alt="{v}"><figcaption>{v} · <b>{ver["nota"]}/15</b></figcaption></figure>'
        quebrou = f'<p class="q">{len(d["regressoes"])} item(ns) quebraram na v2</p>' if d.get("regressoes") else ""
        cards.append(f'<section><h2>{h.escape(d["equipe"])} <span>Desafio {d["desafio"]}</span></h2>{quebrou}<div class="imgs">{imgs}</div></section>')
    pagina = f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Placar do desafio</title>
<style>body{{background:#2C2A29;color:#EDEDEA;font-family:Montserrat,Arial,sans-serif;margin:32px}}h1{{color:#3CDBC0}}
section{{background:#1F1E1D;border-radius:12px;padding:20px;margin:16px 0}}h2 span{{font-size:16px;color:#A7A8AA}}
.imgs{{display:flex;gap:16px;flex-wrap:wrap}}figure{{margin:0}}img{{width:560px;border:1px solid #53565A;border-radius:8px}}
figcaption{{margin-top:6px}}.q{{color:#FF8A80}}</style><h1>Placar do desafio</h1>{''.join(cards)}</html>"""
    (SAIDA / "placar.html").write_text(pagina, encoding="utf-8")


def pastas_das_branches():
    """Cria um worktree para cada branch origin/equipe/* e devolve as pastas de equipe."""
    git("fetch", "--all", "--prune")
    refs = [r for r in git("for-each-ref", "--format=%(refname:short)", "refs/remotes/origin/equipe/").stdout.split() if r]
    base = Path(tempfile.mkdtemp(prefix="avaliacao-"))
    pastas = []
    for ref in refs:
        wt = base / ref.replace("/", "_")
        if git("worktree", "add", "--detach", str(wt), ref).returncode != 0:
            continue
        # Cada branch equipe/<nome> é avaliada só pela pasta equipes/<nome>
        p = wt / "equipes" / ref.split("/", 2)[-1]
        if p.is_dir() and (p / "equipe.json").exists():
            pastas.append((p, ref))
    return pastas, base


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--branches", action="store_true")
    ap.add_argument("--arquivo")
    ap.add_argument("--desafio")
    a = ap.parse_args()

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        if a.arquivo:
            res = avaliar_html(browser, Path(a.arquivo), a.desafio.upper())
            for r in res:
                print(f"{'OK ' if r.ok else 'X  '} {r.item:>2}. {r.descricao}  — {r.detalhe}")
            print(f"\nNota: {sum(r.ok for r in res)}/15")
            return
        if SAIDA.exists():
            shutil.rmtree(SAIDA)
        SAIDA.mkdir()
        if a.branches:
            pastas, base = pastas_das_branches()
        else:
            pastas = [(p, "local") for p in sorted((RAIZ / "equipes").glob("*"))
                      if p.is_dir() and not p.name.startswith("_") and (p / "equipe.json").exists()]
            base = None
        todas = []
        for pasta, origem in pastas:
            d = avaliar_equipe(browser, pasta, origem)
            todas.append(d)
            (SAIDA / f"{d['equipe']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            (SAIDA / f"{d['equipe']}.md").write_text(comentario(d), encoding="utf-8")
            notas = ", ".join(f"{v} {x['nota']}/15" for v, x in d["versoes"].items()) or d.get("erro", "sem saída")
            print(f"{d['equipe']:<25} Desafio {d['desafio']}  {notas}")
        browser.close()
    placar(todas)
    if base:
        shutil.rmtree(base, ignore_errors=True)
        git("worktree", "prune")
    print(f"\n{len(todas)} equipe(s) avaliada(s). Placar em resultados/PLACAR.md e resultados/placar.html")


if __name__ == "__main__":
    main()
