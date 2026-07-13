# Moniquinha's Shine — Pesquisa e Decisão de Preços

**Zona de serviço:** exclusivamente Óbidos e Caldas da Rainha

**Moeda:** EUR (€)

**Atualização da pesquisa:** 13 de julho de 2026

**Estado:** documento interno; preços parcialmente definidos pela Moniquinha

> **Em estudo:** os serviços para alojamentos temporários e veículos alugados não estão publicados no site e não devem entrar no simulador até serem revistos e aprovados pela Moniquinha.

> Todos os serviços têm obrigatoriamente um preço por hora. Preços por visita, rotação, viatura, m² ou projeto são alternativas comerciais e devem ser comparados com o custo horário interno.

## Preços já definidos pela Moniquinha

| Serviço | Preço definido | Mínimo | Condição |
|---|---:|---:|---|
| Limpezas normais | **12 €/h** | **2 h — 24 €** | O valor pode ser ajustado conforme a quantidade de sujidade. |
| Limpeza pós-obra | **a partir de 20 €/h** | A confirmar | Avaliar o estado e o trabalho necessário. |
| Engomadoria — peça normal | **1 €/peça** | A confirmar | Aplicável a peças que possam ser engomadas normalmente. |
| Camisas | **2 €/peça** | A confirmar | Engomadoria. |
| Lençóis | **2 €/peça** | A confirmar | Engomadoria. |
| Capas de edredão | **2 €/peça** | A confirmar | Engomadoria. |
| Restantes serviços | **sob orçamento** | A confirmar | Definir em detalhe com o cliente o que pretende. |

## 1. O que a pesquisa permite concluir

- A Fixando apresenta para limpeza recorrente nas Caldas da Rainha **10–15 €/h**, com média de **12 €/h**.
- A Zaask apresenta a nível nacional **8–25 €/h** para limpeza doméstica, com média próxima de **12 €/h** e exemplos frequentes de **12–15 €/h**.
- Para limpeza profunda, as referências nacionais indicam **12–20 €/h**, podendo ultrapassar 20 €/h em casas maiores ou mais exigentes.
- Para limpeza pós-obra, a Zaask publica **17–30 €/h**, com média aproximada de **20 €/h**.
- Para engomadoria, a referência nacional é **10–15 €/h**. A Lavandaria da Rainha anuncia lavagem e secagem a partir de **1,50 €/kg**.
- Para organização da casa, a Fixando apresenta uma média indicativa de **329 € por projeto no distrito de Leiria**, mas não publica detalhe suficiente para obter uma taxa horária local fiável.
- Empresas de Caldas da Rainha e Óbidos anunciam limpeza doméstica, profunda, pós-obra e rotação de alojamentos, mas normalmente pedem orçamento em vez de publicar preços.
- Para os restantes serviços, os intervalos deste documento são referências de trabalho, não preços locais confirmados.

## 2. Confiança das referências

| Nível | Significado |
|---|---|
| **Local publicado** | Preço explicitamente publicado para Caldas da Rainha ou Óbidos. |
| **Regional publicado** | Preço publicado para o distrito de Leiria ou uma zona próxima comparável. |
| **Nacional publicado** | Preço publicado para Portugal; pode não refletir exatamente o mercado local. |
| **Intervalo de trabalho** | Inferência para discussão, baseada em duração, âmbito e referências disponíveis. |

## 3. Tabela de decisão — preço por hora

Esta é a tabela principal e a futura fonte do simulador. Os valores já comunicados pela Moniquinha estão preenchidos; os restantes ficam por decidir após conversa com o cliente.

O preço-base é cobrado pelas horas trabalhadas. Quando a Moniquinha leva produtos, soma-se **uma taxa fixa definida para esse serviço**, independentemente da duração. Compras, materiais decorativos e consumíveis especiais continuam sempre separados.

