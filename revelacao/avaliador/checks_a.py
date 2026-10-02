"""Gabarito do Desafio A: Painel de monitoramento da Estella (15 itens)."""
from comum import JS_COR, Pagina, hex_rgb, normal, perto, recursos_externos, rgb, rodar_itens, vermelho

ITENS = [
    (1, "Título exato “Estella · Painel de Setembro”"),
    (2, "“Atualizado em 30/09/2026 18:00” à direita do título"),
    (3, "Três cards lado a lado, na ordem pedida"),
    (4, "Valores 15.090, 78% e 22% (total de todos os órgãos, percentuais arredondados)"),
    (5, "Gráfico de barras horizontais"),
    (6, "Barras em ordem decrescente"),
    (7, "Só os 5 maiores órgãos, com os valores corretos"),
    (8, "Barra da UFBA em outra cor"),
    (9, "Tabela à direita do gráfico"),
    (10, "Tabela com as 5 conversas mais recentes e colunas Hora, Órgão, Assunto, Status"),
    (11, "Três status, cada um com uma cor"),
    (12, "Faixa vermelha de alerta visível no topo (22% > 20%)"),
    (13, "Texto exato do alerta"),
    (14, "Fundo #2C2A29 e destaque #3CDBC0"),
    (15, "Arquivo único, sem bibliotecas externas e sem rolagem em 1366×768"),
]

ORGAOS = ["cnpq", "ufba", "dnit", "capes", "mj"]
VALORES = ["3.920", "2.870", "2.410", "1.960", "1.320"]
STATUS = {"resolvido", "transbordo", "em andamento"}
EXTRAS = ["midr", "dpu", "iphan", "antaq"]
RECENTES = ["17:58", "17:51", "17:44", "17:37", "17:30"]
ANTIGAS = ["17:12", "16:55", "16:40"]


# Área real do gráfico: o menor elemento que contém todas as barras (mais robusto que confiar só no data-testid da área)
JS_AREA = """
() => { const bs = [...document.querySelectorAll('[data-testid^="barra-"]')];
  if (!bs.length) return null;
  let a = bs[0]; while (a && !bs.every(b => a.contains(b))) a = a.parentElement;
  const rs = bs.map(b => b.getBoundingClientRect());
  const x = Math.min(...rs.map(r => r.left)), r = Math.max(...rs.map(r => r.right));
  const y = Math.min(...rs.map(r => r.top)), b = Math.max(...rs.map(r => r.bottom));
  return {texto: a ? a.textContent : '', x: x, y: y, width: r - x, height: b - y}; }
"""


