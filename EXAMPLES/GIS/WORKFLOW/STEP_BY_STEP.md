# Workflow do projeto GIS

Este arquivo é o workflow autoritativo do projeto e define a sequência de execução, dependências e critérios de avanço.

## Etapa 1 — Diagnóstico e estrutura
- Verificar a estrutura EWP, a integridade dos diretórios e a presença de entradas.
- Registrar pendências e confirmar o estado do ambiente.
- Critério de avanço: estrutura validada e dados disponíveis ou bootstrap registrado.

## Etapa 2 — Inventário dos dados e ambiente
- Inventariar arquivos em 01_DADOS/, 02_PROCESSAMENTO/ e 03_RESULTADOS/.
- Validar tipos de dado, CRS, resolução, NoData e dependências do ambiente.
- Critério de avanço: estado real do ambiente e dos dados confirmado.

## Etapa 3 — Bootstrap do conjunto sintético
- Quando necessário, gerar MDE e geometria de bacia em 01_DADOS/input/.
- Preservar determinismo e unidades em metros, conforme convenções.
- Critério de avanço: entradas consistentes e documentadas.

## Etapa 4 — Implementação do pipeline
- Implementar o script em 02_PROCESSAMENTO/output/processamento.py.
- Garantir roteiros confiáveis, argumentos explícitos e mensagens adequadas.
- Critério de avanço: execução estável e reproduzível.

## Etapa 5 — Execução e reprodutibilidade
- Executar o pipeline com os dados válidos.
- Validar ausência de variação indevida em duplicatas de execução.
- Critério de avanço: saídas geradas e estatísticas coerentes.

## Etapa 6 — Geração de artefatos finais
- Produzir mapa e relatórios finais em 03_RESULTADOS/output/.
- Confirmar que os artefatos reflitam os valores reais gerados.
- Critério de avanço: artefatos finais consistentes.

## Etapa 7 — Validação final
- Revisar métricas, metadados, NoData e coerência dos percentis.
- Registrar possíveis limitações, pendências e evidências.
- Critério de avanço: aprovação dos checks relevantes.

## Etapa 8 — Encerramento e registro
- Atualizar o status do projeto e registrar o histórico em HIPOTESES_DECISOES/output/.
- Confirmar que decisões relevantes, resultados e execução foram documentados.
- Critério de avanço: fechamento com evidência e sem omissão.
