# WORKFLOW

Esta pasta centraliza o fluxo de execução do projeto e define a sequência operacional oficial do agente EWP.

## Objetivo

Separar a lógica de execução do contexto geral do projeto. Enquanto `ENGINEERING.md` descreve o que é o projeto, o workflow descreve como ele deve ser conduzido passo a passo.

## Arquivos principais

- `STEP_BY_STEP.md`: arquivo autoritativo com a sequência de etapas, dependências, validações e gates.

## Regra do protocolo

O fluxo de execução deve ser:

- explícito;
- reproduzível;
- separado do contexto documental;
- rastreável;
- usado como referência obrigatória pelo agente antes de avançar no trabalho.

## Como o agente deve usar esta pasta

Antes de executar qualquer tarefa técnica, o agente deve:

1. localizar a etapa atual;
2. verificar dependências e entradas;
3. confirmar a presença de validações e gates;
4. executar apenas a etapa autorizada;
5. registrar resultados em `output/`;
6. só então avançar para a próxima etapa.

## Importância

Sem um workflow claro, o projeto corre o risco de perder ordem, consistência e rastreabilidade. Esta pasta garante que a execução siga uma disciplina explícita e que novas pessoas ou agentes consigam continuar o trabalho sem depender do histórico da conversa.
