# Materiais da Moniquinha Shine

| Material | Ficheiros |
|---|---|
| Flyer A5 | [Imagem](flyers/moniquinha-shine-flyer-a5.png) |
| Cartaz | [Imagem](cartazes/moniquinha-shine-cartaz.png) |
| Cartão de visita original | [PDF frente e verso](cartoes-visita/cartao-visita-moniquinha-shine.pdf), [frente](cartoes-visita/cartao-visita-frente.png), [verso](cartoes-visita/cartao-visita-verso.png) |
| Cartão de visita alternativo | [PDF](cartoes-visita/cartao-visita-simples-alternativo.pdf) |
| Íman em coração com avatar | [PNG transparente](imanes/moniquinha-shine-iman-coracao-avatar.png), [PDF de prova a 75 mm](imanes/moniquinha-shine-iman-coracao-avatar-75mm.pdf), [instruções](imanes/README.md) |
| Íman retangular com avatar | [PNG transparente](imanes/moniquinha-shine-iman-retangular-avatar.png), [PDF de prova a 90 × 60 mm](imanes/moniquinha-shine-iman-retangular-avatar-90x60mm.pdf) |
| Íman em estrela com avatar | [PNG transparente](imanes/moniquinha-shine-iman-estrela-avatar.png), [PDF de prova a 90 mm](imanes/moniquinha-shine-iman-estrela-avatar-90mm.pdf) |
| Recursos da marca | [Estrela para impressão](recursos/marca/moniquinha-star-print.png), [WhatsApp](recursos/marca/whatsapp-logo-gradient.png), [favicon legado](recursos/marca/favicon-legado.svg) |

Os materiais anteriores foram preservados. As imagens dos cartões representam a versão original; o cartão alternativo tem o seu próprio PDF.

Esta pasta não faz parte do site publicado. As imagens e os logótipos que o site utiliza continuam na raiz do projeto.

Para gerar o PDF do coração: `python scripts/create_magnet_pdf.py`. Para as variantes, acrescentar `--variant retangular` ou `--variant estrela` (requer `reportlab` e `Pillow`). O gerador do cartão original é `scripts/create_business_card.py` e requer as fontes Segoe UI do Windows.
