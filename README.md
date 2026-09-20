# EWP — Engineering Workspace Protocol

Este repositório não é um projeto técnico específico sendo executado no EWP. Ele é o repositório do agente EWP: uma estrutura de referência para criar, organizar e conduzir workspaces de engenharia com rastreabilidade, governança e continuidade de contexto.

O **Engineering Workspace Protocol (EWP)** é uma forma estruturada de conduzir projetos técnicos com agentes de inteligência artificial sem perder contexto, rastreabilidade ou controle de engenharia. Em vez de depender do histórico de uma conversa, o EWP usa o próprio repositório como memória oficial do trabalho.

O resultado é um workspace preparado para trabalho contínuo: compreensível, auditável, reproduzível e transferível.

## Por que usar o EWP?

Projetos de engenharia raramente falham apenas por falta de capacidade de cálculo. Eles também falham quando uma premissa deixa de ser registrada, um dado original é sobrescrito, uma versão de resultado perde sua origem ou uma decisão é tomada fora da sequência correta.

O EWP reduz esses riscos ao estabelecer uma disciplina operacional:

- o repositório é a fonte oficial de contexto e estado;
- dados originais são preservados;
- requisitos e normas ficam separados de hipóteses e decisões;
- cada resultado mantém ligação com suas entradas e métodos;
- o trabalho segue etapas, dependências e gates explícitos;
- lacunas e incertezas são declaradas, não preenchidas silenciosamente;
- outro profissional ou agente pode continuar o trabalho sem reconstruir todo o histórico.

## O agente EWP

O agente EWP atua como executor técnico e guardião do processo. Antes de trabalhar, ele identifica a raiz do projeto, lê o `ENGINEERING.md`, valida a estrutura do workspace e localiza a etapa aplicável.

Durante a execução, o agente:

- consulta as fontes existentes antes de assumir informações;
- verifica entradas, dependências, validações e aprovações;
- registra hipóteses e decisões relevantes;
- mantém dados de entrada separados dos artefatos gerados;
- utiliza métodos e ferramentas reproduzíveis;
- realiza verificações proporcionais ao risco;
- atualiza o histórico e o estado do projeto;
- interrompe o avanço quando um gate exige revisão ou aprovação.

A definição do agente está em [`.github/agents/EWP.agent.md`](.github/agents/EWP.agent.md).

## Estrutura de um workspace EWP

```text
PROJETO/
├── ENGINEERING.md
├── REQUISITOS/
│   ├── input/
│   ├── output/
│   ├── restricoes.md
│   ├── unidades.md
│   └── convencoes.md
├── HIPOTESES_DECISOES/
│   ├── input/
│   └── output/
├── NORMAS/
│   ├── input/
│   └── output/
├── 00_etapa/
│   ├── input/
│   └── output/
└── 01_etapa/
    ├── input/
    └── output/
```

As etapas numeradas são adaptadas ao fluxo real do projeto. Podem representar levantamento, dimensionamento, simulação, implementação, ensaio, validação, entrega ou qualquer outra sequência tecnicamente justificável.

### `ENGINEERING.md`

É o documento central do workspace. Deve identificar o projeto e registrar, quando aplicável:

- objetivo e escopo;
- estado atual;
- restrições e referências;
- entradas e entregáveis;
- critérios de aceitação;
- informações pendentes;
- próximos passos e histórico;
- sequência **Step by Step**.

A seção **Step by Step** define a ordem oficial de execução. Cada etapa pode declarar entradas, saídas, dependências, pontos de validação, gates de aprovação e condições para prosseguir.

### `REQUISITOS/`

Reúne obrigações técnicas e funcionais, restrições, unidades, convenções e critérios verificáveis. Os requisitos não devem ser confundidos com preferências ou hipóteses de trabalho.

### `HIPOTESES_DECISOES/`

Registra premissas, alternativas avaliadas, decisões tomadas, justificativas, impactos e pontos ainda sujeitos a confirmação. O histórico é preservado; uma decisão nova complementa ou substitui formalmente a anterior sem apagá-la.

### `NORMAS/`

