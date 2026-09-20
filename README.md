# EWP — Exemplo de previsão de vazões

Este repositório demonstra o Engineering Workspace Protocol (EWP) em um projeto de previsão diária de vazões com PyTorch e séries históricas da ANA/HIDROWEB.

O fluxo oficial está em [`ENGINEERING.md`](ENGINEERING.md). Requisitos, normas, decisões, entradas e resultados permanecem separados para garantir rastreabilidade e reprodução.

## Estrutura

- `.github/agents/EWP.agent.md`: definição do agente EWP.
- `ENGINEERING.md`: estado, escopo e sequência obrigatória.
- `REQUISITOS/`, `NORMAS/` e `HIPOTESES_DECISOES/`: governança técnica.
- `00_planejamento/` a `04_validacao/`: etapas com entradas preservadas e saídas rastreáveis.
- `src/ewp_vazoes/`: pipeline de modelagem.
- `tests/`: verificações automatizadas.

## Execução

```bash
python -m venv .venv
pip install -e .
pytest
python -m ewp_vazoes.train --input 02_preprocessamento/output/vazoes_diarias.csv --output 03_modelagem/output
```

O treinamento depende de uma série aprovada nas etapas anteriores. Dados observados não são versionados neste repositório.
