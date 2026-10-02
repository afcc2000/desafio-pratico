# Guia de condução do desafio (só para o instrutor)

Este pacote tem duas partes:

| Pasta | O que é | Quando entra no GitHub |
| --- | --- | --- |
| `treinamento-prompt/` | O repositório que o time clona: regras, material do cliente, scripts | Antes do treinamento |
| `revelacao/` | Avaliador, workflow do GitHub Actions e exemplos para o debrief | Só na hora da conferência |

A pasta `revelacao/` fica fora do repositório até a conferência por um motivo simples: tudo o que está no repositório o time pode ler, inclusive o gabarito.

## 1. Preparação (um ou dois dias antes)

1. Crie um repositório privado no GitHub, por exemplo `treinamento-prompt`, e dê acesso de escrita ao time.
2. Suba o conteúdo de `treinamento-prompt/` na branch `main`:

   ```powershell
   cd treinamento-prompt
   git init -b main
   git add -A
   git commit -m "Desafio de engenharia de prompt"
   git remote add origin https://github.com/<org-ou-usuario>/treinamento-prompt.git
   git push -u origin main
   ```

3. Em **Settings › Actions › General**, confirme que o Actions está habilitado e que o `GITHUB_TOKEN` tem permissão de leitura e escrita (*Read and write permissions*). É isso que permite comentar nos PRs.
4. Peça a cada pessoa que rode `python executar.py --verificar` antes do dia. O comando confere Python, Git e Claude Code e faz uma execução de teste de poucos segundos.
5. Rode você mesmo os dois desafios uma vez, com um prompt bom e um prompt colado, para ter o seu próprio antes e depois.

## 2. As regras do desafio, em resumo

- **Uma execução por versão.** O `executar.py` recusa uma segunda rodada.
- **Commit antes de rodar.** O script recusa o prompt que não foi commitado. O histórico prova que o prompt veio antes da saída.
- **Pasta isolada.** O Claude Code roda numa pasta temporária vazia e não vê o material do cliente nem o repositório.
- **Limite de 2.000 caracteres** no prompt. O material inteiro tem mais de 5.000, então não dá para colar tudo.
- **Mesmo modelo para todos: Haiku.** É menor, como se usaria em produção por custo, e não adivinha o que o prompt deixou de dizer.

### Por que o limite e o Haiku

Nos testes, colar o material inteiro num modelo grande dava 15/15. A tarefa virava copiar e colar. Com o Haiku e o limite, os resultados foram estes:

| Prompt | Desafio A | Desafio B |
| --- | --- | --- |
| Uma frase genérica | 0/15 | 1/15 |
| Trechos dos e-mails colados até o limite | 2/15 | 2/15 |
| Especificação sintetizada com as técnicas (`revelacao/exemplos/`) | 15/15 | 15/15 |

Um mesmo prompt pode variar 1 ou 2 itens entre execuções. Vale dizer isso no debrief: é exatamente o motivo de existir teste de regressão.

## 3. Roteiro no dia

| Momento | Tempo | O que você faz |
| --- | --- | --- |
| Abertura | 2 min | Slide 26. Regra central: o objetivo não é a tela, é o prompt. |
| Criar equipes | 2 min | Cada dupla roda `python nova_equipe.py <nome> <A ou B>`. |
| Ler o material | 3 min | Slides 27 e 28. O material completo está nas pastas `desafios/`. |
| Escrever o prompt | 10 min | Você é o cliente: responda só "está nos e-mails" ou "decidam vocês". Avise quando faltarem 5 e 2 minutos. |
| Executar | 2 min | Commit, `python executar.py <nome> v1`, `git push` e Pull Request. |
| Revelação | 5 min | Veja a seção 4. |
| Rodada 2 | 10 min | Slide 31. PACE para criticar, `v2.md`, executar e push. O Actions reavalia sozinho. |
| Debrief | 5 min | `placar.html` na tela e os exemplos de `revelacao/exemplos/`. |

