# Regularização EWP e diagnóstico

Data local: 2026-09-24_1106; America/Sao_Paulo (UTC-03:00).
Autorização: usuário solicitou implementação integral do plano de regularização e diagnóstico.

## Decisões e conflitos

- Instruções explícitas do usuário prevalecem sobre `.github/agents/EWP.agent.md`: Step by Step incorporado em ENGINEERING.md e status alterado de CONTEXTO GERADO POR IA para INICIAL — CONTEXTO A CONFIRMAR. Justificativa: dados críticos não confirmados, sem aprovação de etapa. Arquivo do agente preservado; conflito documentado, não silenciosamente resolvido.
- A versão anterior de ENGINEERING.md e o fluxo anterior foram copiados byte a byte neste diretório antes das edições. O arquivo em WORKFLOW agora é referência histórica identificada.
- `00_dados` é a área existente; referências ativas a `00_entrada` foram corrigidas. Não houve movimentação de entradas.
- Dependências circulares 03 ← 02/03 e 04 ← 04 substituídas por propostas explicitamente pendentes: 03 ← 01/02 revisadas e 04 ← 03 aprovada. Nenhuma transição foi aprovada ou executada.
- Unidade explícita do croqui: m; conversão para cm por fator 100. Medidas internas sem sufixo interpretadas em m, identificadas no inventário. Unidade dos níveis permanece pendente; `REQUISITOS/unidades.md` não foi alterado.
- Requisitos e PDF normativo originais preservados. Novos diretórios e READMEs somente completam a estrutura autorizada. Nenhum valor normativo foi presumido.
- Não há prova de funcionamento do AutoCAD 2019 no ambiente; SketchUp 2016 localizado, abertura e salvamento não testados.

## Alterações

Modificados: ENGINEERING.md, WORKFLOW/STEP_BY_STEP.md.
Criados até este registro:

- `HIPOTESES_DECISOES/output/2026-09-24_1106_integridade_inicial.json`
- `HIPOTESES_DECISOES/output/2026-09-24_1106_engineering_anterior.md`
- `HIPOTESES_DECISOES/output/2026-09-24_1106_fluxo_anterior.md`
- `HIPOTESES_DECISOES/README.md`
- `REQUISITOS/README.md`
- `NORMAS/README.md`
- `00_dados/README.md`
- `WORKFLOW/README.md`
- `00_dados/output/jose_da_silva_00_inventario_v01.csv`
- `NORMAS/output/jose_da_silva_00_extracao_normativa_v01.txt`
- `NORMAS/output/jose_da_silva_00_fontes_v01.md`
- `00_dados/output/jose_da_silva_00_diagnostico_v01.md`

Este registro, o script de validação e seu relatório completam a entrega. Diretórios input/output foram completados em REQUISITOS, NORMAS e 00_dados; HIPOTESES_DECISOES já possuía ambos. Etapas futuras não foram criadas.

## Estado

Regularização e diagnóstico documental realizados. Etapa 00 parcial e aberta; não foram emitidos DXF, SKP ou pranchas. Não alterar o projeto inteiro para BLOQUEADO por essas pendências. Próximo passo: resposta consolidada às lacunas do diagnóstico, seguida de desenho e validação dos editáveis, antes da aprovação da etapa 00.

## Validação realizada

Executado `00_dados/output/jose_da_silva_00_validar_v01.py`: 57/57 verificações passaram. Relatório criado em `00_dados/output/jose_da_silva_00_validacao_v01.md`. Verificados SHA-256 dos sete originais não editados, cópias históricas dos dois documentos editados, estrutura, 33 dimensões e conversões, fechamento aritmético e extração normativa. A verificação numérica não resolve as ambiguidades geométricas. Não houve teste de abertura DXF/SKP nem declaração de conformidade legal.
