# Testemunhos: configuração e ensaio

1. Projeto Supabase dedicado à Moniquinha Shine: `vpdovbwljwtlqhnqefwo` (Europa). A tabela foi criada com [`sql/reviews.sql`](../sql/reviews.sql). O acesso direto anónimo à tabela está bloqueado; apenas a função do Supabase pode ler e escrever os dados.
2. Publicar [`supabase/functions/reviews/index.js`](../supabase/functions/reviews/index.js) como função Edge `reviews` com `verify_jwt=false` porque o público tem de poder enviar testemunhos e ler os aprovados. A função aplica autenticação própria por token aleatório para ações privadas. Usa a chave secreta disponibilizada automaticamente pelo Supabase à função; nenhuma chave privada fica no site ou no Vercel.
3. Verificar que o EmailJS usado pelo formulário de orçamentos entrega a mensagem com `{{message}}` à Moniquinha; a mensagem do testemunho inclui o endereço privado de aprovação. O endpoint público da função usa o serviço e template existentes do site.
4. Um cliente preenche o formulário e recebe uma confirmação. O testemunho é guardado como `pending`, invisível ao público. O servidor envia um email à Moniquinha com a ligação para rever, publicar ou apagar. O email do cliente/telemóvel nunca aparece no cartão público.
5. A Moniquinha abre a ligação, verifica o contacto e clica em **Publicar testemunho**. Uma atualização da página mostra o cartão publicado. A mesma ligação tem **Apagar testemunho** e remove também os dados privados; use-a para apagar o testemunho do ensaio.

O comentário fica no idioma em que foi escrito. Apenas a interface e o nome do serviço seguem o idioma do site. A chave privada de moderação fica no fragmento (`#`) do URL, que o navegador não envia na requisição de página. Não partilhar o email nem a ligação privada.

Para verificar a lógica sem enviar emails reais: `node --test test/reviews.test.js`.
