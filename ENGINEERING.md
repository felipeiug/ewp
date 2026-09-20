# ENGINEERING — Previsão diária de vazões

## Identificação

- Projeto: Previsão de vazões em estação fluviométrica brasileira
- Responsável: Felipe Emanuel Domiciano Ribeiro
- Data de início: 2026-09-20
- Status: IA GENERATED CONTEXT

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
