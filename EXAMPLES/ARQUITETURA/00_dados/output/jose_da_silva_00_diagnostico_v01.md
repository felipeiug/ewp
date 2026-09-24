# Casa 001 — diagnóstico da etapa 00 — v01

Resultado parcial; DXF e SKP ainda não emitidos. Método: leitura visual do croqui, transcrição das cotas explícitas, conversão por fator 100 e conferência aritmética com as convenções. Não usar dimensões em pixels como medidas.

## Fontes

- ENGINEERING.md; WORKFLOW/STEP_BY_STEP.md.
- REQUISITOS/convencoes.md, unidades.md e restricoes.md.
- 00_dados/input/croqui.jpg; carimbo.png preservado, ainda não diagramado.
- NORMAS/plano_diretor_bh.pdf: 128 páginas; e-book explicativo, apresentação datada de agosto de 2023; extração integral em jose_da_silva_00_referencia_normativa_v01.txt. A leitura inicial não equivale a análise normativa completa.

## Inventário de cotas

| Elemento | Original no croqui (m) | Convertido (cm) |
|---|---|---|
| Largura externa ao fundo | 7,50 | 750 |
| Duas subdivisões superiores | 3,75 + 3,75 | 375 + 375 |
| Extensão direita | 11,50 | 1150 |
| Cadeia esquerda | 3,50 + 3,00 + 1,50 + 3,00 | 350 + 300 + 150 + 300 = 1100 |
| Cadeia direita | 3,50 + 1,50 + 3,00 + 3,50 | 350 + 150 + 300 + 350 = 1150 |
| Dois dormitórios ao fundo, cada | 3,50 × 3,75 | 350 × 375 |
| Dormitório esquerdo central | 3,00 × 3,30 | 300 × 330 |
| Dois banheiros, cada | 1,50 × 3,30 | 150 × 330 |
| Cozinha | 3,00 × 3,30 | 300 × 330 |
| Estar | 3,00 × 4,20 | 300 × 420 |
| Jantar | 3,30 × 3,50 | 330 × 350 |
| Frente, trechos externos | 4,20 + 3,30 | 420 + 330 |

Requisitos documentados: lote 1050 × 2000 cm; pé-direito 300 cm; paredes internas 9 cm, externas 15 cm; rua abaixo; terreno plano simplificado; norte dispensado nesta fase; duas vagas; cobertura com platibanda. Área retangular do lote: 210 m², calculada como 10,50 × 20,00. Implantação e área construída não fixadas.

## Inconsistências e acessos

1. Os dois dormitórios não podem manter 375 cm internos cada em 750 cm externos: 375 + 375 + 15 + 9 + 15 = 789 cm. A convenção já autoriza adaptar essa faixa: se simétrica, largura interna de cada um seria (750 - 30 - 9)/2 = 355,5 cm. Valor calculado, ainda não geometria emitida.
2. O mesmo conflito se repete em profundidade: as cotas internas da cadeia direita somam os mesmos 1150 cm da cota externa, sem reservar paredes. Mesmo com três divisórias simples de 9 cm e duas externas de 15 cm, seriam 1207 cm. Este é um teste aritmético de incompatibilidade, não uma dimensão externa proposta. O ajuste autorizado para os dormitórios não resolve automaticamente cozinha, banheiros e jantar.
3. Os trechos frontais 420 e 330 somam 750 cm externos; não podem simultaneamente representar larguras internas completas sem descontar paredes. Corredor e encontro com o estar precisam ser coordenados.
4. A diferença 1150 - 1100 = 50 cm entre laterais é compatível com o avanço desenhado do jantar. Não foi tratada como erro nem como cota explícita do avanço.
5. O banheiro direito aparece com porta para a lateral externa e sem porta desenhada para o corredor. Não é comprovadamente inacessível: depende de acesso externo e implantação ainda não definidos. Proposta para revisão: transferir acesso ao corredor, sem presumir autorização para alterar o croqui.
6. Corredor, vãos, peitoris e platibanda não têm cotas explícitas. As convenções autorizam escolhas do agente; nenhuma foi aplicada antes do fechamento da geometria. Garagem de duas vagas não aparece no croqui da área construída e precisa ser implantada no lote.

## Situação normativa e formatos

Consulta em 2026-09-24: a PBH disponibiliza parâmetros geográficos e cadastrais no Geosiurbe/BHMap: https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/base-de-dados . Referência do Plano Diretor: https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/plano-diretor/proposta .
Não foram confirmados o lote cadastral, zoneamento, sobrezoneamentos e parâmetros específicos deste endereço. Não adotar recuos, permeabilidade ou coeficientes por suposição; conformidade ainda não verificada.
Formatos exigidos: DXF para AutoCAD 2019 e SKP para SketchUp 2016. Nenhum teste de abertura realizado; disponibilidade de gravador SKP compatível ainda não verificada.

## Decisão necessária

Definir se devem prevalecer as cotas externas (750 × 1150 cm, com o avanço frontal indicado), ajustando medidas internas para acomodar paredes, ou as medidas internas dos ambientes, revisando o contorno externo. A autorização atual para adaptar dormitórios não abrange inequivocamente todos os ambientes.
Após essa decisão, resolver implantação, acesso do banheiro e parâmetros urbanísticos, gerar e validar os arquivos da etapa 00. Etapas 01 e seguintes não iniciadas; dependem das validações e aprovações do workflow.
