# ENGINEERING — Projeto arquitetônico completo

## Identificação

- Projeto: Casa 001
- Responsável: Felipe Emanuel Domiciano Ribeiro
- Data de início: 2026-09-24
- Cliente: José da Silva
- Endereço: Rua Oliveira - N° 1356. Bairro Cruzeiro. Belo Horizonte - MG CEP: 30310-150


- Status: INICIAL — CONTEXTO A CONFIRMAR
- Justificativa (2026-09-24): contexto e geometria ainda possuem lacunas; nenhuma etapa técnica aprovada. O diagnóstico documental não representa conclusão da etapa 00.

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

## Histórico

- 2026-09-20 — Estrutura criada e fluxo inicial definido para previsão de vazões.
- 2026-09-24 — Escopo alterado para projeto arquitetônico completo com entregáveis SketchUp, AutoCAD e PDF.

## Pendências e próximo passo — 2026-09-24

- Consultar `00_dados/output/jose_da_silva_00_diagnostico_v01.md` e o inventário correspondente.
- Confirmar unidade dos níveis, orientação, implantação, paredes, vãos e referências das cotas; obter identificação cadastral e parâmetros urbanísticos do lote.
- Disponibilidade do executável não comprova licença, funcionamento ou abertura de entregáveis.
- Permanecer na etapa 00; próximos desenhos dependem das respostas e dos testes de ferramentas.
- Os diretórios das etapas posteriores serão criados apenas ao atingir cada etapa.

### Adendo ao histórico — 2026-09-24

Regularização estrutural e diagnóstico autorizados pelo usuário. O Step by Step foi incorporado neste documento; o fluxo externo foi identificado como histórico. Corrigidos caminhos para `00_dados`; novas dependências de 03 e 04 permanecem propostas. Os requisitos originais e o croqui foram preservados. Nenhuma aprovação de etapa foi inferida.
