"""Publica a avaliação de cada equipe como comentário no Pull Request da branch equipe/<nome>.

Usa o GitHub CLI (gh), que já vem instalado nos runners do GitHub Actions.
Se a variável PR_NUMBER existir (evento pull_request), comenta só naquele PR.
"""
import json
import os
import subprocess
from pathlib import Path

SAIDA = Path(__file__).resolve().parent.parent / "resultados"


def gh(*args):
    return subprocess.run(["gh", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")


def main():
    pr_fixo = os.environ.get("PR_NUMBER")
    for md in sorted(SAIDA.glob("*.md")):
        if md.name == "PLACAR.md":
            continue
        equipe = md.stem
        numero = pr_fixo
        if not numero:
            r = gh("pr", "list", "--head", f"equipe/{equipe}", "--state", "open", "--json", "number")
            prs = json.loads(r.stdout or "[]")
            if not prs:
                print(f"{equipe}: sem PR aberto, pulei")
                continue
            numero = str(prs[0]["number"])
        r = gh("pr", "comment", numero, "--body-file", str(md))
        print(f"{equipe}: comentário no PR #{numero} {'ok' if r.returncode == 0 else 'falhou: ' + r.stderr.strip()}")


if __name__ == "__main__":
    main()
