"""Gabarito do Desafio B: Tela de abertura de chamado no GLPI (15 itens)."""
from comum import Pagina, hex_rgb, normal, perto, recursos_externos, rgb, rodar_itens, verde, vermelho

ITENS = [
    (1, "Título e subtítulo com o texto exato"),
    (2, "Nome e matrícula travados, sem edição"),
    (3, "Sistema: SEI, SIGEPE e GLPI, nessa ordem"),
    (4, "Tipo de acesso em botões de opção, só Leitura e Escrita"),
    (5, "Asterisco vermelho nos três campos obrigatórios"),
    (6, "Justificativa escondida com Leitura"),
    (7, "Justificativa aparece ao escolher Escrita"),
    (8, "Contador “0/20” atualiza ao digitar"),
    (9, "Contador fica verde ao chegar em 20"),
    (10, "“Campo obrigatório” embaixo de cada campo vazio"),
    (11, "Nenhum alerta do navegador"),
    (12, "Resumo com os dados escolhidos"),
    (13, "“Voltar e editar” preserva os dados"),
    (14, "Mensagem final exata, com o número do chamado"),
    (15, "Arquivo único, sem bibliotecas externas, com as cores da Positivo"),
]

JUSTIFICATIVA = "Preciso editar processos do meu setor"


