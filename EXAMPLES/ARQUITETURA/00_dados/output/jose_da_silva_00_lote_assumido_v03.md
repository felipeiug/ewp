# Casa 001 — lote assumido — revisão documental 03

## Premissa vigente

Usuário autorizou dispensar identificação cadastral e considerar o projeto viável no local informado, com lote de 1050 × 2000 cm. Registro: `HIPOTESES_DECISOES/output/2026-09-24_1640_lote_assumido.md`. Não solicitar novamente cadastro para avançar no estudo. Conformidade urbanística específica não verificada.

Este adendo supera exclusivamente a exigência cadastral e o impedimento correspondente nos documentos v02. Preserva as cotas externas, o croqui e a geometria da casa. A revisão 03 é documental e de conferência do lote; os arquivos editáveis vigentes continuam sendo `jose_da_silva_00_planta_v02.dxf` e `jose_da_silva_00_paredes_v02.skp`.

## Conferência

- Lote: 1050 × 2000 cm, 210 m²; casa: contorno externo de 84,15 m², conforme JSON v02.
- Casa posicionada para teste em x=150…900, y=550…1700 cm; laterais 150 cm, fundos 300 cm e frente mínima 550 cm. Frente do estar a 600 cm por causa do avanço de 50 cm do jantar.
- Duas reservas de vagas de 250 × 500 cm: x=175…425 e x=450…700, ambas em y=25…525. Contidas no lote e sem sobreposição entre si ou com a casa.
- Distâncias são escolhas geométricas para o estudo, não parâmetros legais confirmados. Sem dimensionamento de muros, portões, cobertura da garagem ou validação de trajetórias e circulação de pedestres.
- Esquema mostra projeções de paredes sem detalhar vãos; consultar DXF/SKP v02 para os acessos. O banheiro direito mantém o acesso externo, com faixa lateral disponível.

## Validação e continuidade

Script `jose_da_silva_00_lote_assumido_v03.py` executado com verificações de contenção, não sobreposição e área. Hashes dos sete derivados v02 comparados com o relatório anterior: preservados. Evidências em `jose_da_silva_00_lote_assumido_validacao_v03.json`; prévia PNG na mesma pasta.

Mantidos os testes geométricos e de arquivos v02: DXF auditado; SKP reaberto pela biblioteca do SketchUp 2016. Testes nas interfaces gráficas continuam pendentes para aceitação final; não são apresentados como realizados.

Etapa 00 com entregáveis disponíveis para revisão do estudo, sem impedimento cadastral. Próxima transição: aprovação da etapa 00, exigida por `WORKFLOW/STEP_BY_STEP.md`, antes de 01 — Render 3D. Esta autorização sobre o lote não foi registrada como aprovação de desenhos ou como liberação para obra.
