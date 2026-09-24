# Casa 001 — etapa 00 — revisão 02

Situação: ajuste dimensional executado; etapa 00 parcial, para revisão. Não liberado para obra nem apresentado como projeto legal. A autorização para ajustar medidas não constitui aprovação da etapa.

## Decisão e fontes

Prevalecem as cotas externas, por instrução expressa do usuário em 2026-09-24. Registro: `HIPOTESES_DECISOES/output/2026-09-24_1631_prioridade_cotas_externas.md`.

Fontes: `00_dados/input/croqui.jpg`, `ENGINEERING.md`, `REQUISITOS/convencoes.md`, `unidades.md`, `restricoes.md`, `WORKFLOW/STEP_BY_STEP.md` e `NORMAS/plano_diretor_bh.pdf`. Carimbo preservado para a etapa de pranchas. O diagnóstico v01 permanece como histórico do conflito anterior à decisão.

## Critério geométrico

Coordenadas em centímetros: x=0 na face externa esquerda; y=0 na frente do jantar; z=0 no piso de referência; rua em y negativo. Conversões: cotas originais em m × 100 = cm; gravação interna do SketchUp em polegadas = cm / 2,54, com exibição configurada para cm.

Contorno externo: (0,50), (420,50), (420,0), (750,0), (750,1150), (0,1150). Mantidos 750 cm de largura, 1150 cm à direita, 1100 cm à esquerda e trechos frontais de 420/330 cm. Avanço do jantar calculado em 50 cm. Área geométrica encerrada pelo contorno: (750 × 1150 - 420 × 50)/10000 = 84,15 m²; não equivale a área computável legal verificada.

Intermediárias longitudinais do croqui interpretadas como eixos das divisórias: y=350/500/800 à esquerda e y=350/650/800 à direita. As faces externas das extremidades permanecem fixas. Esta referência de eixo é uma decisão de representação explicitada, pois o croqui não resolve as espessuras.

Paredes externas 15 cm, internas 9 cm e altura 300 cm. Corredor livre entre x=320 e x=420, com 100 cm de largura; fundo do vestíbulo em y=900 cm. Divisória entre dormitórios posteriores centrada em x=375 cm. A largura máxima de cada um resulta em (750 - 2 × 15 - 9)/2 = 355,5 cm. A profundidade máxima é 1150 - 15 - (800 + 4,5) = 330,5 cm. Os recortes retiram área dos retângulos máximos.

## Ambientes fechados

Dimensões antigas transcritas do texto do croqui, sem uniformizar sua ordem. Dimensões novas em x × y; áreas calculadas pelos polígonos livres, sem soleiras. Nos dormitórios posteriores, as dimensões são do retângulo envolvente e a área já desconta o recorte de acesso.

| Ambiente | Texto anterior (cm) | Dimensões novas (cm) | Área livre (m²) |
|---|---|---|---|
| Dormitorio 1 | 350 x 375 | 355.5 × 330.5 | 11.1275 |
| Dormitorio 2 | 350 x 375 | 355.5 × 330.5 | 11.2320 |
| Dormitorio 3 | 300 x 330 | 296 × 291 | 8.6136 |
| Banheiro 1 | 150 x 330 | 296 × 141 | 4.1736 |
| Banheiro 2 | 150 x 330 | 306 × 141 | 4.3146 |
| Cozinha | 300 x 330 | 306 × 291 | 8.9046 |

Estar e jantar permanecem integrados à circulação, sem parede divisória adicionada. Faixa do estar: x=15…420, y=65…345,5, correspondente a 405 × 280,5 cm. Faixa do jantar: x=420…735, y=15…345,5, com desconto da parede do avanço de x=420…435 até y=65; largura junto à fachada de 300 cm e no trecho interno de 315 cm. Essas faixas são referências de uso, sem áreas legais independentes atribuídas.

Área interna geométrica total, excluindo projeções de paredes e soleiras: 75.6069 m². A circulação continua dentro dessa área; não somar novamente as faixas de uso.

## Vãos escolhidos pelo agente

Posições exatas em `jose_da_silva_00_geometria_v02.json`. Dimensões abaixo são vãos geométricos livres, não medidas comerciais de folhas. Portas, janelas e materiais de esquadrias não são sólidos do SKP nesta etapa de paredes; as portas têm representação simbólica no DXF.

| Vão | Uso | Largura × altura (cm) | Base acima do piso (cm) |
|---|---|---|---|
| P01 | Entrada principal | 90 × 210 | 0 |
| P02 | Dormitorio 1 | 80 × 210 | 0 |
| P03 | Dormitorio 2 | 80 × 210 | 0 |
| P04 | Dormitorio 3 | 80 × 210 | 0 |
| P05 | Banheiro 1 | 80 × 210 | 0 |
| P06 | Banheiro 2: acesso externo preservado | 80 × 210 | 0 |
| P07 | Cozinha | 80 × 210 | 0 |
| J01 | Dormitorio 1 | 120 × 120 | 90 |
| J02 | Dormitorio 2 | 120 × 120 | 90 |
| J03 | Dormitorio 3 | 120 × 120 | 90 |
| J04 | Banheiro 1: alta | 60 × 60 | 180 |
| J05 | Banheiro 2: bandeira acima da porta | 80 × 60 | 220 |
| J06 | Cozinha | 150 × 110 | 110 |
| J07 | Estar | 160 × 120 | 90 |
| J08 | Jantar | 180 × 120 | 90 |
| V01 | Abertura cozinha/jantar do croqui | 140 × 100 | 110 |

