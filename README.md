# ✨ Moniquinha's Shine

Site profissional multilingue para os serviços da Moniquinha nas zonas de Óbidos e Caldas da Rainha.

**Produção:** [www.moniquinhashine.pt](https://www.moniquinhashine.pt/)

## Serviços

- **Limpeza de casas:** regular, profunda, pós-obra e entrada/saída
- **Alojamentos e viaturas:** Airbnb, alojamentos temporários e veículos alugados
- **Organização e cuidados do lar:** lavandaria, armários, organização doméstica, garagens, decoração festiva e home staging
- **Pacotes:** Brilho Semanal, Recomeço e Pronto a Mostrar

## Funcionalidades

- Página única responsiva em português, inglês, francês e espanhol
- Formulário de orçamento em três passos, com seleção de serviços por categoria
- Morada obrigatória e validada para Óbidos ou Caldas da Rainha
- Pesquisa de moradas através do Nominatim/OpenStreetMap
- Localização atual apenas quando o cliente carrega no respetivo botão
- Pré-visualização e ligação da morada no Google Maps
- Envio por EmailJS, pedido preparado no WhatsApp e ligação opcional para SMS
- SEO técnico com metadados, dados estruturados, sitemap, robots e favicon
- Vercel Analytics e cabeçalhos de segurança

## Tecnologia

O site é estático e não utiliza framework:

- HTML, CSS e JavaScript em `index.html`
- EmailJS para entrega do formulário por email
- Nominatim/OpenStreetMap para pesquisa e validação de moradas
- Google Maps para pré-visualização da localização confirmada
- Vercel para alojamento e deploy automático

## Desenvolvimento local

Não existe etapa de compilação. A partir da raiz do projeto:

```bash
python -m http.server 8000
```

Depois, abrir `http://127.0.0.1:8000/`.

O comando abaixo existe apenas para compatibilidade com a Vercel:

```bash
pnpm build
```

## Estrutura principal

```text
moniquinhashine/
├── index.html          # Página, estilos, traduções e comportamento
├── favicon.svg         # Favicon da marca
├── moniquinha.webp     # Imagem otimizada usada no site
├── moniquinha.jpeg     # Imagem original
├── robots.txt          # Regras para motores de pesquisa
├── sitemap.xml         # URL canónica para indexação
├── vercel.json         # Deploy, cache e cabeçalhos de segurança
└── .vercelignore       # Exclui documentação e ferramentas internas
```

`PRECOS_MERCADO.md` e `send_precos_email.py` são materiais internos e não fazem parte do site publicado.

## Deploy

O projeto Vercel está ligado ao branch `master`. Cada push para `master` inicia automaticamente um deploy de produção; não é necessário executar a CLI da Vercel.

Antes do push, confirmar:

1. O site funciona localmente nos quatro idiomas.
2. A seleção de serviços e a validação da morada continuam funcionais.
3. As ligações de WhatsApp, SMS e Google Maps são geradas corretamente.
4. `git diff --check` não apresenta erros.

## Segurança e configuração

- Nunca guardar credenciais SMTP, chaves privadas ou ficheiros `.env` no repositório.
- A chave pública do EmailJS pode existir no cliente; as permissões e domínios autorizados devem ser limitados no painel do EmailJS.
- Os documentos internos permanecem excluídos do bundle através de `.vercelignore`.

## Licença

Projeto pessoal da Moniquinha's Shine.