def avaliar(browser, arquivo):
    p = Pagina(browser, arquivo)
    html = arquivo.read_text(encoding="utf-8", errors="replace")

    def i1():
        t = p.texto("titulo")
        return t == "Estella · Painel de Setembro", f"encontrado: “{t}”" if t else "data-testid=titulo não encontrado"

    def i2():
        t, a, b = p.texto("atualizado"), p.caixa("titulo"), p.caixa("atualizado")
        if "Atualizado em 30/09/2026 18:00" not in t:
            return False, f"texto: “{t}”"
        return bool(a and b and b["x"] > a["x"] + a["width"] / 2), "texto certo; posição em relação ao título conferida"

    def i3():
        cx = [p.caixa(f"card-{n}") for n in ("atendimentos", "resolvidos", "transbordo")]
        if None in cx:
            return False, "algum card sem data-testid"
        ordem = cx[0]["x"] < cx[1]["x"] < cx[2]["x"]
        linha = max(c["y"] for c in cx) - min(c["y"] for c in cx) < 50
        return ordem and linha, f"ordem {'ok' if ordem else 'errada'}, {'mesma linha' if linha else 'não estão lado a lado'}"

    def i4():
        t = {n: p.texto(f"card-{n}").replace(" %", "%") for n in ("atendimentos", "resolvidos", "transbordo")}
        ok = "15.090" in t["atendimentos"] and "78%" in t["resolvidos"] and "22%" in t["transbordo"]
        return ok, " | ".join(t.values())

    def i5():
        cx = [p.caixa(f"barra-{o}") for o in ORGAOS]
        if None in cx:
            return False, "faltam barras com data-testid"
        return all(c["width"] > c["height"] for c in cx), "todas mais largas que altas" if all(c["width"] > c["height"] for c in cx) else "há barras verticais"

    def i6():
        cx = {o: p.caixa(f"barra-{o}") for o in ORGAOS}
        if None in cx.values():
            return False, "faltam barras"
        por_y = [o for o, _ in sorted(cx.items(), key=lambda kv: kv[1]["y"])]
        larguras = [cx[o]["width"] for o in ORGAOS]
        decresce = all(a >= b - 2 for a, b in zip(larguras, larguras[1:]))
        return por_y == ORGAOS and decresce, f"ordem na tela: {', '.join(por_y)}"

    def i7():
        area = p.page.evaluate(JS_AREA)
        t = normal((area or {}).get("texto", "")) + " " + p.texto("grafico-orgaos")
        faltam = [v for v in VALORES if v not in t and v.replace(".", "") not in t]
        sobram = [o.upper() for o in EXTRAS if o.upper() in t.upper() or p.existe(f"barra-{o}")]
        ok = not faltam and not sobram
        return ok, "5 maiores com valores certos" if ok else f"faltam: {faltam or '—'}; sobram: {sobram or '—'}"

    def i8():
        cores = {o: rgb(p.cor(f"barra-{o}")["fundo"]) for o in ORGAOS}
        ufba = cores.pop("ufba")
        ok = ufba is not None and all(c is not None and not perto(c, ufba, 10) for c in cores.values())
        return ok, f"UFBA {ufba}, demais {sorted(set(cores.values()), key=str)}"

    def i9():
        g, t = p.page.evaluate(JS_AREA) or p.caixa("grafico-orgaos"), p.caixa("tabela-conversas")
        if not g or not t:
            return False, "gráfico ou tabela sem data-testid"
        direita = t["x"] >= g["x"] + g["width"] * 0.5
        sobrepoe = t["y"] < g["y"] + g["height"] and g["y"] < t["y"] + t["height"]
        return direita and sobrepoe, "lado a lado" if direita and sobrepoe else "não está à direita do gráfico"

    def i10():
        dados = p.el("tabela-conversas").evaluate(
            """t => { const rows=[...t.querySelectorAll('tr')];
                 return {cab: [...rows[0].children].map(c=>c.textContent.trim()),
                         linhas: rows.slice(1).filter(r=>r.querySelector('td')).length}; }""")
        cab = [normal(c) for c in dados["cab"]]
        t = p.texto("tabela-conversas")
        recentes = all(h in t for h in RECENTES) and not any(h in t for h in ANTIGAS)
        ok = cab == ["Hora", "Órgão", "Assunto", "Status"] and dados["linhas"] == 5 and recentes
        return ok, f"colunas {cab}, {dados['linhas']} linhas, {'as 5 mais recentes' if recentes else 'não são as 5 mais recentes'}"

    def i11():
        loc = p.page.locator('[data-testid="status"]')
        vistos = {}
        for k in range(loc.count()):
            nome = normal(loc.nth(k).text_content()).lower()
            c = loc.nth(k).evaluate(JS_COR)
            vistos.setdefault(nome, set()).add((rgb(c["fundo"]), rgb(c["texto"])))
        nomes_ok = set(vistos) == STATUS
        assinaturas = [next(iter(v)) for v in vistos.values()]
        distintas = len(set(assinaturas)) == len(assinaturas)
        return nomes_ok and distintas, f"status: {sorted(vistos)}; cores {'distintas' if distintas else 'repetidas'}"

    def i12():
        if not p.visivel("alerta-transbordo"):
            return False, "alerta não visível"
        c = p.cor("alerta-transbordo")
        cor = rgb(c["fundo"]) or rgb(c["borda"]) or rgb(c["texto"])
        topo = p.caixa("alerta-transbordo")["y"] < p.caixa("card-atendimentos")["y"] if p.existe("card-atendimentos") else True
        return vermelho(cor) and topo, f"cor {cor}, {'acima dos cards' if topo else 'não está no topo'}"

    def i13():
        t = p.texto("alerta-transbordo")
        return "Transbordo acima da meta de 20%" in t, f"texto: “{t}”"

    def i14():
        fundo = rgb(p.page.evaluate("getComputedStyle(document.body).backgroundColor")) or \
            rgb(p.page.evaluate("getComputedStyle(document.documentElement).backgroundColor"))
        cores = p.todas_cores()
        f_ok = perto(fundo, hex_rgb("2C2A29")) or any(perto(c, hex_rgb("2C2A29")) for c in cores)
        d_ok = any(perto(c, hex_rgb("3CDBC0")) for c in cores)
        return f_ok and d_ok, f"fundo {fundo}; #3CDBC0 {'presente' if d_ok else 'ausente'}"

    def i15():
        ext = recursos_externos(html) or p.requisicoes_externas
        dims = p.page.evaluate("[document.documentElement.scrollWidth, document.documentElement.scrollHeight, innerWidth, innerHeight]")
        rolagem = dims[0] > dims[2] + 1 or dims[1] > dims[3] + 1
        return not ext and not rolagem, ("recursos externos encontrados" if ext else "sem dependências") + ("; tem rolagem" if rolagem else "; sem rolagem")

    res = rodar_itens(ITENS, [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15])
    return res, p
