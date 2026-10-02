---
name: avaliar-equipe
description: Avalia a branch de uma equipe do desafio de engenharia de prompt contra o gabarito de 15 itens em revelacao/. Use quando o instrutor pedir para avaliar, corrigir ou dar nota a uma equipe ou branch (equipe/<nome>), ou a todas.
argument-hint: equipe/<nome> | <nome> | todas
---

# Avaliar equipe

Argumento: `$ARGUMENTS` (branch `equipe/<nome>`, só `<nome>` ou `todas`).

Repositório: raiz `desafio-pratico`. As equipes ficam em `treinamento-prompt/equipes/<nome>/` na própria branch, e o gabarito fica em `revelacao/` na `main`. **Nunca** faça checkout da branch da equipe nem commit/push na `main`: use um worktree temporário.

## 1. Buscar a branch

```bash
git fetch origin --prune
git for-each-ref --format='%(refname:short)' refs/remotes/origin/equipe/   # lista as equipes
WT="$TMP/avaliacao-<nome>"; git worktree add --detach "$WT" origin/equipe/<nome>
```

Se a branch não existir no `origin`, procure uma local `equipe/<nome>`. Se não achar nenhuma, liste as disponíveis e pare.
Com `todas`, repita os passos 1 a 6 para cada `origin/equipe/*` e no fim monte um placar.

## 2. Ler os arquivos da equipe (em `$WT/treinamento-prompt/equipes/<nome>/`)

- `equipe.json`: `desafio` (A ou B) e `integrantes`
- `prompts/v1.md`: o prompt
- `saida/v1/execucao.json`: registro da execução
- `saida/v1/index.html`: o resultado

Se não houver `saida/v1/`, a equipe ainda não executou. Informe e pare.

## 3. Integridade (mostre cada item como OK ou ⚠️)

1. `execucao.json` existe. Sem ele, o HTML não veio do `executar.py`.
2. `sha256_prompt` = SHA-256 do `prompts/v1.md` **exatamente como está no arquivo**, sem strip: `python -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],encoding='utf-8').read().encode()).hexdigest())" <v1.md>`.
3. O prompt tem no máximo 2.000 caracteres depois do strip (confira com `caracteres_prompt`).
4. `modelos` contém apenas o modelo definido em `MODELO` no `treinamento-prompt/executar.py` (hoje Sonnet).
5. Ordem no histórico, com `git -C "$WT" log --format='%h %ad %s' --date=iso -- treinamento-prompt/equipes/<nome>`: o prompt foi commitado antes do commit `<nome>: saída v1`.
6. Nenhum commit depois de `<nome>: saída v1` altera `saida/` ou `prompts/v1.md`. Para conferir: `git -C "$WT" log <commit-saida>..HEAD --name-only -- treinamento-prompt/equipes/<nome>`.

## 4. Nota objetiva (gabarito)

Rode a partir da raiz da `main`, já que o avaliador está em `revelacao/`:

```bash
PYTHONIOENCODING=utf-8 python revelacao/avaliador/avaliar.py --arquivo "$WT/treinamento-prompt/equipes/<nome>/saida/v1/index.html" --desafio <A|B>
```

Se faltar dependência, instale com `pip install -r revelacao/avaliador/requirements.txt` e depois `python -m playwright install chromium`.
A saída mostra os 15 itens com OK ou X e um detalhe. **A nota oficial é esta.** Não altere a nota com base na sua opinião.

## 5. Análise qualitativa

- Para cada item com X, encontre a armadilha correspondente na tabela da seção 5 do `CONDUCAO.md`. Explique o que o prompt disse, ou deixou de dizer, que levou ao erro, citando um trecho do `v1.md`.
- Compare com `revelacao/exemplos/<A|B>-prompt-bom.md`: o que o prompt bom especifica e este não.
- Abra o `index.html` e procure **dados inventados**, como órgãos, números, nomes ou matrículas que não estão no material de `treinamento-prompt/desafios/`.
- Avalie os seis elementos (persona, tarefa, contexto, exemplos, formato de saída, restrições) e as técnicas do README: SoT, CoT, casos de borda, textos exatos e autoconferência.
- Comente o `briefing_colado_pct`: muito material colado indica que a equipe colou em vez de sintetizar.

## 6. Relatório

Responda em PT-BR no chat:

```
## Equipe <nome> · Desafio <A|B> · <integrantes>
**Nota: X/15** · <duracao_s>s · US$ <custo> · <caracteres> caracteres · <pct>% do material colado

### Integridade
<lista OK/⚠️>

### Itens
| # | Item | Resultado | Por quê |
(15 linhas; em "Por quê", para os X, cite a armadilha e o que faltou no prompt)

### Pontos fortes do prompt
### O que melhoraria (3 a 5 sugestões concretas, com texto que poderia entrar no prompt)
```

Salve o mesmo conteúdo em `revelacao/resultados/<nome>.md`. Essa pasta está no `.gitignore`: não faça commit.
Com `todas`, termine com um placar ordenado por nota (Equipe | Desafio | Nota | Integridade) e os itens que mais falharam por desafio. Salve esse placar em `revelacao/resultados/PLACAR.md`.

## 7. Limpeza

```bash
git worktree remove --force "$WT"; git worktree prune
```
