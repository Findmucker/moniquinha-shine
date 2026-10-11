# Organização dos ficheiros

Reorganização de 11 de outubro de 2026. Os materiais anteriores foram movidos, sem alterar o seu conteúdo. O site e as suas imagens ativas mantêm os caminhos existentes.

| Caminho anterior | Caminho atual |
|---|---|
| `PRECOS_MERCADO.md` | [docs/negocio/precos-mercado.md](negocio/precos-mercado.md) |
| `docs/testemunhos.md` | [docs/tecnico/testemunhos.md](tecnico/testemunhos.md) |
| `output/images/MoniquinhaShineFlyer-A5.png` | [materiais/flyers/moniquinha-shine-flyer-a5.png](../materiais/flyers/moniquinha-shine-flyer-a5.png) |
| `output/images/MoniquinhaShinePoster.png` | [materiais/cartazes/moniquinha-shine-cartaz.png](../materiais/cartazes/moniquinha-shine-cartaz.png) |
| `output/pdf/cartao-visita-moniquinha-shine.pdf` | [materiais/cartoes-visita/cartao-visita-moniquinha-shine.pdf](../materiais/cartoes-visita/cartao-visita-moniquinha-shine.pdf) |
| `output/pdf/cartao-visita-simples-alternativo.pdf` | [materiais/cartoes-visita/cartao-visita-simples-alternativo.pdf](../materiais/cartoes-visita/cartao-visita-simples-alternativo.pdf) |
| `output/pdf/cartao-visita-frente.png` | [materiais/cartoes-visita/cartao-visita-frente.png](../materiais/cartoes-visita/cartao-visita-frente.png) |
| `output/pdf/cartao-visita-verso.png` | [materiais/cartoes-visita/cartao-visita-verso.png](../materiais/cartoes-visita/cartao-visita-verso.png) |
| `output/pdf/moniquinha-star-print.png` | [materiais/recursos/marca/moniquinha-star-print.png](../materiais/recursos/marca/moniquinha-star-print.png) |
| `output/pdf/whatsapp-logo-gradient.png` | [materiais/recursos/marca/whatsapp-logo-gradient.png](../materiais/recursos/marca/whatsapp-logo-gradient.png) |
| `favicon.svg` (legado) | [materiais/recursos/marca/favicon-legado.svg](../materiais/recursos/marca/favicon-legado.svg) |

## Limpeza realizada

- Separação de documentos de negócio, documentação técnica e materiais gráficos por tipo.
- Remoção da antiga estrutura `output/images` / `output/pdf`, depois de mover todos os ficheiros.
- Correção das ligações da documentação técnica e dos caminhos dos recursos no gerador do cartão original.
- Remoção da referência a `send_precos_email.py` do README e da configuração: o ficheiro não existe no repositório atual.
- Exclusão de materiais, scripts e documentação do deploy; regras para evitar caches Python e ficheiros temporários no Git.
- Preservação dos dois cartões, flyer, cartaz e recursos gráficos anteriores. Não foram eliminados materiais finais.

Consultar o [índice dos materiais](../materiais/README.md) e as [instruções do íman](../materiais/imanes/README.md).
