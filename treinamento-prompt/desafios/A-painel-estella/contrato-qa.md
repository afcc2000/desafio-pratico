# Contrato de testes (QA)

Os testes automáticos localizam os elementos por estes atributos `data-testid`. Sem eles, o teste reprova.

| Elemento | `data-testid` |
| --- | --- |
| Título | `titulo` |
| Texto de atualização | `atualizado` |
| Card de atendimentos | `card-atendimentos` |
| Card de resolvidos | `card-resolvidos` |
| Card de transbordo | `card-transbordo` |
| Área do gráfico | `grafico-orgaos` |
| O elemento colorido de cada barra | `barra-` + sigla do órgão em minúsculas (ex.: `barra-cnpq`) |
| Tabela (elemento `<table>`) | `tabela-conversas` |
| Cada célula de status na tabela | `status` |
| Faixa de alerta | `alerta-transbordo` |
