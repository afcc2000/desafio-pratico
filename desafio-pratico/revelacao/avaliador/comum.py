"""Funções compartilhadas pelos checks dos desafios A e B."""
import re
from dataclasses import dataclass

VIEWPORT = {"width": 1366, "height": 768}

# Lê a cor "efetiva" de um elemento: fundo, depois preenchimento SVG, depois o primeiro descendente pintado.
JS_COR = """
(el) => {
  const vazio = c => !c || c === 'none' || c === 'transparent' || /rgba\\(0, 0, 0, 0\\)/.test(c);
  const pick = e => {
    const s = getComputedStyle(e);
    if (!vazio(s.backgroundColor)) return s.backgroundColor;
    if (!vazio(s.fill) && e instanceof SVGElement) return s.fill;
    const g = s.backgroundImage.match(/rgba?\\([^)]+\\)/);
    if (g) return g[0];
    return null;
  };
  let c = pick(el);
  if (!c) for (const d of el.querySelectorAll('*')) { c = pick(d); if (c) break; }
  return { fundo: c, texto: getComputedStyle(el).color, borda: getComputedStyle(el).borderTopColor };
}
"""

# Lista todas as cores usadas na página (texto, fundo, borda, fill, stroke).
JS_TODAS_CORES = """
() => {
  const out = new Set();
  for (const e of document.querySelectorAll('*')) {
    const s = getComputedStyle(e);
    [s.color, s.backgroundColor, s.borderTopColor, s.borderLeftColor, s.fill, s.stroke].forEach(c => c && out.add(c));
    (s.backgroundImage.match(/rgba?\\([^)]+\\)/g) || []).forEach(c => out.add(c));
  }
  return [...out];
}
"""


@dataclass
class Resultado:
    item: int
    descricao: str
    ok: bool
    detalhe: str = ""


def rgb(texto):
    """'rgb(44, 42, 41)' -> (44, 42, 41). Retorna None se não houver cor."""
    if not texto:
        return None
    m = re.search(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:[,\s/]+([\d.]+))?", texto)
    if not m:
        return None
    if m.group(4) is not None and float(m.group(4)) == 0:
        return None
    return tuple(round(float(x)) for x in m.groups()[:3])


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def perto(a, b, tol=6):
    return a is not None and b is not None and all(abs(x - y) <= tol for x, y in zip(a, b))


def vermelho(c):
    return c is not None and c[0] >= 150 and c[1] <= 120 and c[2] <= 120


def verde(c):
    return c is not None and c[1] >= 110 and c[1] > c[0] + 40 and c[1] > c[2] + 40


def normal(t):
    return re.sub(r"\s+", " ", (t or "").replace(" ", " ")).strip()


def recursos_externos(html):
    padroes = [r"<script[^>]+src\s*=", r"<link[^>]+href\s*=\s*[\"']?(https?:)?//", r"@import", r"url\(\s*[\"']?(https?:)?//"]
    return [p for p in padroes if re.search(p, html, re.I)]


class Pagina:
    """Abre o HTML e oferece atalhos por data-testid."""

    def __init__(self, browser, caminho):
        self.caminho = caminho
        self.dialogos = 0
        self.requisicoes_externas = []
        self.ctx = browser.new_context(viewport=VIEWPORT)
        self.page = self.ctx.new_page()
        self.page.set_default_timeout(2500)
        self.page.on("dialog", self._dialogo)
        self.page.on("request", self._requisicao)
        self.carregar()

    def _dialogo(self, d):
        self.dialogos += 1
        d.dismiss()

    def _requisicao(self, r):
        if r.url.startswith("http"):
            self.requisicoes_externas.append(r.url)

    def carregar(self):
        self.page.goto(self.caminho.resolve().as_uri(), wait_until="load", timeout=15000)
        self.page.wait_for_timeout(400)

    def el(self, testid):
        return self.page.locator(f'[data-testid="{testid}"]').first

    def existe(self, testid):
        return self.page.locator(f'[data-testid="{testid}"]').count() > 0

    def texto(self, testid):
        return normal(self.el(testid).text_content(timeout=2000)) if self.existe(testid) else ""

    def caixa(self, testid):
        return self.el(testid).bounding_box(timeout=2000) if self.existe(testid) else None

    def visivel(self, testid):
        return self.existe(testid) and self.el(testid).is_visible()

    def cor(self, testid):
        return self.el(testid).evaluate(JS_COR)

    def todas_cores(self):
        return {rgb(c) for c in self.page.evaluate(JS_TODAS_CORES)} - {None}

    def fechar(self):
        self.ctx.close()


def rodar_itens(itens, funcoes):
    """Executa cada check isoladamente: uma falha não derruba os outros."""
    resultados = []
    for (n, desc), f in zip(itens, funcoes):
        try:
            ok, det = f()
        except Exception as e:  # noqa: BLE001
            msg = str(e).splitlines()[0]
            if "Timeout" in msg:
                det = "elemento do contrato de QA não encontrado ou não interagível (confira os data-testid)"
            else:
                det = f"erro ao conferir: {msg[:160]}"
            ok = False
        resultados.append(Resultado(n, desc, bool(ok), det))
    return resultados
