"""Executa o prompt de uma equipe UMA única vez no Claude Code, isolado do repositório.

Uso:
    python executar.py --verificar          # testa se o ambiente está pronto
    python executar.py <equipe> v1          # roda prompts/v1.md da equipe
    python executar.py <equipe> v2          # rodada 2

O que o script garante:
  * o prompt precisa estar commitado antes de rodar (o histórico prova que ele veio primeiro);
  * o Claude Code roda numa pasta temporária vazia: não enxerga o briefing nem o resto do repositório;
  * a execução é não interativa (claude -p): não há como corrigir pelo chat;
  * se a saída daquela versão já existir, o script se recusa a rodar de novo.
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
MARCADOR_MODELO = "APAGUE ESTA LINHA"
TIMEOUT_S = 900
LIMITE_CARACTERES = 2000
# Mesmo modelo para todas as equipes, para a comparação ser justa.
MODELO = "sonnet"

# Instrução fixa, igual para todas as equipes, acrescentada ao final do prompt.
SUFIXO = (
    "\n\n---\n"
    "[Instrução fixa do executor, igual para todas as equipes] "
    "Salve o resultado final como um único arquivo chamado index.html na pasta atual. "
    "Não faça perguntas: ninguém vai responder durante a execução."
)

# Flags do Claude Code em modo não interativo:
#   -p                         executa um prompt e sai (sem chat)
#   --model sonnet             mesmo modelo para todas as equipes
#   --permission-mode acceptEdits  permite criar/editar arquivos sem pedir aprovação
#   --tools Read,Write,Edit    só ferramentas de arquivo; sem terminal (Bash)
#   --setting-sources project  ignora configurações pessoais (~/.claude); a pasta temporária não tem projeto
#   --output-format json       devolve custo, duração e sessão para o registro
FLAGS = ["-p", "--model", MODELO, "--permission-mode", "acceptEdits", "--tools", "Read,Write,Edit",
         "--setting-sources", "project", "--output-format", "json"]


def erro(msg: str) -> None:
    print(f"\n[ERRO] {msg}\n")
    sys.exit(1)


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")


def achar_claude() -> str:
    caminho = shutil.which("claude")
    if not caminho:
        erro("Não encontrei o comando 'claude'. Instale o Claude Code e confira se ele abre no terminal com: claude --version")
    return caminho


def rodar_claude(prompt: str, pasta: Path) -> dict:
    cmd = [achar_claude(), *FLAGS]
    inicio = time.time()
    proc = subprocess.run(
        cmd, input=prompt, cwd=pasta, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=TIMEOUT_S,
    )
    duracao = round(time.time() - inicio, 1)
    if proc.returncode != 0:
        erro(f"O Claude Code terminou com erro (código {proc.returncode}).\n{proc.stderr.strip()[:2000]}")
    try:
        dados = json.loads(proc.stdout)
    except json.JSONDecodeError:
        dados = {"result": proc.stdout}
    dados["_duracao_s"] = duracao
    return dados


def recuperar_html(pasta: Path, dados: dict) -> str | None:
    alvo = pasta / "index.html"
    if alvo.exists():
        return alvo.read_text(encoding="utf-8", errors="replace")
    outros = sorted(pasta.rglob("*.html"))
    if outros:
        return outros[0].read_text(encoding="utf-8", errors="replace")
    m = re.search(r"```html\s*(.*?)```", str(dados.get("result", "")), re.S | re.I)
    return m.group(1) if m else None


def pct_briefing_colado(pasta_equipe: Path, prompt: str) -> int | None:
    """Percentual das frases do briefing que aparecem literalmente no prompt (só para registro)."""
    try:
        desafio = json.loads((pasta_equipe / "equipe.json").read_text(encoding="utf-8")).get("desafio")
        pasta = RAIZ / "desafios" / {"A": "A-painel-estella", "B": "B-chamado-glpi"}[desafio]
        texto = "\n".join(f.read_text(encoding="utf-8") for f in sorted(pasta.glob("*")) if f.name != "LEIA-ME.md")
    except Exception:
        return None
    limpa = lambda t: re.sub(r"\s+", " ", re.sub(r"[*`>#|]", "", t)).strip().lower()
    pedacos = []
    for linha in texto.splitlines():
        pedacos += re.split(r"(?<=[.!?;])\s+", linha)
    frases = [limpa(f) for f in pedacos if len(limpa(f)) > 40]
    alvo = limpa(prompt)
    return round(100 * sum(f in alvo for f in frases) / len(frases)) if frases else None


def verificar() -> None:
    print("Verificando o ambiente...")
    if sys.version_info < (3, 10):
        erro("Use Python 3.10 ou mais novo.")
    print(f"  Python {sys.version.split()[0]} ok")
    if git("--version").returncode != 0:
        erro("Git não encontrado.")
    print("  Git ok")
    claude = achar_claude()
    v = subprocess.run([claude, "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(f"  Claude Code {v.stdout.strip()} ok")
    with tempfile.TemporaryDirectory(prefix="desafio-teste-") as tmp:
        print("  Testando uma execução curta (leva alguns segundos)...")
        rodar_claude("Crie um arquivo chamado ok.txt contendo apenas a palavra ok.", Path(tmp))
        if not (Path(tmp) / "ok.txt").exists():
            erro("O Claude Code rodou, mas não conseguiu criar arquivo. Avise o instrutor.")
    print("\nTudo pronto para o desafio.\n")


def executar(equipe: str, versao: str) -> None:
    if versao not in ("v1", "v2"):
        erro("A versão deve ser v1 ou v2.")
    pasta_equipe = RAIZ / "equipes" / equipe
    if not pasta_equipe.is_dir() or equipe.startswith("_"):
        erro(f"Equipe '{equipe}' não encontrada em equipes/. Crie com: python nova_equipe.py <nome> <A|B>")
    arq_prompt = pasta_equipe / "prompts" / f"{versao}.md"
    prompt = arq_prompt.read_text(encoding="utf-8") if arq_prompt.exists() else ""
    if MARCADOR_MODELO in prompt or len(prompt.strip()) < 80:
        erro(f"{arq_prompt.relative_to(RAIZ)} ainda está com o modelo ou vazio. Escreva o prompt primeiro.")
    if len(prompt.strip()) > LIMITE_CARACTERES:
        erro(f"O prompt tem {len(prompt.strip())} caracteres. O limite é {LIMITE_CARACTERES}: sintetize o que realmente importa.")
    saida = pasta_equipe / "saida" / versao
    if saida.exists():
        erro(f"A saída de {versao} já existe. Vale só uma execução por versão.")
    if versao == "v2" and not (pasta_equipe / "saida" / "v1" / "index.html").exists():
        erro("Rode a v1 antes da v2.")

    rel = arq_prompt.relative_to(RAIZ).as_posix()
    if git("ls-files", "--error-unmatch", rel).returncode != 0 or git("status", "--porcelain", "--", rel).stdout.strip():
        erro(f"Faça commit do prompt antes de rodar:\n  git add {rel}\n  git commit -m \"{equipe}: prompt {versao}\"")

    print(f"Executando {rel} uma única vez, numa pasta isolada. Aguarde...")
    with tempfile.TemporaryDirectory(prefix="desafio-") as tmp:
        dados = rodar_claude(prompt + SUFIXO, Path(tmp))
        html = recuperar_html(Path(tmp), dados)

    saida.mkdir(parents=True)
    if html:
        (saida / "index.html").write_text(html, encoding="utf-8")
    registro = {
        "equipe": equipe,
        "versao": versao,
        "executado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "duracao_s": dados.get("_duracao_s"),
        "caracteres_prompt": len(prompt.strip()),
        "sha256_prompt": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "gerou_html": bool(html),
        "briefing_colado_pct": pct_briefing_colado(pasta_equipe, prompt),
        "custo_usd": dados.get("total_cost_usd"),
        "modelos": list((dados.get("modelUsage") or {}).keys()),
        "sessao": dados.get("session_id"),
        "resposta_final": str(dados.get("result", ""))[:2000],
    }
    (saida / "execucao.json").write_text(json.dumps(registro, ensure_ascii=False, indent=2), encoding="utf-8")

    git("add", saida.relative_to(RAIZ).as_posix())
    git("commit", "-m", f"{equipe}: saída {versao}")
    if not html:
        print("\nO Claude Code terminou, mas não gerou o index.html. A execução foi registrada mesmo assim.")
    else:
        print(f"\nPronto em {registro['duracao_s']}s. Abra no navegador: {(saida / 'index.html')}")
    print("A saída já foi commitada. Agora é só: git push\n")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--verificar":
        verificar()
    elif len(sys.argv) == 3:
        executar(sys.argv[1], sys.argv[2])
    else:
        print(__doc__)
