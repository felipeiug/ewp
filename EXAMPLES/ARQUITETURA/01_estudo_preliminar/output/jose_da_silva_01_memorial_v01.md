# Casa 001 — estudo preliminar 3D — revisão 01

## Aprovação, fontes e escopo

Etapa 00 aprovada pelo usuário em 2026-09-24 para iniciar a etapa 01. Fonte e decisões em `HIPOTESES_DECISOES/output/2026-09-24_1802_aprovacao_00_estudo_01.md`. Identificação cadastral dispensada anteriormente; não é pendência para continuar o estudo. A conformidade urbanística específica permanece não verificada.

Modelo produzido a partir do próprio `00_dados/output/jose_da_silva_00_paredes_v02.skp`, com suas 16 paredes em grupos preservados, transladados no lote sem escala ou rotação. Planta `jose_da_silva_00_planta_v02.dxf` e geometria JSON v02 mantidas como referências coordenadas. Fontes originais e versões anteriores preservadas; hashes no relatório de validação.

Este é um estudo arquitetônico editável. Não inclui projeto estrutural, instalações, detalhamento de impermeabilização, desempenho das esquadrias, orçamento ou liberação executiva.

## Geometria e implantação

- Lote: 1050 × 2000 cm. Casa: 750 × 1150 cm, com avanço frontal de 50 cm do jantar e contorno de 84,15 m². Paredes externas 15 cm e internas 9 cm, pé-direito 300 cm.
- Origem da casa no lote: x=150, y=600 cm. A implantação preliminar avançou 50 cm para o fundo em relação ao esquema v03 da etapa 00, para acomodar passagem de pedestres. Laterais 150 cm; fundos 250 cm; frente mínima 600 cm e frente do estar 650 cm.
- Reserva de duas vagas de 250 × 500 cm, com dois veículos volumétricos indicativos. Carros não são modelos de fabricantes. Nenhuma simulação de trajetória veicular é alegada.
- Portão de pedestres à esquerda e caminho nominal de 100 cm, separado das vagas até a porta principal; faixa externa direita preservada para acesso ao banheiro 2. Os testes verificam encaixe em planta e ausência de sobreposição, sem certificar acessibilidade normativa.
- Pisos no nível de referência 0,00 m, terreno plano assumido. Espessuras dos volumes de base são de representação e não dimensionamento de laje/fundação.

## Mobiliário e acabamentos

Peças paramétricas organizadas em grupos de objetos e subgrupos de componentes, sem dependência de bibliotecas externas de móveis. Medidas exatas, partes e materiais em `jose_da_silva_01_geometria_v01.json`.

| Ambiente | Conteúdo do estudo |
|---|---|
| Dormitório 1, ao fundo à esquerda | Duas camas de 90 × 188 cm, armário de 190 × 55 cm e criado central |
| Dormitório 2, ao fundo à direita | Cama de 158 × 198 cm, armário de 210 × 55 cm e dois criados |
| Dormitório 3, central à esquerda | Cama de 138 × 188 cm e armário lateral de 55 × 130 cm |
| Dois banheiros | Box, painel de vidro, ducha, vaso com caixa acoplada, bancada, cuba, torneira e espelho |
| Cozinha | Bancada com pia e cooktop, armários, coifa, geladeira e bancada de apoio |
| Estar | Sofá, tapete, mesa de centro e rack com TV |
| Jantar | Mesa de 80 × 150 cm e seis cadeiras |

No dormitório 3, a passagem entre cama e armário tem 68 cm; o espaço de 30 cm no lado oposto da cama não foi considerado circulação principal. O arranjo é compacto e deve ser revisado se houver exigência de acesso amplo pelos dois lados. Os giros das sete portas não interceptam as projeções dos móveis cadastrados.

Acabamentos propostos: madeira clara nos dormitórios e marcenaria, cinza claro nos pisos sociais, branco quente nas paredes, tecidos neutros com detalhes azul e oliva, metais em grafite. Materiais do SKP são cores/opacity editáveis; não são texturas comerciais ou especificações de compra.

Janelas mantêm os vãos definidos na etapa 00; esquadrias e vidros acrescentados. Portas representadas abertas a 90° para leitura do arranjo. O passa-pratos não foi tratado como abertura externa para ventilação. Os vãos, marcos e folhas são representação preliminar e dependem de detalhamento posterior.

## Cobertura, fachada e ambiente externo

Platibanda até 360 cm; cobertura oculta representada com inclinação de estudo de 3%, sem ultrapassar a platibanda. Forro e espessuras são volumes geométricos preliminares. Inclinação, estrutura, isolamento, drenagem e impermeabilização dependem de desenvolvimento técnico; não se declara que um produto específico admite os valores escolhidos.

Garagem com cobertura metálica representativa a aproximadamente 250 cm; fechamento perimetral e portões com 210 cm. Acesso veicular de 580 cm e acesso pedonal de 100 cm. Fechamento e controle de acessos incorporados ao estudo, sem alegação de certificação de segurança. Árvores de pequeno porte ao fundo e arbustos baixos nas áreas livres.

## Modelo e cenas

Arquivo principal: `jose_da_silva_01_mobiliado_v01.skp`, salvo no formato SketchUp 2016, com unidades exibidas em centímetros.

1. `01_Interiores_axonometria`: interior mobiliado, com camadas de cobertura, fechamento e cobertura de garagem ocultas.
2. `02_Planta_mobiliada`: vista de cima, com coberturas ocultas.
3. `03_Fachada`: conjunto externo com cobertura e fechamento.

Ao abrir o arquivo, o estado inicial destaca interiores. As coberturas e muros existem no arquivo e podem ser mostrados pelas cenas/camadas. Nomenclatura de 2016: layers. Não há objetos soltos na raiz fora de grupos.

## Validação

Executados: contenção do mobiliário nos ambientes; comparação entre projeções dos 29 itens principais; giros de portas; caminho pedonal separado das vagas; conferência das dimensões globais; preservação das fontes; gravação e reabertura pela biblioteca SketchUpAPI 16.1.1449; verificação de duas faces por aresta em cada grupo sólido; contagem de cenas, layers e materiais.

Resultados geométricos detalhados: `jose_da_silva_01_validacao_v01.json`. Abertura e alternância das cenas na interface gráfica do SketchUp ainda não foram testadas pelo agente. Nenhum teste na interface do AutoCAD é alegado nesta etapa.

Referências geométricas PNG foram calculadas para orientar a IA. A vista superior usa corte analítico de paredes a 120 cm; a fachada usa projeção com teste de profundidade. Não substituem as duas imagens por IA solicitadas. Prompts exatos e método: `jose_da_silva_01_prompts_ia_v01.json`; imagens por IA terão verificação visual registrada separadamente. Sua aparência pode variar e não substitui medidas do SKP/DXF.

## Reprodução e continuidade

Scripts `jose_da_silva_01_gerar_v01.py`, `jose_da_silva_01_skp_v01.py` e `jose_da_silva_01_vistas_v01.py`, com reutilização do auxiliar de API preservado em `00_dados/output/`. Executar a partir da raiz: `python 01_estudo_preliminar/output/jose_da_silva_01_gerar_v01.py`. Gera modelo e referências; as imagens por IA são resultados não determinísticos de chamadas separadas e seus prompts ficam registrados.

O gerador cria derivados v01; preservar uma revisão emitida antes de mudar parâmetros. A etapa 01 será considerada entregue após persistência e conferência das duas imagens por IA. Próxima etapa do projeto: desenvolvimento 2D coordenado, seguindo o workflow, sem emitir pranchas finais antecipadamente.
