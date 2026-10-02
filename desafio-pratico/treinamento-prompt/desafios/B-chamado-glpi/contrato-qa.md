# Contrato de testes (QA)

Os testes automáticos localizam os elementos por estes atributos `data-testid`. Sem eles, o teste reprova.

| Elemento | `data-testid` |
| --- | --- |
| Título | `titulo` |
| Subtítulo | `subtitulo` |
| Nome (campo travado) | `nome` |
| Matrícula (campo travado) | `matricula` |
| Lista de sistemas (elemento `<select>`) | `campo-sistema` |
| Opção Leitura (`<input type="radio">`) | `opcao-leitura` |
| Opção Escrita (`<input type="radio">`) | `opcao-escrita` |
| Justificativa (`<textarea>`) | `campo-justificativa` |
| Contador de caracteres | `contador` |
| Cada asterisco de obrigatório | `asterisco` |
| Botão Continuar | `btn-continuar` |
| Mensagem de erro de cada campo | `erro-sistema`, `erro-tipo`, `erro-justificativa` |
| Área do resumo | `resumo` |
| Botão Voltar e editar | `btn-voltar` |
| Botão Abrir chamado | `btn-abrir` |
| Mensagem de sucesso | `mensagem-sucesso` |
