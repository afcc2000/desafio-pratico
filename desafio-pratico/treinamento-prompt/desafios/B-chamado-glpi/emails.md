# Thread de e-mails: "Tela de solicitação de acesso (GLPI)"

> Pessoas e dados fictícios, criados só para este desafio.

---

**De:** Paulo Ribeiro (coordenador de TI, dono do formulário)
**Para:** equipe de desenvolvimento
**Data:** 15/09/2026 10:05

Pessoal, precisamos de uma tela para o formulário **"Solicitação de acesso a sistema"** do GLPI. A ideia inicial:

- Sistema: SEI, SIGEPE, GLPI e SIAFI.
- Tipo de acesso: Leitura, Escrita ou Administrador.
- Justificativa: sempre obrigatória, com pelo menos 10 caracteres.
- Se faltar algum campo, mostra um alerta avisando a pessoa.

Mando em anexo o export do formulário (`formulario-exportado.json`).

---

**De:** Helena Prado (Jurídico)
**Data:** 17/09/2026 16:22

Paulo, uma observação: a justificativa só faz sentido quando o acesso é de **Escrita**. Nesse caso, ela precisa ter **no mínimo 20 caracteres**. Para Leitura, nem mostrem o campo.

---

**De:** Paulo Ribeiro
**Data:** 18/09/2026 09:30

Combinado com o Jurídico. Atualizando tudo, vale o que está aqui:

1. **Administrador sai**, isso é outro formulário. O tipo de acesso fica só **Leitura ou Escrita**, em **botões de opção**.
2. **SIAFI também não entra agora.** A lista fica **SEI, SIGEPE e GLPI**, nessa ordem. O export que mandei está desatualizado.
3. A justificativa segue o que a Helena disse e tem um **contador "0/20"** que se atualiza enquanto a pessoa digita e **fica verde quando chegar em 20**.
4. **Nada de pop-up de alerta**, os usuários odeiam. Quando faltar algo, aparece **"Campo obrigatório"** em vermelho **embaixo de cada campo** que faltou.
5. Os campos obrigatórios levam um **asterisco vermelho**.
6. O título é o nome do formulário. O subtítulo é **"Seus dados já foram preenchidos pelo login"**. Nome e matrícula vêm do login e **não podem ser editados**.
7. Antes de abrir, mostra um **resumo** com os dados escolhidos e dois botões: **"Voltar e editar"**, sem perder nada do que foi preenchido, e **"Abrir chamado"**.

---

**De:** Tiago Lima (backend do MCP)
**Data:** 19/09/2026 14:10

Oi, pessoal. Para a tela de teste:

- O usuário logado vem como em `usuario-logado.json`.
- Quando o chamado é criado, o MCP devolve algo como `resposta-api-exemplo.json`. Usem essa resposta de exemplo, sem chamar API nenhuma.
- A mensagem de sucesso segue o padrão do service desk: **"Chamado #AAAA-NNNNN aberto com sucesso"**, onde AAAA é o ano e NNNNN é o número do chamado com **5 dígitos**, completando com zeros à esquerda.
- Cores da Positivo: **#2C2A29** e **#3CDBC0**. **Um arquivo HTML só**, sem bibliotecas externas.

O QA mandou o contrato de testes em separado (`contrato-qa.md`).