| ID | Serviço | Referência horária | Confiança | **Preço-base sem produtos** | **Taxa fixa de produtos por serviço** | **Mínimo de horas** | **Preço mínimo** |
|---|---|---:|---|---:|---:|---:|---:|
| `cleaning` | Limpeza Regular | 10–15 €/h | Local publicado | **12 €/h** | **___ €** | **2 h** | **24 €** |
| `deep-cleaning` | Limpeza Profunda | 12–20+ €/h | Nacional publicado | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `construction` | Limpeza Pós-Obra | 17–30 €/h | Nacional publicado | **a partir de 20 €/h** | **___ €** | **___ h** | **___ €** |
| `movein` | Limpeza de Entrada/Saída | 12–25 €/h | Nacional + intervalo | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `rental-stay` | Airbnb e Alojamentos Temporários | derivado do tempo de rotação | Intervalo de trabalho | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `rental-car` | Veículos Alugados | derivado do tempo por viatura | Regional + intervalo | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `laundry` | Lavandaria e Engomadoria | 10–15 €/h para engomar | Nacional publicado | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `closet` | Organização de Armários | 20–35 €/h | Intervalo de trabalho | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `organization` | Organização do Lar | 20–35 €/h | Intervalo de trabalho | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `garage` | Garagens e Armazéns | 20–35 €/h | Intervalo de trabalho | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `holiday` | Decoração de Festas e Épocas | sem comparável local fiável | Intervalo de trabalho | **___ €/h** | **___ €** | **___ h** | **___ €** |
| `staging` | Home Staging Leve | derivado do âmbito e duração | Nacional + intervalo | **___ €/h** | **___ €** | **___ h** | **___ €** |

### Como preencher a taxa de produtos

```text
preço sem produtos
    = preço-base por hora × horas trabalhadas

preço com produtos
    = (preço-base por hora × horas trabalhadas)
    + taxa fixa de produtos desse serviço
```

A taxa de produtos é aplicada **uma única vez ao serviço**. Por exemplo, duas ou cinco horas de limpeza regular usam a mesma taxa fixa de produtos da limpeza regular. Cada tipo de serviço pode ter uma taxa diferente; preencher **0 €** quando não se aplicar.

## 4. Preços alternativos ao valor por hora

Preencher apenas os que a Moniquinha quiser mostrar ao cliente. A taxa horária da secção 3 continua obrigatória.

| ID | Unidade alternativa | Como validar internamente | **Preço decidido** |
|---|---|---|---:|
| `cleaning` | visita recorrente | horas previstas × preço/hora | **___ €/visita** |
| `deep-cleaning` | tipologia ou projeto | horas previstas × preço/hora | **___ €** |
| `construction` | m² ou projeto | nunca abaixo do preço mínimo horário | **___ €/m² ou ___ €** |
| `movein` | tipologia ou projeto | horas previstas × preço/hora | **___ €** |
| `rental-stay` | rotação/tipologia | horas previstas + camas + roupa | **___ €/rotação** |
| `rental-car` | viatura/nível | horas previstas + deslocação | **___ €/viatura** |
| `laundry` | peça, kg, carga ou cesto | tempo + detergente + energia | **___ €/peça, ___ €/kg ou ___ €/carga** |
| `closet` | armário/projeto | horas previstas + materiais | **___ €/projeto** |
| `organization` | divisão/projeto | horas previstas + materiais | **___ €/projeto** |
| `garage` | dia/projeto | horas + descarte + transporte | **___ €/dia/projeto** |
| `holiday` | projeto | horas + montagem/desmontagem; materiais à parte | **___ €/projeto** |
| `staging` | divisão/projeto | horas; compras, mobiliário e fotografia à parte | **___ €/projeto** |

## 5. Produtos e consumíveis

Não existe um kit genérico separado. A Moniquinha decide, na secção 3, a **taxa fixa de produtos de cada serviço**. Essa taxa cobre apenas os produtos e consumíveis normais necessários ao serviço correspondente e é cobrada uma vez, não por hora nem por unidade.

### Outros materiais

- Detergente, amaciador e tira-nódoas da lavandaria: cobertos pela **taxa fixa de produtos da lavandaria**
- Caixas, divisórias, cabides e etiquetas: **cliente compra / Moniquinha compra e refatura**
- Sacos, transporte e taxas de descarte: **incluídos / + ___ €**
- Decoração, iluminação e consumíveis de montagem: **sempre à parte / incluídos até ___ €**
- Acessórios de home staging: **cliente fornece / aluguer ou compra à parte**

## 6. Referências de trabalho para preços fechados

Estas tabelas ajudam a decidir preços alternativos. Não substituem a taxa por hora.

### Airbnb e alojamentos temporários

