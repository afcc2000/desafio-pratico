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

# Contrato de testes (QA)

Os testes automáticos 