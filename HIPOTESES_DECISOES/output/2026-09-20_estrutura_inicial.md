# Estrutura inicial e decisões de modelagem

Data e fuso: 2026-09-20, America/Sao_Paulo.

## Decisões iniciais

- Framework: PyTorch.
- Modelo candidato: LSTM univariada.
- Alvo: vazão média diária em `m³/s`.
- Horizonte inicial: um dia.
- Referência mínima: persistência.
- Métricas: RMSE, MAE e NSE.

## Hipóteses a validar

- A estação selecionada terá extensão e continuidade adequadas.
- A frequência diária e a vazão estarão disponíveis na exportação.
- A janela de 30 dias será revisada na modelagem.

Essas hipóteses não substituem a inspeção dos dados nem os gates do `ENGINEERING.md`.
