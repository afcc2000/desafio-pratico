# Desafio de Engenharia de Prompt — Time BSB

Um prompt, uma execução. O objetivo não é a tela; é o prompt.

## A regra

- Cada dupla escolhe **um** desafio: [A — Painel da Estella](desafios/A-painel-estella/LEIA-ME.md) ou [B — Tela de chamado no GLPI](desafios/B-chamado-glpi/LEIA-ME.md).
- O prompt roda **uma única vez**, com o `executar.py`. Não existe conversa de correção.
- O prompt tem no máximo **2.000 caracteres**. Colar todo o material não cabe: é preciso sintetizar o que vale.
- Todas as equipes usam o mesmo modelo, o **Haiku**, um modelo menor, como em produção por custo. Ele não adivinha o que o prompt deixou de dizer.
- O material de cada desafio é o que o cliente mandou: e-mails com mudanças de ideia, planilhas e o contrato do QA. Transformar isso numa especificação clara é o seu trabalho.
- O Claude Code roda numa **pasta vazia**: ele **não lê** esses arquivos nem este repositório. Tudo o que ele precisa saber tem que estar no seu prompt.
- A nota é quantos dos **15 itens** do gabarito saíram certos nessa execução. O gabarito só aparece na conferência.

## Antes do treinamento (5 minutos)

1. Instale o **Python 3.10+**, o **Git** e o **Claude Code**, e faça login no Claude Code.
2. Clone o repositório e teste o ambiente:

```powershell
git clone <URL-DO-REPOSITORIO>
cd treinamento-prompt
python executar.py --verificar
```

Se aparecer “Tudo pronto para o desafio”, está tudo certo.

## Durante o desafio

```powershell
# 1. Crie a equipe (cria a branch equipe/<nome> e a pasta equipes/<nome>)
python nova_equipe.py ana-e-bruno A

# 2. Escreva o prompt em equipes/ana-e-bruno/prompts/v1.md e faça commit
git add equipes/ana-e-bruno
git commit -m "ana-e-bruno: prompt v1"

# 3. Execute uma única vez (a saída é salva e commitada sozinha)
python executar.py ana-e-bruno v1

# 4. Envie e abra um Pull Request para a main
git push -u origin equipe/ana-e-bruno
```

O resultado fica em `equipes/<nome>/saida/v1/index.html`. Abra no navegador para ver.

## Rodada 2

Depois da conferência:

1. Peça uma crítica ao Claude Code (PACE) e escreva a nova versão em `prompts/v2.md`.
2. Faça commit, rode `python executar.py <nome> v2` e dê `git push`.

O avaliador compara a v1 com a v2 e mostra o que melhorou e o que **quebrou**.

## Dicas de técnica

- Os seis elementos: persona, tarefa, contexto, exemplos, formato de saída e restrições.
- **SoT**: descreva o layout antes do detalhe.
- **CoT**: peça raciocínio passo a passo para as regras condicionais.
- Liste os **casos de borda** e os **textos exatos** entre aspas.
- Peça ao modelo que **confira o próprio resultado** contra a lista de requisitos antes de terminar.

## Perguntas frequentes

**Errei o prompt e já rodei. Posso rodar de novo?**
Não na mesma versão. Essa é a regra. Use a rodada 2.

**Posso colar trechos do material do cliente?**
Pode, dentro do limite de 2.000 caracteres. Mas e-mail de cliente não é especificação: tem decisão antiga, sugestão descartada e dado que está só na planilha. O registro da execução mostra quanto do material foi colado literalmente.

**Não é para mexer no `index.html` gerado?**
Não. A saída é o resultado do seu prompt, do jeito que veio.
