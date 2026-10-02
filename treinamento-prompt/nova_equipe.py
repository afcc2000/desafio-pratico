"""Cria a pasta e a branch de uma equipe.

Uso:
    python nova_equipe.py <nome-da-equipe> <A|B>

Exemplo:
    python nova_equipe.py ana-e-bruno A
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[2].upper() not in ("A", "B"):
        print(__doc__)
        sys.exit(1)
    nome, desafio = sys.argv[1].lower(), sys.argv[2].upper()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", nome):
        print("Use só letras minúsculas, números e hífen no nome da equipe (ex.: ana-e-bruno).")
        sys.exit(1)
    destino = RAIZ / "equipes" / nome
    if destino.exists():
        print(f"A equipe '{nome}' já existe.")
        sys.exit(1)

    r = git("checkout", "-b", f"equipe/{nome}")
    if r.returncode != 0:
        print(f"Não consegui criar a branch equipe/{nome}:\n{r.stderr}")
        sys.exit(1)

    shutil.copytree(RAIZ / "equipes" / "_modelo", destino)
    info = json.loads((destino / "equipe.json").read_text(encoding="utf-8"))
    info.update({"equipe": nome, "desafio": desafio})
    (destino / "equipe.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

    git("add", destino.relative_to(RAIZ).as_posix())
    git("commit", "-m", f"{nome}: cria equipe (desafio {desafio})")
    briefing = "desafios/A-painel-estella/" if desafio == "A" else "desafios/B-chamado-glpi/"
    print(f"""
Equipe '{nome}' criada na branch equipe/{nome} (desafio {desafio}).

Próximos passos:
  1. Leia o material do cliente na pasta {briefing} (comece pelo LEIA-ME.md)
  2. Coloque os nomes da dupla em equipes/{nome}/equipe.json
  3. Escreva o prompt em equipes/{nome}/prompts/v1.md
  4. git add equipes/{nome} && git commit -m "{nome}: prompt v1"
  5. python executar.py {nome} v1
  6. git push -u origin equipe/{nome}  e avise o instrutor
""")


if __name__ == "__main__":
    main()
