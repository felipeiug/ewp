# Unidades e referências

## 1. Finalidade

Este documento define as unidades, escalas e referências de medição esperadas no processamento geoespacial do projeto GIS.

## 2. Unidades principais

- elevação em metros;
- resolução do raster em metros por pixel;
- declividade em percentual;
- coordenadas em CRS projetado, preferencialmente em metros;
- áreas e limites geoespaciais em unidades compatíveis com o CRS adotado.

## 3. Convenções de medição

- a camada de elevação deve ser tratada como superfície contínua em metros;
- a declividade percentual deve ser calculada exclusivamente a partir de valores válidos;
- valores ausentes devem permanecer mascarados e não convertidos em zero;
- todas as métricas finais devem declarar a unidade correspondente e o método adotado.

## 4. Referências de validação

- o CRS deve ser declarado em todos os relatórios e metadados;
- a resolução do raster deve constar em todas as saídas relevantes;
- qualquer variação de unidade deve ser registrada como decisão e impactar o relatório final.

## 5. Regras de consistência

- métricas em porcentagem devem ser reportadas como percentuais, não como frações;
- a análise deve preservar escala física dos dados e nunca inventar precisão;
- o cálculo deve manter coerência entre unidades, transformação e estatísticas finais.