Armazena normas, procedimentos, referências técnicas e registros de verificação. As fontes ficam em `input/`; análises de aderência, checklists e resultados ficam em `output/`.

### Etapas numeradas

Cada área de trabalho possui:

- `input/`: fontes originais ou entradas aprovadas, mantidas sem alteração;
- `output/`: transformações, cálculos, modelos, relatórios e demais resultados reproduzíveis.

Essa separação torna explícito o caminho entre a evidência recebida e o resultado produzido.

## Hierarquia das fontes

Quando há divergência, o EWP utiliza esta ordem de precedência:

1. dados originais em `input/`;
2. requisitos e normas aplicáveis;
3. hipóteses e decisões registradas;
4. `ENGINEERING.md`;
5. resultados reproduzíveis em `output/`;
6. informações existentes apenas na conversa.

Conflitos não são resolvidos silenciosamente. As fontes, o impacto e a decisão adotada devem permanecer registrados.

## Ciclo de trabalho

Um ciclo típico no EWP segue esta sequência:

1. identificar ou inicializar a raiz do workspace;
2. validar a estrutura e ler o estado do projeto;
3. localizar a etapa atual no `ENGINEERING.md`;
4. verificar entradas, requisitos, dependências e gates;
5. executar o trabalho com método reproduzível;
6. validar consistência, unidades e critérios de aceitação;
7. armazenar resultados em `output/`;
8. registrar decisões, limitações e histórico;
9. avançar somente quando as condições da próxima etapa forem satisfeitas.

## Potencial de aplicação

O protocolo pode apoiar projetos de diferentes áreas e escalas, incluindo:

- engenharia civil, elétrica, mecânica, ambiental e de produção;
- análise de dados, aprendizado de máquina e modelagem científica;
- dimensionamento, simulação e otimização;
- estudos de viabilidade e avaliações técnico-econômicas;
- desenvolvimento de hardware e software embarcado;
- pesquisa acadêmica e documentação experimental;
- processos regulados que exigem evidências e revisão;
- projetos longos executados por várias pessoas ou agentes.

O EWP não determina quais ferramentas técnicas devem ser usadas. Ele organiza como entradas, métodos, decisões e resultados são conectados, permitindo incorporar planilhas, scripts, notebooks, CAD, modelos numéricos, documentos LaTeX, bancos de dados e ferramentas especializadas no mesmo fluxo de governança.

## Benefícios para equipes e agentes

- **Continuidade:** o conhecimento permanece no projeto, não em uma sessão isolada.
- **Rastreabilidade:** resultados podem ser relacionados às fontes e decisões que os originaram.
- **Reprodutibilidade:** métodos, parâmetros e artefatos ficam disponíveis para repetição.
- **Revisão:** gates e critérios de aceitação tornam a validação explícita.
- **Segurança:** dados originais e histórico são preservados.
- **Colaboração:** pessoas e agentes trabalham sobre a mesma estrutura de referência.
- **Escalabilidade:** novas etapas podem ser adicionadas sem perder a organização do projeto.

## Como começar

1. Baixe ou clone este repositório como base do agente EWP.
2. Instale ou selecione o agente definido em `.github/agents/EWP.agent.md`.
3. Abra o workspace em um ambiente compatível.
4. Use o repositório como template para criar um projeto real ou adaptar a estrutura a um caso concreto.
5. Peça ao agente para iniciar o workspace ou execute o comando `START`.
6. Confirme as informações e gates indicados no `ENGINEERING.md`.
7. Conduza o projeto pelas etapas registradas.

## Exemplo incluído

Este repositório contém uma aplicação demonstrativa de previsão de vazões. Ela mostra como requisitos, normas, decisões, entradas, saídas e etapas podem ser organizados dentro do protocolo. O domínio apresentado pode ser substituído pela estrutura e pelo fluxo técnico de qualquer outro projeto.

## Princípio central

> O contexto de engenharia deve permanecer no workspace, e cada resultado deve poder explicar de onde veio, como foi produzido e o que ainda precisa ser validado.

O EWP aproxima a velocidade dos agentes de inteligência artificial da disciplina exigida por projetos técnicos reais.