| Tipologia | Tempo indicativo | Intervalo de trabalho | **Preço fechado decidido** |
|---|---:|---:|---:|
| Quarto / estúdio / T0 | 2–3 h | 40–60 € | **___ €** |
| T1 | 2,5–3,5 h | 45–70 € | **___ €** |
| T2 | 3,5–5 h | 60–90 € | **___ €** |
| T3 | 5–6,5 h | 80–120 € | **___ €** |
| T4+ / moradia | após visita | sob orçamento | **___ € / sob orçamento** |

Extras:

- Fazer camas: **incluído / + ___ € por cama**
- Lavagem de roupa: **incluída / + ___ € por kg ou carga**
- Consumíveis dos hóspedes: **incluídos / custo + ___ % / não incluídos**
- Rotação urgente no próprio dia: **+ ___ % / + ___ €**
- Fotografias de controlo: **incluídas / + ___ €**

### Veículos alugados

| Nível | Conteúdo indicativo | Intervalo de trabalho | **Preço fechado decidido** |
|---|---|---:|---:|
| Rápido | aspiração, superfícies e vidros interiores | 20–30 € | **___ €** |
| Completo | interior + exterior | 30–45 € | **___ €** |
| Sujidade intensa | areia, manchas, pelos ou lixo excessivo | base + 15–30 € | **+ ___ €** |
| SUV / 7 lugares | maior área e duração | base + 5–15 € | **+ ___ €** |

> Confirmar acesso autorizado a água, eletricidade e estacionamento. Não incluir polimento, motor, desmontagem ou tratamento técnico de estofos sem equipamento e seguro adequados.

### Engomadoria por peça

O preço por peça aplica-se à engomadoria. As peças normais custam 1 €; camisas, lençóis e capas de edredão custam 2 €. Peças especiais ou trabalhos que incluam lavagem, secagem ou tratamento de nódoas devem ser avaliados com o cliente.

| Tipo de peça | Serviço | **Preço por peça** | Tempo médio a medir |
|---|---|---:|---:|
| T-shirt / top | engomar | **1 €/peça** | **___ min** |
| Camisa / blusa | engomar | **2 €/peça** | **___ min** |
| Calças / saia | engomar | **1 €/peça** | **___ min** |
| Vestido simples | engomar | **1 €/peça** | **___ min** |
| Casaco normal | engomar | **1 €/peça** | **___ min** |
| Lençol | engomar | **2 €/peça** | **___ min** |
| Fronha | engomar | **1 €/peça** | **___ min** |
| Toalha | engomar | **1 €/peça** | **___ min** |
| Capa de edredão | engomar | **2 €/peça** | **___ min** |
| Edredão, cobertor ou peça delicada | avaliar com o cliente | **sob orçamento** | **___ min** |

Decisões adicionais:

- Quantidade mínima: **___ peças ou ___ €**
- Recolha e entrega: **incluída / + ___ €**
- Peças delicadas ou que exijam limpeza especializada: **sob orçamento / não disponíveis**
- Apenas engomadoria, sem lavagem: **1 €/peça normal; 2 €/camisa, lençol ou capa de edredão**
- Roupa de alojamento local em volume: **preço normal / tabela própria / desconto de ___ %**

### Organização, decoração e home staging

| Serviço | Intervalo de trabalho | **Preço decidido** |
|---|---:|---:|
| Organização de armário | 20–35 €/h; sessão mínima sugerida de 3 h | **___ €/h; mínimo ___ h** |
| Organização do lar | 20–35 €/h | **___ €/h; mínimo ___ h** |
| Garagem/armazém | 20–35 €/h; descarte à parte | **___ €/h; mínimo ___ h** |
| Decoração sazonal simples | 90–250 € + materiais | **___ €/h ou ___ €/projeto** |
| Home staging leve | 180–450 € sem compras, mobiliário ou fotografia | **___ €/h ou ___ €/projeto** |

Os intervalos de decoração e home staging leve são inferências de âmbito reduzido, não preços locais publicados.

## 7. Pacotes

O simulador calcula primeiro todas as horas e extras, depois aplica o desconto do pacote.

