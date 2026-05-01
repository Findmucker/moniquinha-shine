# ✨ Moniquinha's Shine

Website profissional para serviços de limpeza, babysitting e serviços domésticos na região de Óbidos e Caldas da Rainha.

**Live:** [moniquinhashine.pt](https://moniquinhashine.pt)

## Serviços

- 🧹 Limpeza regular e profunda
- 👶 Babysitting
- 📦 Organização doméstica
- 👔 Lavandaria e engomadoria
- 🎨 Home staging e decoração de interiores

## Funcionalidades

- Landing page single-page responsiva
- Multilingue (PT, EN, FR, ES)
- Formulário de contacto via EmailJS
- SEO optimizado (meta tags, Open Graph, sitemap, robots.txt)
- Design mobile-first

## Tech Stack

- **HTML/CSS/JS** — site estático, sem framework
- **EmailJS** — envio de formulários sem backend
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
├── moniquinha.jpeg    # Foto de perfil (original)
├── moniquinha.webp    # Foto de perfil (optimizada)
├── robots.txt         # Instruções para crawlers
└── sitemap.xml        # Sitemap para SEO
```

## Deploy

Site estático — fazer upload dos ficheiros para qualquer hosting.

Para GitHub Pages:
1. Settings → Pages → Source: Deploy from branch → `master` / `root`
2. Site disponível em `https://findmucker.github.io/moniquinha-shine/`

## Domínio

O site está configurado para o domínio `moniquinhashine.pt`. Para ligar:
1. Configurar DNS A record para o IP do hosting
2. Ou CNAME para o domínio do hosting provider

## Licença

Projeto pessoal — feito com ✨
