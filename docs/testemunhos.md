# Testemunhos: configuração e ensaio

1. Criar um projeto Supabase dedicado à Moniquinha Shine (região da UE). Executar [`sql/reviews.sql`](../sql/reviews.sql) nele. A tabela bloqueia acesso direto do navegador e permite apenas operações feitas pelo servidor.
2. No projeto Vercel `moniquinhas-shine`, configurar **apenas no ambiente Production** `SUPABASE_URL` e `SUPABASE_SECRET_KEY` do projeto criado. A secret key é privada e nunca deve ser colocada no HTML ou no Git. Fazer um novo deploy para carregar as variáveis.
3. Verificar que o EmailJS usado pelo formulário de orçamentos entrega a mensagem com `{{message}}` à Moniquinha; a mensagem do testemunho inclui o endereço privado de aprovação. O endpoint `/api/reviews` usa o serviço e template existentes do site.
4. Um cliente preenche o formulário e recebe uma confirmação. O testemunho é guardado como `pending`, invisível ao público. O servidor envia um email à Moniquinha com a ligação para rever, publicar ou apagar. O email do cliente/telemóvel nunca aparece no cartão público.
5. A Moniquinha abre a ligação, verifica o contacto e clica em **Publicar testemunho**. Uma atualização da página mostra o cartão publicado. A mesma ligação tem **Apagar testemunho** e remove também os dados privados; use-a para apagar o testemunho do ensaio.

O comentário fica no idioma em que foi escrito. Apenas a interface e o nome do serviço seguem o idioma do site. A chave privada de moderação fica no fragmento (`#`) do URL, que o navegador não envia na requisição de página. Não partilhar o email nem a ligação privada.

Para verificar a lógica sem enviar emails reais: `node --test test/reviews.test.js`.