| ID | Pacote | Componentes atuais | **Desconto/preço decidido** |
|---|---|---|---:|
| `pkg-weekly` | Brilho Semanal | limpeza regular + lavandaria/engomadoria + organização ligeira | **___ % ou ___ €** |
| `pkg-fresh` | Recomeço | limpeza profunda + organização do lar + armários | **___ % ou ___ €** |
| `pkg-showroom` | Pronto a Mostrar | home staging leve + limpeza profunda | **___ % ou ___ €** |

## 8. Regras comerciais

| Regra | **Decisão Moniquinha** |
|---|---|
| Deslocação incluída | **apenas Óbidos/Caldas / até ___ km** |
| Serviço mínimo geral | **___ h / ___ €** |
| Produtos da Moniquinha | **taxa fixa própria de cada serviço: + ___ €/serviço** |
| Fim de semana | **+ ___ % / sem acréscimo** |
| Feriado | **+ ___ % / indisponível** |
| Urgência inferior a 24 h | **+ ___ % / + ___ €** |
| Cliente semanal | **− ___ %** |
| Cliente quinzenal | **− ___ %** |
| Cancelamento com menos de ___ h | **___ € / ___ %** |
| Sinal para projetos | **___ %** |
| IVA | **incluído / acresce à taxa legal / confirmar enquadramento** |

## 9. Fórmula do futuro simulador

```text
base = preço_base_por_hora × horas_estimadas
base = máximo(preço_mínimo, base)

se a Moniquinha fornecer os produtos:
    subtotal = base + taxa_fixa_de_produtos_do_serviço
senão:
    subtotal = base

estimativa = subtotal
           + extras
           + urgência/fim de semana
           - desconto de recorrência/pacote
```

Para lavandaria cobrada por peça:

```text
total_peças = soma(quantidade_de_cada_tipo × preço_por_peça)
total_peças = máximo(preço_mínimo, total_peças)

se a Moniquinha fornecer os produtos:
    total_peças = total_peças + taxa_fixa_de_produtos_da_lavandaria

estimativa_lavandaria = total_peças + recolha/entrega
```

Se existir preço fechado:

```text
preço_fechado nunca deve ser inferior ao custo horário interno
sem justificação e aprovação da Moniquinha.
```

O resultado mostrado ao cliente deve ser um intervalo estimado e indicar “sujeito a confirmação após fotografias ou visita” nos serviços complexos.

## 10. Fontes consultadas

Consulta efetuada em 13 de julho de 2026:

- [Fixando — Limpeza recorrente nas Caldas da Rainha](https://www.fixando.pt/limpeza-da-casa-recorrente/preco/Leiria/Caldas_da_Rainha)
- [Zaask — Preços de limpeza doméstica](https://www.zaask.pt/quanto-custa/limpeza-de-apartamento)
- [Zaask — Preços de limpeza pós-obra](https://react.zaask.pt/quanto-custa/limpeza-pos-obra)
- [Zaask — Limpeza profunda e engomadoria](https://www.zaask.pt/quanto-custa/empregadas-domesticas)
- [Fixando — Organização da casa em Leiria](https://www.fixando.pt/organizacao-casa/preco/Leiria)
- [Zaask — Home staging](https://www.zaask.pt/quanto-custa/home-staging)
- [Lavandaria da Rainha / CEERDL](https://ceerdl.org/index.php/lavandaria-da-rainha/)
- [AB-House Cleaning — serviços locais](https://abhouseclean.com/index_pt)
- [Ritmo Service — serviços locais](https://www.ritmoservice.pt/)
- [Caldas Detail Garage — serviço automóvel local](https://caldasdetailgarage.pt/)
- [Referência pública de lavagem automóvel](https://www.oa.pt/upl/%7Bcb99866d-7d56-4646-a3fb-9f2251c65f9e%7D.pdf)
- [Referência informal de lavagem automóvel em Leiria](https://www.reddit.com/r/leiria/comments/1m22y28/)

## 11. Antes de implementar o simulador

1. Preencher todos os campos da secção 3.
2. Escolher os preços alternativos que serão visíveis ao cliente.
3. Definir o conteúdo e custo do kit de produtos.
4. Confirmar custos de deslocação, materiais, impostos e tempo não faturado.
5. Testar a tabela com pelo menos três trabalhos reais.
6. Converter as decisões aprovadas numa configuração do simulador.

---

*Documento interno. Não publicar preços enquanto a Moniquinha não os aprovar.*