def avaliar(browser, arquivo):
    p = Pagina(browser, arquivo)
    html = arquivo.read_text(encoding="utf-8", errors="replace")
    pg = p.page

    def travado(testid):
        return p.el(testid).evaluate(
            """e => { const tag = e.tagName;
                if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return e.disabled || e.readOnly;
                return !e.isContentEditable && !e.querySelector('input:not([disabled]):not([readonly]),textarea:not([disabled]):not([readonly])'); }""")

    def valor_ou_texto(testid):
        return normal(p.el(testid).evaluate("e => ('value' in e && e.value) ? e.value : e.innerText"))

    def i1():
        t, s = p.texto("titulo"), p.texto("subtitulo")
        ok = "Solicitação de acesso a sistema" in t and "Seus dados já foram preenchidos pelo login" in s
        return ok, f"título “{t}” · subtítulo “{s}”"

    def i2():
        n, m = valor_ou_texto("nome"), valor_ou_texto("matricula")
        ok = "Marina Souza" in n and "48213" in m and travado("nome") and travado("matricula")
        return ok, f"nome “{n}”, matrícula “{m}”"

    def i3():
        opcoes = p.el("campo-sistema").evaluate(
            "s => [...s.options].filter(o => o.value !== '' && !o.disabled).map(o => o.text.trim())")
        return opcoes == ["SEI", "SIGEPE", "GLPI"], f"opções: {opcoes}"

    def i4():
        info = [p.el(t).evaluate("e => [e.tagName, e.type, e.name]") for t in ("opcao-leitura", "opcao-escrita")]
        ok = all(i[0] == "INPUT" and i[1] == "radio" for i in info) and info[0][2] and info[0][2] == info[1][2]
        total = pg.locator(f'input[type="radio"][name="{info[0][2]}"]').count() if ok else 0
        ok = ok and total == 2
        return ok, f"{total} opções no grupo" if info[0][2] else f"{info}"

    def i5():
        loc = pg.locator('[data-testid="asterisco"]')
        cores = [rgb(loc.nth(k).evaluate("e => getComputedStyle(e).color")) for k in range(loc.count())]
        ok = len(cores) >= 3 and all(vermelho(c) for c in cores)
        return ok, f"{len(cores)} asteriscos, cores {cores[:3]}"

    def i6():
        antes = p.visivel("campo-justificativa")
        p.el("opcao-leitura").check()
        depois = p.visivel("campo-justificativa")
        return not antes and not depois, f"visível no início: {antes}; com Leitura: {depois}"

    def i7():
        p.el("opcao-escrita").check()
        pg.wait_for_timeout(150)
        return p.visivel("campo-justificativa"), "aparece com Escrita" if p.visivel("campo-justificativa") else "não aparece"

    def i8():
        inicial = p.texto("contador")
        p.el("campo-justificativa").fill("abcde")
        pg.wait_for_timeout(100)
        depois = p.texto("contador")
        return "0/20" in inicial.replace(" ", "") and "5/20" in depois.replace(" ", ""), f"início “{inicial}”, com 5 letras “{depois}”"

    def i9():
        p.el("campo-justificativa").fill("a" * 19)
        pg.wait_for_timeout(100)
        c19 = rgb(p.el("contador").evaluate("e => getComputedStyle(e).color"))
        p.el("campo-justificativa").fill("a" * 20)
        pg.wait_for_timeout(100)
        c20 = rgb(p.el("contador").evaluate("e => getComputedStyle(e).color"))
        return verde(c20) and c19 != c20, f"19 letras {c19} → 20 letras {c20}"

    def i10():
        p.carregar()
        p.el("btn-continuar").click()
        pg.wait_for_timeout(200)
        vazios = {t: (p.visivel(t), p.texto(t)) for t in ("erro-sistema", "erro-tipo")}
        p.el("opcao-escrita").check()
        p.el("btn-continuar").click()
        pg.wait_for_timeout(200)
        vazios["erro-justificativa"] = (p.visivel("erro-justificativa"), p.texto("erro-justificativa"))
        ok = all(v and "Campo obrigatório" in t for v, t in vazios.values())
        cores_ok = all(vermelho(rgb(p.el(t).evaluate("e => getComputedStyle(e).color"))) for t in vazios if p.existe(t))
        faltando = [t for t, (v, tx) in vazios.items() if not (v and "Campo obrigatório" in tx)]
        return ok and cores_ok, "todas as mensagens em vermelho" if ok and cores_ok else f"problemas em: {faltando or 'cor das mensagens'}"

    def preencher_e_continuar():
        p.carregar()
        p.el("campo-sistema").select_option(label="SIGEPE")
        p.el("opcao-escrita").check()
        pg.wait_for_timeout(100)
        p.el("campo-justificativa").fill(JUSTIFICATIVA)
        p.el("btn-continuar").click()
        pg.wait_for_timeout(250)

    def i12():
        preencher_e_continuar()
        if not p.visivel("resumo"):
            return False, "resumo não apareceu"
        t = p.texto("resumo")
        faltam = [x for x in ("SIGEPE", "Escrita", JUSTIFICATIVA) if x not in t]
        return not faltam, "resumo completo" if not faltam else f"faltam no resumo: {faltam}"

    def i13():
        if not p.visivel("btn-voltar"):
            preencher_e_continuar()
        p.el("btn-voltar").click()
        pg.wait_for_timeout(250)
        sistema = p.el("campo-sistema").evaluate("s => s.options[s.selectedIndex] ? s.options[s.selectedIndex].text.trim() : ''")
        escrita = p.el("opcao-escrita").is_checked()
        just = p.el("campo-justificativa").input_value() if p.visivel("campo-justificativa") else ""
        ok = sistema == "SIGEPE" and escrita and just == JUSTIFICATIVA
        return ok, f"sistema “{sistema}”, escrita {escrita}, justificativa {'preservada' if just == JUSTIFICATIVA else 'perdida'}"

    def i14():
        preencher_e_continuar()
        p.el("btn-abrir").click()
        pg.wait_for_timeout(250)
        t = p.texto("mensagem-sucesso")
        return p.visivel("mensagem-sucesso") and "Chamado #2026-00412 aberto com sucesso" in t, f"mensagem: “{t}”"

    def i11():
        return p.dialogos == 0, f"{p.dialogos} alerta(s) do navegador durante os testes"

    def i15():
        p.carregar()
        ext = recursos_externos(html) or p.requisicoes_externas
        cores = p.todas_cores()
        marca = any(perto(c, hex_rgb("2C2A29")) or perto(c, hex_rgb("3CDBC0")) for c in cores)
        return not ext and marca, ("recursos externos encontrados" if ext else "sem dependências") + ("; usa as cores da Positivo" if marca else "; cores da Positivo ausentes")

    funcs = [i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i12, i13, i14, i11, i15]
    ordem = [ITENS[k] for k in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 10, 14)]
    res = rodar_itens(ordem, funcs)
    res.sort(key=lambda r: r.item)
    p.carregar()
    return res, p
