# ENGINEERING — Previsão diária de vazões

## Identificação

- Projeto: Previsão de vazões em estação fluviométrica brasileira
- Responsável: Felipe Emanuel Domiciano Ribeiro
- Data de início: 2026-09-20
- Status: INICIAL — CONTEXTO A CONFIRMAR

## Objetivo

Desenvolver e validar um modelo PyTorch para prever a vazão média diária de uma estação da ANA, em horizonte de um dia, usando séries históricas obtidas no HIDROWEB.

## Escopo

Inclui seleção da estação, aquisição e inventário dos dados, controle de qualidade, preparação de janelas temporais, treinamento de uma LSTM, comparação com persistência e avaliação fora da amostra.

Não inclui previsão operacional em tempo real, emissão de alertas, operação de reservatórios ou declaração de segurança para tomada de decisão.

## Restrições e referências

- Requisitos: `REQUISITOS/`.
- Procedimento técnico: `NORMAS/input/NT-001_previsao_vazoes.tex`.
- Fonte hidrológica: ANA, HIDROWEB e Hidro Webservice.
- Dados originais devem permanecer em diretórios `input/`.

## Entradas

- Código da estação fluviométrica: A CONFIRMAR.
- Série histórica exportada do HIDROWEB: PENDENTE.
- Período de análise: A CONFIRMAR após inspeção da disponibilidade.
- Variáveis auxiliares, como precipitação: opcionais e sujeitas a registro de proveniência.

## Entregáveis

- inventário e proveniência dos dados;
- série diária tratada e relatório de qualidade;
- modelo, parâmetros, métricas e previsões;
- comparação com persistência;
- relatório de validação e limitações.

## Critérios de aceitação

1. Separação temporal sem embaralhamento entre treino, validação e teste.
2. Normalização ajustada apenas com o treino.
3. Comparação com persistência no mesmo período de teste.
4. Registro de RMSE, MAE e NSE, unidades e período avaliado.
5. Código testado e execução reproduzível a partir das entradas registradas.
6. Nenhuma lacuna, dado suspeito ou transformação ocultada.

## Step by Step

### 00 — Planejamento

- Entrada: objetivo, estação candidata e horizonte.
- Saída: escopo aprovado em `00_planejamento/output/`.
- Validação: confirmar estação, variável-alvo e horizonte.
- Gate: aprovação do responsável antes da aquisição definitiva.

### 01 — Aquisição e inventário

- Dependência: etapa 00 aprovada.
- Entrada: exportação original do HIDROWEB em `01_dados/input/`.
- Saída: inventário, checksum e proveniência em `01_dados/output/`.
- Validação: estação, unidade, período, frequência e campos de consistência.
- Gate: série e proveniência aceitas.

### 02 — Controle de qualidade e preparação

- Dependência: etapa 01 validada.
- Entrada: dados inventariados.
- Saída: `02_preprocessamento/output/vazoes_diarias.csv` e relatório de qualidade.
- Validação: duplicidades, datas ausentes, valores inválidos e regra documentada para lacunas.
- Gate: tratamento aprovado; lacunas não podem ser preenchidas silenciosamente.

### 03 — Modelagem

- Dependência: etapa 02 aprovada.
- Entrada: série diária tratada.
- Saída: pesos, configuração, previsões e métricas em `03_modelagem/output/`.
- Validação: ausência de vazamento temporal e comparação com persistência.
- Gate: modelo e execução revisados.

### 04 — Validação e encerramento

- Dependência: etapa 03 revisada.
- Entrada: previsões, observações e artefatos do modelo.
- Saída: relatório em `04_validacao/output/`.
- Validação: critérios de aceitação, limitações e rastreabilidade.
- Gate: aprovação técnica para concluir o projeto.

### 05 — Relatório Final

- Gere o relatrório com o compilado de tudo que foi realizado em um arquivo .tex.

## Informações a confirmar

- estação e bacia;
- período útil da série;
- horizonte adicional;
- política para lacunas e dados qualificados pela ANA;
- ambiente computacional de referência.

## Próximos passos

Executar a etapa 00 e registrar a seleção da estação. As etapas posteriores permanecem condicionadas aos gates acima.

## Histórico

- 2026-09-20 — Estrutura criada e fluxo inicial definido para previsão de vazões.
- 2026-09-20 — Norma técnica migrada para LaTeX.
