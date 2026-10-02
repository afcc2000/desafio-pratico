Você é dev front-end sênior. Crie UM index.html (CSS/JS inline, sem lib externa) da tela GLPI. QA automatizado: textos e data-testid EXATOS. [x] = data-testid="x".

FORMULÁRIO
- Título "Solicitação de acesso a sistema" [titulo]; subtítulo "Seus dados já foram preenchidos pelo login" [subtitulo].
- <input readonly> Nome "Marina Souza" [nome] e Matrícula "48213" [matricula].
- Sistema: <select> [campo-sistema] com 1ª opção "Selecione" value="" e depois SEI, SIGEPE, GLPI.
- Tipo de acesso: 2 <input type="radio" name="tipo">: Leitura [opcao-leitura], Escrita [opcao-escrita]. Nenhum marcado.
- Justificativa: <textarea> [campo-justificativa], escondida (contêiner display:none) exceto com Escrita marcada. Contador "N/20" [contador], começa "0/20", atualiza no evento input; cor #2E7D32 com 20+ caracteres, senão #6B6A67.
- Asterisco "*" vermelho #D32F2F [asterisco] nos rótulos dos 3 campos.
- Botão "Continuar" [btn-continuar], type="button".

AO CLICAR CONTINUAR (passo a passo; nunca use alert/confirm):
1. Sistema vazio → "Campo obrigatório" em #D32F2F embaixo dele [erro-sistema].
2. Sem tipo → "Campo obrigatório" [erro-tipo].
3. Escrita e justificativa < 20 caracteres → "Campo obrigatório" [erro-justificativa].
Erros ficam ocultos até haver erro e somem quando corrigidos.
4. Tudo válido → esconde o formulário e mostra o RESUMO.

RESUMO [resumo]: mostra sistema, "Leitura"/"Escrita" e a justificativa. Botões:
- "Voltar e editar" [btn-voltar]: volta ao formulário com todos os valores mantidos e a justificativa visível.
- "Abrir chamado" [btn-abrir]: mostra "Chamado #2026-00412 aberto com sucesso" [mensagem-sucesso].

Estilo: fundo #2C2A29, cartão #F4F4F2, botões #3CDBC0.

Antes de terminar, simule: tudo vazio→Continuar; Leitura; Escrita com 19 e 20 letras; preencher→Continuar; Voltar; Abrir. Corrija o que falhar.
