

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