Você é dev front-end sênior. Crie UM index.html (CSS/JS inline, sem CDN nem lib externa) com o painel da Estella. Testes automáticos: textos e data-testid EXATOS.

Layout, de cima para baixo, cabendo em 1366x768 sem rolagem:
1. Faixa vermelha (#D32F2F, texto branco) "Transbordo acima da meta de 20%" [alerta-transbordo]. Aparece porque transbordo 22% > meta 20% (regra em JS).
2. Linha: título "Estella · Painel de Setembro" [titulo] à esquerda; "Atualizado em 30/09/2026 18:00" [atualizado] à direita.
3. Três cards lado a lado nesta ordem: "Atendimentos" 15.090 [card-atendimentos]; "Resolvidos pela Estella" 78% [card-resolvidos]; "Transbordo para humano" 22% [card-transbordo].
4. Duas colunas:
- Esquerda [grafico-orgaos]: barras HORIZONTAIS (divs), maior para menor, valor ao lado: CNPq 3.920, UFBA 2.870, DNIT 2.410, CAPES 1.960, MJ 1.320. Só esses 5. Barras #3CDBC0 [barra-cnpq, barra-ufba, barra-dnit, barra-capes, barra-mj]; UFBA em #FFB25C.
- Direita: título "Últimas conversas" e <table> [tabela-conversas], colunas Hora, Órgão, Assunto, Status, exatamente estas linhas:
17:58 CNPq Bolsa de produtividade Resolvido
17:51 UFBA Trancamento de matrícula Em andamento
17:44 DNIT Recurso de multa Transbordo
17:37 CAPES Acesso à Plataforma Sucupira Resolvido
17:30 MJ Emissão de certidão Transbordo
Cada célula de status [status] com fundo próprio: Resolvido #2E7D32, Transbordo #C62828, Em andamento #F9A825.

Estilo: fundo da página #2C2A29, texto #EDEDEA, destaque #3CDBC0. [x] = data-testid="x".

Antes de terminar, confira cada item acima no arquivo e corrija o que faltar.
