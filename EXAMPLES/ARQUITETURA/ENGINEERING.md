# ENGINEERING — Projeto arquitetônico completo

## Identificação

- Projeto: Casa 001
- Responsável: Felipe Emanuel Domiciano Ribeiro
- Data de início: 2026-09-24
- Cliente: José da Silva
- Endereço: Rua Oliveira - N° 1356. Bairro Cruzeiro. Belo Horizonte - MG CEP: 30310-150


- Status: ATIVO
- Justificativa atual (2026-09-24): etapa 00 aprovada pelo usuário para iniciar a etapa 01 — modelo 3D com mobiliário e imagens por IA. Local e lote de 1050 × 2000 cm assumidos para o estudo; identificação cadastral dispensada e conformidade urbanística específica não verificada. Projeto ATIVO.
- Justificativa inicial preservada (2026-09-24): contexto e geometria ainda possuem lacunas; nenhuma etapa técnica aprovada. O diagnóstico documental não representa conclusão da etapa 00.

## Objetivo

Você deve atuar como arquiteto/engenheiro e, a partir de um croqui com medidas, você deverá gerar:
- A plata baixa e cortes para o autocad;
- O projeto arquitetônico completo em 3D para o sketchup;
- As plantas em folha A1 no formato PDF.

## Escopo

Realizar a interpretação do Croquí em `00_dados/input/croqui.jpg`, cujas cotas explícitas estão em metros (conversão para centímetros registrada na etapa 00) e, a partir dele, desenvolver o que é pedido.

O croquí trata-se de uma residência de medio-alto padrão e está em metros, porém não fica em um condomínio então as medidas de segurança devem ser respeitadas dado a localização do imóvel.
O croqui apresenta os dados em metros, porém neste projeto tudo devera ser cotado em centímetros, inclusive o projeto em 3D no sketchup.

Não inclui aprovação legal automática, levantamento topográfico, sondagem, projeto estrutural, instalações prediais, orçamento executivo ou responsabilidade técnica de execução e informações específicas para essas disciplinas.


## Entradas

- Croqui feito à mão com medidas: `00_dados/input/croqui.jpg`;
- Tipo de edificação e uso: Disponível em `REQUISITOS/convencoes.md`;
- Dimensões e orientação do lote, níveis e topografia: Disponível em `REQUISITOS/convencoes.md`;
- Metregem construida, área verde, espaçamentos das bordas do lote em `NORMAS/plano_diretor_bh.pdf`;
- Programa de necessidades, preferências de materiais e padrão de representação: `REQUISITOS/convencoes.md`;
- A versão do Sketchup é a de 2016 e a do AutoCAD de 2019.

Caso as medidas do croqui não estejam condizentes peça para que o usuário explique quais medidas devem ser consideradas.

## Entregáveis

- registro do croqui de entrada, inventário de medidas;
- plantas baixas, cortes, fachadas e detalhes em arquivos editáveis do AutoCAD;
- modelo 3D coordenado em arquivo editável do SketchUp;
- pranchas diagramadas e versões finais em PDF;
- relatório de compatibilização, revisões, limitações e arquivos entregues.

## Critérios de aceitação

1. Todas as cotas usadas no desenho estão rastreáveis ao croqui ou a uma decisão registrada.
2. Plantas, cortes, fachadas e modelo 3D usam a mesma versão de medidas, níveis e nomenclatura.
3. Arquivos editáveis do AutoCAD e SketchUp abrem no ambiente de referência e mantêm escala, unidades, layers/tags e referências necessárias.
4. PDFs finais têm pranchas legíveis, carimbo, escala gráfica ou numérica, norte quando aplicável, revisão e identificação do projeto.
5. Nenhuma medida ausente, inferência de projeto ou incompatibilidade é ocultada e deve, obrigatóriamente, ser solicitada ao usuário.
6. Os entregáveis finais são reproduzíveis a partir do croqui, decisões registradas e arquivos-fonte preservados.

## Step by Step

A sequência detalhada permanece em `WORKFLOW/STEP_BY_STEP.md`, incorporada por referência, sem alteração de suas etapas:

1. 00 — Dados: conferir croqui, requisitos e legislação; resolver inconsistências; gerar DXF e SKP de paredes; validar uso, local, lote, orientação, níveis, medidas e formatos.
2. 01 — Render 3D: somente após aprovação da etapa 00, usar seus DXF/SKP e validar ambientes, fluxos, áreas e premissas.
3. 02 — Desenvolvimento 2D: após a etapa anterior na sequência e com etapa 00 aprovada; usar a mesma geometria e validar desenhos e adequação normativa.
4. 03 — Compatibilização: somente com 01 e 02 revisadas; conferir conjunto e PDFs.
5. 04 — Relatório: somente com 03 aprovada; conferir fontes e entregáveis.

