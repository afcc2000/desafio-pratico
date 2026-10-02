# Thread de e-mails: "Painel da Estella para a reunião de outubro"

> Pessoas, órgãos e números fictícios, criados só para este desafio.

---

**De:** Laura Menezes (gestora do contrato)
**Para:** equipe de desenvolvimento
**Data:** 22/09/2026 09:14

Pessoal, bom dia!

Para a reunião de resultados de outubro, quero uma tela simples para mostrar como a Estella foi em setembro. Pensei em algo assim:

- Título "Painel da Estella".
- Quatro cards: Atendimentos, Resolvidos pela Estella, Transbordo para humano e Tempo médio de resposta.
- Um gráfico de pizza com os atendimentos de todos os órgãos.
- Uma tabela com as conversas do dia.
- Usar aquele azul do nosso site (#0057B8) como cor principal.

O Rafael vai mandar os dados. Obrigada!

---

**De:** Rafael Souto (BI)
**Data:** 22/09/2026 15:40

Oi, Laura. Seguem em anexo os dados de setembro já fechados:

- `atendimentos-setembro.csv`: atendimentos por órgão, com quantos a Estella resolveu e quantos foram para atendente humano.
- `ultimas-conversas.csv`: as últimas conversas registradas no dia 30.

Para o gráfico, sugiro usar o Chart.js direto pelo CDN, fica bonito rápido.

Ainda não tenho o tempo médio de resposta consolidado.

---

**De:** Laura Menezes
**Data:** 25/09/2026 11:02

Gente, conversei com a diretoria e mudou bastante coisa. Vale o que está aqui:

1. Tira o tempo médio de resposta, já que não temos o dado. Ficam só **três cards**, nesta ordem: **Atendimentos** (o total do mês, somando todos os órgãos), **Resolvidos pela Estella** e **Transbordo para humano**. Esses dois últimos em **percentual do total**, arredondado, sem casa decimal. O total de atendimentos com ponto de milhar, no padrão brasileiro.
2. Pizza não. Quero **barras deitadas**, só com os **5 órgãos com mais atendimentos**, do maior para o menor, com o número ao lado de cada barra. A **UFBA fica em outra cor**, porque é a implantação nova e a diretoria quer ver ela.
3. O título passa a ser **"Estella · Painel de Setembro"**. No canto direito do topo, **"Atualizado em 30/09/2026 18:00"**.
4. Esquece o azul do site. Usa as cores da marca: **fundo #2C2A29** e **destaque #3CDBC0**.
5. Na tabela, só as **5 conversas mais recentes**, com as colunas **Hora, Órgão, Assunto e Status**, nessa ordem. Protocolo e canal não precisam aparecer. O status escrito do jeito normal, **Resolvido, Transbordo ou Em andamento**, cada um com uma cor. A tabela fica à **direita do gráfico**, com o título **"Últimas conversas"**.

---

**De:** Carla Nunes (TI do órgão)
**Data:** 26/09/2026 08:47

Bom dia. Alguns pontos técnicos antes de vocês começarem:

- A tela vai rodar na TV da sala de reunião e no notebook do diretor, que é **1366×768**. **Não pode ter rolagem**, nem horizontal nem vertical.
- A nossa rede **bloqueia CDN**. Então nada de biblioteca externa: precisa ser **um arquivo HTML só**, com tudo dentro.
- A meta de transbordo do contrato é de **20%**. Se passar da meta, quero uma **faixa vermelha no topo da tela** com o texto **"Transbordo acima da meta de 20%"**.

O time de QA mandou o contrato de testes em separado (`contrato-qa.md`).
