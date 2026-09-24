# Restrições do projeto

## 1. Finalidade

Este documento estabelece as restrições operacionais, de dados e de execução que o projeto deve obedecer durante a implementação e a validação.

## 2. Restrições de dados

- não utilizar dados reais ou externos sem autorização explícita;
- não alterar arquivos de entrada fornecidos pelo usuário;
- preservar CRS, resolução, extensão e valores de NoData quando aplicáveis;
- impedir a geração silenciosa de resultados incompletos.

## 3. Restrições de execução

- a execução deve ser determinística para o mesmo conjunto de dados e ambiente;
- a implementação deve ser idempotente e controlada por parâmetros explícitos;
- qualquer falha relevante deve ser registrada, sem ocultar exceções ou warnings relevantes;
- qualquer dependência ausente deve ser tratada como limitação ou bootstrap documentado.

## 4. Restrições de documentação

- o projeto não deve omitir decisões metodológicas importantes;
- alterações de método ou convenção exigem registro formal em HIPOTESES_DECISOES;
- o relatório final deve distinguir entre resultado validado, resultado parcial e bloqueio real.

## 5. Critério de conformidade

O projeto só pode ser considerado atendido quando todas as restrições acima forem respeitadas e os artefatos finais forem consistentes com a execução realizada.
