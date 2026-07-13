# ✨ Moniquinha's Shine

Website profissional para serviços de limpeza e serviços domésticos na região de Óbidos e Caldas da Rainha.

**Live:** [moniquinhashine.pt](https://moniquinhashine.pt)

## Serviços

- 🧹 Limpeza regular e profunda
- 🏡 Limpeza de Airbnb e alojamentos temporários
- 🚗 Limpeza de veículos alugados para visitantes em Óbidos
- 📦 Organização doméstica
- 👔 Lavandaria e engomadoria
- 🏨 Home staging

## Funcionalidades

- Landing page single-page responsiva
- Multilingue (PT, EN, FR, ES)
- Formulário de contacto via EmailJS + WhatsApp deep-link
- **Wizard de orçamento em 3 passos** com validação por passo
- **Morada obrigatória com autocomplete** (Nominatim / OpenStreetMap)
  - Resultados limitados a Óbidos e Caldas da Rainha
  - Botão opcional para o cliente partilhar a localização atual
  - Pré-visualização e link da morada no Google Maps
- SEO optimizado (meta tags, Open Graph, sitemap, robots.txt)
- Design mobile-first

## Tech Stack

- **HTML/CSS/JS** — site estático, sem framework
- **EmailJS** — envio de formulários sem backend
- **Nominatim (OpenStreetMap)** — pesquisa e confirmação de moradas
- **Google Maps embed** — pré-visualização da morada confirmada
- **Hosting:** pode ser qualquer host estático (Vercel, Netlify, GitHub Pages)

## Setup

Não requer instalação — basta servir os ficheiros estáticos.

```bash
# Localmente com Python
python -m http.server 8000

# Ou com npx
npx serve .
```

## Estrutura

```
moniquinha-shine/
├── index.html         # Página principal (HTML completo)
├── favicon.svg        # Ícone de estrela da marca
├── moniquinha.jpeg    # Foto de perfil (original)
├── moniquinha.webp    # Foto de perfil (optimizada)
├── robots.txt         # Instruções para crawlers
└── sitemap.xml        # Sitemap para SEO
```

## Deploy

Site estático — fazer upload dos ficheiros para qualquer hosting.

### Vercel (recomendado)

O projeto `moniquinhas-shine` está ligado ao repositório através da integração Git da Vercel.

**Deploy automático:** cada push para `master` cria uma implantação de produção diretamente na Vercel. Não é necessário um workflow GitHub Actions separado nem segredos do Vercel no GitHub.

**Deploy manual** (CLI):

```bash
npx vercel --prod
```

Configuração da pasta de saída, cabeçalhos, redirects e cache em `vercel.json`. Ficheiros internos (research, mailer) excluídos do bundle via `.vercelignore`.

### GitHub Pages (alternativa)

1. Settings → Pages → Source: Deploy from branch → `master` / `root`
2. Site disponível em `https://findmucker.github.io/moniquinha-shine/`

## Domínio

O site está configurado para o domínio `moniquinhashine.pt`. Para ligar:
1. Configurar DNS A record para o IP do hosting
2. Ou CNAME para o domínio do hosting provider

## Licença

Projeto pessoal — feito com ✨