## Histórico — 2026-09-24_161919 (America/Sao_Paulo)

- START: estrutura mínima complementada conforme instruções diretas do usuário; fontes preservadas. Divergências com `.github/agents/EWP.agent.md` registradas em `HIPOTESES_DECISOES/output/2026-09-24_161919_start.md`.
- Etapa 00 parcialmente executada: inventário e diagnóstico em `00_dados/output/jose_da_silva_00_diagnostico_v01.md`. Geometria depende da decisão sobre cotas conflitantes; nenhuma aprovação presumida.
- Status do projeto mantido: INICIAL — CONTEXTO A CONFIRMAR. Próximo passo: resolver cotas, conferir implantação e parâmetros do lote, produzir e validar DXF/SKP.

## Histórico — 2026-09-24_1631 (America/Sao_Paulo)

- Determinação do usuário: prevalecem sempre as cotas externas; ajustar as internas conforme necessário. Substitui a exigência conflitante de conservar todas as medidas internas; registro em `HIPOTESES_DECISOES/output/2026-09-24_1631_prioridade_cotas_externas.md`.
- Atualizado somente o requisito correspondente em `REQUISITOS/convencoes.md`, com histórico preservado no registro acima. Croqui, carimbo, normas, unidades, restrições e workflow preservados.
- Gerados `00_dados/output/jose_da_silva_00_planta_v02.dxf` e `00_dados/output/jose_da_silva_00_paredes_v02.skp`, com fonte geométrica, scripts, memorial, prévias e validação v02 na mesma pasta.
- Status alterado de INICIAL — CONTEXTO A CONFIRMAR para ATIVO: execução técnica iniciada após a decisão dimensional. Etapa 00 parcial, em revisão; etapas posteriores não iniciadas.
- Próximo passo: conferir enquadramento cadastral/urbanístico e implantação com duas vagas, validar aberturas e realizar testes nas interfaces dos aplicativos; submeter o conjunto da etapa 00 à aprovação prevista no workflow. A aprovação da prioridade dimensional não representa aprovação dos entregáveis.

### Adendo — 2026-09-24_1636 (America/Sao_Paulo)

Após o usuário autorizar a busca pelo lote, consulta à base oficial de endereços da PBH não retornou correspondência para Rua Oliveira, 1356, nem para CEP 30310150 com esse número. Evidências e limitações em `HIPOTESES_DECISOES/output/2026-09-24_1636_consulta_lote.md`. A identificação cadastral permanece pendente; nenhum lote alternativo ou parâmetro urbanístico foi presumido. Correção dimensional e arquivos v02 disponíveis para revisão.

### Adendo — 2026-09-24_1640 (America/Sao_Paulo)

- Usuário dispensou a identificação do lote e determinou assumir que o projeto pode ocorrer no local com as dimensões informadas. Superada a pendência cadastral como condição de avanço do estudo; histórico anterior preservado. Registro: `HIPOTESES_DECISOES/output/2026-09-24_1640_lote_assumido.md`.
- Atualizados pontualmente `REQUISITOS/convencoes.md` e a validação da etapa 00 em `WORKFLOW/STEP_BY_STEP.md`. Nenhuma norma alterada; conformidade específica não declarada.
- Conferência de encaixe e reserva de duas vagas em `00_dados/output/jose_da_silva_00_lote_assumido_v03.md` e respectiva prévia PNG. Revisão documental v03 utiliza os DXF/SKP v02 sem mudar a geometria da casa.
- Próximo passo: revisão e aprovação da etapa 00 para iniciar 01 — Render 3D. Não repetir a solicitação de cadastro. Os testes de abertura nas interfaces dos aplicativos permanecem indicados para a aceitação final.

### Adendo — 2026-09-24_1802 (America/Sao_Paulo)

- Etapa 00 aprovada expressamente pelo usuário: “Sim, pode fazer.” Autorizado iniciar modelo 3D com mobiliário e ambientação e as duas imagens por IA da etapa 01.
- Registro da aprovação e premissas: `HIPOTESES_DECISOES/output/2026-09-24_1802_aprovacao_00_estudo_01.md`. Modelo da casa mantém contorno e paredes v02. Implantação preliminar deslocada 50 cm para o fundo para acomodar passagem pedonal, mantendo lote e dimensões da casa.
- Área de trabalho: `01_estudo_preliminar/`; fontes da etapa 00 preservadas. Não solicitar novamente aprovação da etapa 00 ou identificação cadastral.