## 4. A revelação (conferência)

Copie o avaliador e o workflow para a `main` e envie:

```powershell
# a partir da pasta do repositório clonado, na branch main
xcopy /E /I ..\revelacao\avaliador avaliador
xcopy /E /I ..\revelacao\.github .github
git add avaliador .github
git commit -m "Avaliador do desafio"
git push
```

Depois, no GitHub: **Actions › Avaliar desafio › Run workflow**. Em 2 ou 3 minutos:

- cada PR recebe um comentário com a nota, item a item;
- o resumo da execução mostra o placar;
- o artefato `resultados` traz o `placar.html` com os screenshots de todas as equipes.

**Plano B, sem Actions:** rode na sua máquina.

```powershell
pip install -r avaliador/requirements.txt
python -m playwright install chromium
python avaliador/avaliar.py --branches
start resultados\placar.html
```

Na rodada 2, cada `git push` numa branch com PR aberto dispara a avaliação de novo. O comentário mostra a v1 contra a v2 e marca com 🔻 o que quebrou.

## 5. As armadilhas do material (para o debrief)

### Desafio A: Painel da Estella

| Armadilha no material | Item do gabarito |
| --- | --- |
| O primeiro e-mail pede 4 cards; o terceiro tira o tempo médio | 3 |
| O total de atendimentos não está escrito: é a soma do CSV (15.090) | 4 |
| Resolvidos e transbordo precisam virar percentual (78% e 22%) | 4 |
| Primeiro era pizza com todos os órgãos; depois, barras deitadas só com os 5 maiores | 5, 6, 7 |
| O CSV vem fora de ordem | 6 |
| O CSV de conversas tem 8 linhas fora de ordem; só entram as 5 mais recentes | 10 |
| O status no CSV vem como `em_andamento` | 11 |
| O azul do site foi descartado | 14 |
| O BI sugeriu Chart.js por CDN; a TI proibiu CDN | 15 |
| O contrato diz `barra-` + sigla: é preciso deduzir `barra-ufba` | 5 a 8 |

### Desafio B: Tela de chamado no GLPI

| Armadilha no material | Item do gabarito |
| --- | --- |
| O export do formulário ainda tem SIAFI | 3 |
| O export ainda tem Administrador | 4 |
| O export diz 10 caracteres; o Jurídico mudou para 20 | 9 |
| A justificativa só existe para Escrita | 6, 7 |
| O primeiro e-mail pedia alerta; depois proibiram pop-up | 10, 11 |
| O número do chamado precisa ser montado: ano 2026 + id 412 com 5 dígitos = `#2026-00412` | 14 |
| Nome e matrícula estão só no `usuario-logado.json` | 2 |

Uma observação boa para o debrief: nos testes, os prompts colados fizeram o modelo **inventar** dados, como órgãos e números que não existem e um usuário com nome e matrícula falsos. É alucinação por falta de contexto, ao vivo.

## 6. Como saber se alguém burlou a regra

- **Origem do HTML:** `saida/vN/execucao.json` registra o horário, a duração, o hash do prompt, o modelo, o custo e quanto do material foi colado. Um HTML sem esse arquivo não veio do `executar.py`.
- **Prompt original:** confira se o hash do prompt bate com o arquivo commitado. Ele fica no histórico do git.
- **Edição à mão:** se alguém editar o `index.html` depois, o commit aparece no histórico da branch.

## 7. Custos e requisitos

- Cada execução com o Haiku custou entre US$ 0,04 e US$ 0,10 nos testes e levou de 30 a 70 segundos. Ela usa a conta do Claude Code de cada pessoa.
- Requisitos por pessoa: Python 3.10+, Git, Claude Code instalado e logado, e acesso de escrita ao repositório.
- No Windows, se `python` não funcionar, use `py` (por exemplo, `py executar.py --verificar`).
