# Convenções de requisitos

## 1. Finalidade

Este documento reúne as convenções do processo que estruturam o atendimento aos requisitos do projeto GIS e sua validação final.

## 2. Convenções de projeto

- o projeto deve seguir a estrutura EWP e manter separação entre engenharia, requisitos e normas;
- a execução deve ser auditável e reproduzível;
- as decisões com impacto em metodologia, CRS, resolução ou NoData devem ser registradas formalmente;
- a validação deve considerar dados reais gerados pelo processamento e não apenas a presença de arquivos.

## 3. Convenções de aceitação

- entradas devem ser legíveis e compatíveis;
- a bacia e o MDE devem ser consistentes em CRS ou sofrer reprojeção controlada e documentada;
- a saída deve conter apenas valores válidos em pixels processados;
- relatórios, JSONs e mapas devem refletir a mesma base de cálculo.

## 4. Convenções de documentação

- qualquer hipótese de bootstrap deve ser registrada com causa, impacto e evidência;
- falhas e bloqueios devem ser reportados explicitamente no relatório final;
- a descrição do método e da referência espacial deve ser clara e não ambígua.

## 5. Critério final

A conformidade do projeto é confirmada quando os requisitos deste diretório, as normas técnicas e os critérios de execução forem atendidos simultaneamente, sem omissão de evidência.
