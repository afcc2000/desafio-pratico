# Guia de condução do desafio (só para o instrutor)

| Pasta | O que é |
| --- | --- |
| `treinamento-prompt/` | O que o time usa: regras, material do cliente, scripts |
| `revelacao/` | Avaliador (gabarito de 15 itens) e exemplos para o debrief |

Fluxo: cada pessoa ou dupla cria uma branch `equipe/<nome>`, escreve **um** prompt, roda uma vez e dá push. Depois, você abre o Claude Code neste repositório e pede a avaliação da branch. Não tem GitHub Actions nem Pull Request.

## 1. Preparação

1. Dê acesso de escrita (push) ao time no repositório `afcc2000/desafio-pratico`.
2. Peça a cada pessoa que clone e rode a verificação, que confere Python, Git e Claude Code e faz uma execução de teste de poucos segundos:

   ```powershell
   git clone https://github.com/afcc2000/desafio-pratico.git
   cd desafio-pratico/treinamento-prompt
   python executar.py --verificar
   ```

3. Na sua máquina, uma vez só, instale o avaliador:

   ```powershell
   pip install -r revelacao/avaliador/requirements.txt
   python -m playwright install chromium
   ```

## 2. As regras do desafio, em resumo

- **Uma execução.** O `executar.py` recusa uma segunda rodada da mesma versão.
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

Um mesmo prompt pode variar 1 ou 2 itens entre execuções.

## 3. Roteiro no dia

| Momento | Tempo | O que você faz |
| --- | --- | --- |
| Abertura | 2 min | Regra central: o objetivo não é a tela, é o prompt. |
| Criar equipes | 2 min | Cada um roda `python nova_equipe.py <nome> <A ou B>`. |
| Ler o material | 3 min | O material completo está nas pastas `treinamento-prompt/desafios/`. |
| Escrever o prompt | 10 min | Você é o cliente: responda só "está nos e-mails" ou "decidam vocês". Avise quando faltarem 5 e 2 minutos. |
| Executar | 2 min | Commit, `python executar.py <nome> v1` e `git push -u origin equipe/<nome>`. |
| Avaliação | 5 min | Veja a seção 4. |
| Debrief | 5 min | Resultado de cada equipe e os exemplos de `revelacao/exemplos/`. |

## 4. Avaliação com o Claude Code

Abra o Claude Code na raiz deste repositório (`desafio-pratico`) e peça:

```
/avaliar-equipe equipe/<nome>      # uma equipe
/avaliar-equipe todas              # todas as branches equipe/* com placar
```

O Claude busca a branch sem mexer na sua `main` e confere a integridade (seção 6). Depois roda o avaliador de 15 itens e explica cada item que falhou, cruzando com as armadilhas da seção 5 e com o prompt bom de exemplo. Uma cópia do relatório fica em `revelacao/resultados/<equipe>.md`.

Para testar um HTML solto à mão:

```powershell
$env:PYTHONIOENCODING="utf-8"
python revelacao/avaliador/avaliar.py --arquivo <caminho>/index.html --desafio A
```

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

- **Origem do HTML:** `saida/v1/execucao.json` registra o horário, a duração, o hash do prompt, o modelo, o custo e quanto do material foi colado. Um HTML sem esse arquivo não veio do `executar.py`.
- **Prompt original:** confira se o hash do prompt bate com o arquivo commitado.
- **Edição à mão:** se alguém editar o `index.html` depois, o commit aparece no histórico da branch.

## 7. Custos e requisitos

- Cada execução com o Haiku custou entre US$ 0,04 e US$ 0,10 nos testes e levou de 30 a 70 segundos. Ela usa a conta do Claude Code de cada pessoa.
- Requisitos por pessoa: Python 3.10+, Git, Claude Code instalado e logado, e acesso de escrita ao repositório.
- No Windows, se `python` não funcionar, use `py` (por exemplo, `py executar.py --verificar`).
