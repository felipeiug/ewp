# Normas do projeto GIS

## Propósito
Este diretório registra as normas, convenções e referências operacionais do processamento geoespacial do projeto GIS.

## Convenções principais
- Elevação em metros.
- Resolução em metros por pixel.
- Declividade percentual calculada a partir de valores válidos.
- CRS projetado, preferencialmente em metros, com documentação explícita.
- NoData mascarado e sem conversão em zero.

## Regras
- Dados sintéticos devem ser determinísticos e reproduzíveis.
- Resultados devem ser validados antes de aceitação.
- Alterações de método ou convenção devem ser registradas em HIPOTESES_DECISOES.
- O registro de execução deve preservar rastreabilidade entre entrada, processamento e saída.

## Referência
As normas gerenciais e operacionais específicas estão consolidadas em REQUISITOS/.