O banheiro 2 mantém o acesso externo do croqui; depende de passagem lateral na implantação. A bandeira acima da porta é proposta do agente, não cota observada. Janelas altas são indicadas por projeção na prévia. Abertura V01 representa o vão entre cozinha e jantar, não ventilação direta ao exterior. Ventilação efetiva, iluminação, segurança, acessibilidade e dimensionamento de vergas ainda não foram validados; a geometria não constitui dimensionamento estrutural.

## Lote e conferência urbanística

Lote informado de 1050 × 2000 cm = 210 m². A casa deixa uma diferença dimensional de 300 cm na largura e 850 cm no comprimento, antes de definir implantação e muros. Como teste de encaixe, uma distribuição de 150 cm em cada lateral e 550 cm à frente / 300 cm atrás fecha essas dimensões. São valores hipotéticos de teste, não recuos legais adotados.

Dois envelopes hipotéticos de veículos de 250 × 500 cm cabem lado a lado na faixa frontal desse teste; isto não valida garagem, manobras, portões, passeio, cobertura ou área permeável. A posição final da casa e as duas vagas ainda dependem da conferência do lote. Não foi iniciada a planta de implantação da etapa 02.

A [PBH indica Geosiurbe/BHMap para consulta cadastral e dos parâmetros geográficos](https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/base-de-dados). A [página oficial do Plano Diretor](https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/plano-diretor/proposta), consultada em 2026-09-24, distingue o texto legal dos e-books explicativos. O e-book local não identifica sozinho as condições específicas do lote. Após autorização do usuário para buscar pelo lote, foi consultado o serviço WFS publicado na [página oficial de acesso aos dados](https://prefeitura.pbh.gov.br/bhgeo/acesso-aos-dados): 43 registros de endereço da Rua Oliveira no Cruzeiro, nenhum com número 1356; a pesquisa alternativa por CEP 30310150 e número 1356 também retornou zero registros. Isso não prova inexistência do imóvel, mas impede identificá-lo com os dados atuais. Evidências integrais, filtros e horários preservados em `consulta_lote_v02/`. Não inferir zoneamento pelo bairro nem escolher lote por similaridade de área. Registro: `HIPOTESES_DECISOES/output/2026-09-24_1636_consulta_lote.md`.

Pendente: índice cadastral do IPTU ou identificação de zona/quadra/lote para consulta confiável; depois verificar recuos, ocupação, permeabilidade, eventuais restrições e aberturas. Nenhum valor normativo foi inventado e nenhuma conformidade legal é declarada.

## Arquivos, método e testes

- `jose_da_silva_00_planta_v02.dxf`: DXF AC1027, modelspace em cm, paredes, símbolos de vãos, ambientes e cotas de conferência. Para abertura no AutoCAD 2019; não testado pela interface do AutoCAD.
- `jose_da_silva_00_paredes_v02.skp`: formato SketchUp 2016, 16 grupos de paredes, layers e materiais; sem faces ou arestas soltas na raiz. Sem pisos, mobiliário e cobertura, conforme saída de paredes da etapa 00.
- `jose_da_silva_00_geometria_v02.json`: fonte comum de coordenadas, ambientes, vãos e malhas.
- `jose_da_silva_00_conferencia_planta_v02.png` e `jose_da_silva_00_conferencia_3d_v02.png`: prévias técnicas calculadas da mesma fonte; não são os renders por IA da etapa 01 nem pranchas finais.
- `jose_da_silva_00_conferencia_dxf_v02.png`: visualização do próprio DXF reaberto, usada para conferir sua representação e os textos de cotas.
- `jose_da_silva_00_validacao_v02.json`: resultados e hashes das fontes/saídas; versões das ferramentas.
- Scripts `jose_da_silva_00_gerar_v02.py` e `jose_da_silva_00_skp_api_v02.py`: geração reproduzível. ezdxf 1.4.4 instalado apenas em `00_dados/output/ferramentas/python`; demais versões no relatório de validação. Biblioteca SketchUpAPI 16.1.1449 da instalação local.

Reprodução a partir da raiz: `python 00_dados/output/jose_da_silva_00_gerar_v02.py`. Regenera os derivados v02; para uma nova decisão emitida, criar nova revisão antes de alterar parâmetros. Não executar o script de diagnóstico v01 para gerar a geometria.

Testes executados: contorno e espessuras; ausência de sobreposição volumétrica entre paredes; vãos contidos e sem colisão entre si; cada malha fechada e volume orientado coerente; DXF reaberto sem erros/reparos e seção a 120 cm idêntica à fonte; textos de todas as cotas comparados numericamente com suas medidas em cm (fator de exibição explicitamente 1); SKP salvo e reaberto pela biblioteca 2016, limites 750 × 1150 × 300 cm, cm como unidade exibida e duas faces por aresta de cada grupo. Inspeção visual das prévias e da visualização do DXF. Testes pela interface gráfica dos aplicativos permanecem pendentes.

## Continuidade

A correção dimensional está concluída nesta revisão. A etapa 00 permanece parcial, com conferência cadastral/urbanística, implantação e revisão dos entregáveis pendentes. Somente depois de satisfeitas as validações e aprovada a etapa 00 executar as etapas seguintes, conforme `WORKFLOW/STEP_BY_STEP.md`. A solicitação de dados cadastrais não altera as cotas externas nem reabre a decisão já autorizada.
