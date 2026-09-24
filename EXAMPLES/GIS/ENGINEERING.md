# ENGINEERING

## 1. Identificação

- Projeto: GIS - Processamento geoespacial
- Responsável: Agente EWP
- Data de referência: 2026-09-24
- Status: ATIVO

## 2. Objetivo

Este projeto objetiva demonstrar, de forma reprodutível e auditável, a geração de um Modelo Digital de Elevação sintético, a análise da bacia hidrográfica associada e o cálculo da declividade percentual por raster.

A execução deve seguir o padrão EWP, preservando rastreabilidade, integridade de dados e transparência de decisão. O projeto deve operar sem depender de dados reais ou de downloads externos, priorizando execução determinística em ambiente Windows e registros explícitos de qualquer limitação ou hipótese adotada.

## 3. Escopo

### 3.1 Dentro do escopo

- validar a estrutura do projeto EWP;
- confirmar a existência das entradas necessárias;
- gerar dados sintéticos determinísticos quando a entrada não estiver disponível;
- implementar o pipeline de processamento geoespacial;
- calcular a declividade percentual a partir do MDE;
- produzir artefatos de resultado e relatório de validação;
- registrar decisões e impactos em HIPOTESES_DECISOES;
- documentar status, dependências e pendências.

### 3.2 Fora do escopo

- uso de dados reais ou geodados externos não autorizados;
- alteração de entradas fornecidas pelo usuário;
- mudança silenciosa de CRS, resolução ou NoData;
- geração de resultados sem validação técnica;
- adoção de metodologia não registrada formalmente.

## 4. Restrições, premissas e condições

- Os dados de entrada devem ser preservados em estado original.
- Nenhuma saída deve ser considerada válida apenas por existir em disco.
- Qualquer dependência ausente deve ser registrada e, quando possível, substituída por bootstrap determinístico e documentado.
- O projeto deve operar sem inventar precisão ou omitir falhas relevantes.
- Em caso de conflito entre documentos, a ordem de precedência é: dados originais, requisitos, normas, hipóteses e decisões, e, por fim, este documento.

## 5. Referências

- Requisitos: REQUISITOS/
- Normas: NORMAS/
- Hipóteses e decisões: HIPOTESES_DECISOES/
- Etapas do projeto: 00_PLANEJAMENTO/, 01_DADOS/, 02_PROCESSAMENTO/, 03_RESULTADOS/
- Workflow autoritativo: WORKFLOW/STEP_BY_STEP.md
- Convenção técnica principal: NORMAS/README.md

## 5.1 Workflow de execução

O workflow autoritativo do projeto está definido em WORKFLOW/STEP_BY_STEP.md. Este documento é a referência de execução e deve ser obedecido para avanço entre etapas, validações e registros.

## 6. Entradas esperadas

- 01_DADOS/input/mde_sintetico.tif
- 01_DADOS/input/bacia_sintetica.geojson

Quando qualquer uma das entradas não estiver disponível, o projeto deve gerar um conjunto sintético determinístico em local de entrada e registrar esta ação como bootstrap, sem alterar arquivos fornecidos pelo usuário.

## 7. Entregáveis esperados

- 01_DADOS/input/ com dados sintéticos, quando necessário;
- 02_PROCESSAMENTO/output/processamento.py;
- 02_PROCESSAMENTO/output/declividade_pct.tif;
- 02_PROCESSAMENTO/output/metricas_processamento.json;
- 03_RESULTADOS/output/mapa_declividade.png;
- 03_RESULTADOS/output/metricas.json;
- 03_RESULTADOS/output/validacao.md;
- HIPOTESES_DECISOES/output/decisoes.md ou arquivo equivalente de registro.

## 8. Critérios de aceitação

O projeto será considerado aprovado somente quando:

- as entradas forem legíveis e compatíveis;
- a bacia e o MDE estiverem no mesmo CRS, ou houver reprojeção controlada e registrada;
- o raster de saída tiver dimensões, transformação e NoData consistentes;
- a declividade for calculada de forma estável e reprodutível;
- todas as métricas relevantes forem coerentes com os valores válidos;
- os relatórios e JSONs apresentarem campos mínimos e sem valores omitidos;
- o comando de execução puder ser repetido sem alteração do código;
- as decisões relevantes tiverem sido registradas em HIPOTESES_DECISOES.

## 9. Passo a passo do projeto

### Etapa 1 — Diagnóstico e estrutura

Entradas: estrutura do workspace e arquivos existentes.
Saídas esperadas: confirmação da estrutura EWP e identificação de pendências.
Validação: verificar a presença dos diretórios e a existência de dados de entrada.
Gatilho de avanço: identificação da base funcional e dos arquivos faltantes.

### Etapa 2 — Inventário dos dados e ambiente

Entradas: artefatos existentes em 01_DADOS/, 02_PROCESSAMENTO/ e 03_RESULTADOS/.
Saídas esperadas: inventário de tipos, tamanhos, CRS, resolução e versões relevantes.
Validação: conferir se há dados legíveis e se o ambiente atende ao mínimo operacional.
Gatilho de avanço: confirmação do estado real do ambiente e dos dados.

### Etapa 3 — Bootstrap do conjunto sintético

Entradas: ausência de dados necessários ou inconsistência detectada.
Saídas esperadas: MDE e geometria de bacia sintéticos gerados em 01_DADOS/input/.
Validação: verificar se o bootstrap é determinístico, em metros e em CRS definido.
Gatilho de avanço: dados de entrada consistentes e documentados.

### Etapa 4 — Implementação do pipeline

Entradas: MDE, bacia e convenções técnicas.
Saídas esperadas: script executável em 02_PROCESSAMENTO/output/processamento.py.
Validação: verificar argumentos, uso de caminhos absolutos/relativos confiáveis, suporte a --help e mensagens claras de erro.
Gatilho de avanço: código funcional e estável.

### Etapa 5 — Execução e reprodutibilidade

Entradas: script de processamento e dados de entrada.
Saídas esperadas: raster processado, métricas JSON e material de validação.
Validação: executar duas vezes e comparar resultados; confirmar ausência de variação indevida.
Gatilho de avanço: execução estável e repetível.

### Etapa 6 — Geração de artefatos finais

Entradas: raster calculado e estatísticas geradas.
Saídas esperadas: mapa de declividade, relatório técnico e métricas finais.
Validação: conferir que o mapa seja consistente com o raster e que os relatórios refiram-se aos valores reais.
Gatilho de avanço: artefatos finais consistentes.

### Etapa 7 — Validação final

Entradas: saídas geradas e convenções técnicas.
Saídas esperadas: relatório de validação com status, limitações e evidências.
Validação: verificar critérios mínimos, integração de metadata, integridade do NoData e consistência dos percentis.
Gatilho de avanço: aprovação de todos os checks relevantes.

### Etapa 8 — Encerramento e registro

Entradas: resultado validado ou bloqueado.
Saídas esperadas: atualização do status do projeto e registro formal em HIPOTESES_DECISOES.
Validação: confirmar que as decisões, pendências e comando de execução foram documentados.
Gatilho de avanço: fechamento com evidência e sem omissão.

