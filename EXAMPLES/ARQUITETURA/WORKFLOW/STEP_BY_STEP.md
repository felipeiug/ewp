# Referência histórica — não executar

Desde 2026-09-24, o fluxo vigente está na seção **Step by Step** de `../ENGINEERING.md`, por instrução expressa do usuário. O conteúdo abaixo preserva a sequência anterior, inclusive caminhos inválidos e dependências circulares; não constitui um segundo fluxo vigente.

---


## Step by Step

### 00 — Dados

- Verificar croqui feito à mão com medidas em `00_entrada/input/` e informar inconsistências, ambiente inacessíveis ou fora de padrão e outros dados que sejam necessários.
- Saída: arquivo da planta baixa `.dxf` e residência, somente paredes, `.skp` salvo em `00_entrada/output/`.
- Validação: confirmar uso, local, lote, orientação, níveis, medidas críticas, legislação e formatos de entrega.

### 01 — Render 3D

- Dependência: etapa 00 aprovada.
- Gerar o projeto SKP 3D com móveis e ambientação, gerar também uma imagem da renderização do imóvel vista de cima e da fachada, gerar por IA e não pelo software.
- Entrada: DXF e SKP disponíveis em `00_entrada/output/` na versão mais recente.
- Saída: `01_estudo_preliminar/output/`.
- Validação: ambientes, fluxos, áreas, dimensões e premissas conferidos.

### 02 — Desenvolvimento 2D no AutoCAD

- Dependência: etapa 00 aprovada.
- Entrada: DXF e SKP disponíveis em `00_entrada/output/` na versão mais recente.
- Saída: planta baixa, implantação, cortes, fachadas, cotas, níveis, layers e arquivo editável `.dxf` em `02_autocad/output/`.
- Validação: escala, unidades, espessuras, vãos, cotas, níveis, referências cruzadas e adequação ao plano diretor do município.

### 03 — Compatibilização e documentação final

- Dependência: etapas 02 e 03 revisadas.
- Entrada: DXF, SKP, decisões e lista de pendências.
- Saída: desenhos finais, pranchas, carimbo, lista de arquivos e PDFs em `03_projeto/output/`.
- Validação: conferência folha a folha, legibilidade, escala, revisão, consistência 2D/3D e ausência de pendências críticas.

### 04 — Relatório e entrega

- Dependência: etapa 04 aprovada.
- Entrada: todos os arquivos-fonte e PDFs emitidos.
- Saída: relatório compilado em `.tex` e `.pdf`, índice de entregáveis, premissas, limitações e histórico de revisões em `04_relatorio/output/`.
- Validação: abrir os arquivos entregues, verificar links/referências e confirmar que o conjunto é reproduzível a partir do croqui preservado.