from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import pymupdf

ROOT = Path(__file__).resolve().parents[2]
stamp = datetime.now(ZoneInfo('America/Sao_Paulo')).strftime('%Y-%m-%d_%H%M%S')
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
sources = [p for p in ROOT.rglob('*') if p.is_file() and
           ('input' in p.relative_to(ROOT).parts or p.suffix == '.pdf' or
            p.parent.name == 'REQUISITOS' or p.name == 'STEP_BY_STEP.md')]
before = {str(p.relative_to(ROOT)): digest(p) for p in sources}
created = []
def create(rel, text):
    p = ROOT / rel
    if not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('x', encoding='utf-8') as f:
            f.write(text)
        created.append(rel)

areas = {
    'HIPOTESES_DECISOES': 'Registrar premissas, decisões e alterações. Entradas: decisões fornecidas. Saídas: registros datados e verificações.',
    'REQUISITOS': 'Preservar requisitos, unidades e convenções. Entradas: requisitos fornecidos. Saídas: verificações, sem substituir os documentos existentes.',
    'NORMAS': 'Preservar referências normativas. Entradas: documentos oficiais e referência existente na raiz desta área. Saídas: análises rastreáveis; a presença da referência não comprova conformidade.',
    '00_dados': 'Conferir o croqui e preparar a geometria. Entradas: croqui e carimbo. Saídas: diagnóstico e, após resolver medidas, DXF e SKP da etapa 00.',
}
for area, purpose in areas.items():
    for sub in ('input', 'output'):
        p = ROOT / area / sub
        if not p.exists():
            p.mkdir()
            created.append(f'{area}/{sub}/')
    create(f'{area}/README.md', f'# {area}\n\n{purpose}\n')
create('WORKFLOW/README.md', '# Workflow\n\nFinalidade: manter a sequência de execução. Entradas: contexto e requisitos. Saídas: etapas, dependências e validações em STEP_BY_STEP.md.\n')
eng = ROOT / 'ENGINEERING.md'
with eng.open('a', encoding='utf-8') as f:
    f.write(f'''\n## Step by Step

A sequência detalhada permanece em `WORKFLOW/STEP_BY_STEP.md`, incorporada por referência, sem alteração de suas etapas:

1. 00 — Dados: conferir croqui, requisitos e legislação; resolver inconsistências; gerar DXF e SKP de paredes; validar uso, local, lote, orientação, níveis, medidas e formatos.
2. 01 — Render 3D: somente após aprovação da etapa 00, usar seus DXF/SKP e validar ambientes, fluxos, áreas e premissas.
3. 02 — Desenvolvimento 2D: após a etapa anterior na sequência e com etapa 00 aprovada; usar a mesma geometria e validar desenhos e adequação normativa.
4. 03 — Compatibilização: somente com 01 e 02 revisadas; conferir conjunto e PDFs.
5. 04 — Relatório: somente com 03 aprovada; conferir fontes e entregáveis.

## Histórico — {stamp} (America/Sao_Paulo)

- START: estrutura mínima complementada conforme instruções diretas do usuário; fontes preservadas. Divergências com `.github/agents/EWP.agent.md` registradas em `HIPOTESES_DECISOES/output/{stamp}_start.md`.
- Etapa 00 parcialmente executada: inventário e diagnóstico em `00_dados/output/jose_da_silva_00_diagnostico_v01.md`. Geometria depende da decisão sobre cotas conflitantes; nenhuma aprovação presumida.
- Status do projeto mantido: INICIAL — CONTEXTO A CONFIRMAR. Próximo passo: resolver cotas, conferir implantação e parâmetros do lote, produzir e validar DXF/SKP.\n''')

doc = pymupdf.open(ROOT / 'NORMAS/plano_diretor_bh.pdf')
create('00_dados/output/jose_da_silva_00_referencia_normativa_v01.txt',
       'Fonte: NORMAS/plano_diretor_bh.pdf; extração PyMuPDF '+pymupdf.VersionBind+'; páginas numeradas a partir de 1.\n\n' +
       '\n'.join(f'--- Página {i+1} ---\n'+p.get_text() for i,p in enumerate(doc)))
create('00_dados/output/jose_da_silva_00_diagnostico_v01.md', '''# Casa 001 — diagnóstico da etapa 00 — v01

Resultado parcial; DXF e SKP ainda não emitidos. Método: leitura visual do croqui, transcrição das cotas explícitas, conversão por fator 100 e conferência aritmética com as convenções. Não usar dimensões em pixels como medidas.

## Fontes

- ENGINEERING.md; WORKFLOW/STEP_BY_STEP.md.
- REQUISITOS/convencoes.md, unidades.md e restricoes.md.
- 00_dados/input/croqui.jpg; carimbo.png preservado, ainda não diagramado.
- NORMAS/plano_diretor_bh.pdf: 128 páginas; e-book explicativo, apresentação datada de agosto de 2023; extração integral em jose_da_silva_00_referencia_normativa_v01.txt. A leitura inicial não equivale a análise normativa completa.

## Inventário de cotas

| Elemento | Original no croqui (m) | Convertido (cm) |
|---|---|---|
| Largura externa ao fundo | 7,50 | 750 |
| Duas subdivisões superiores | 3,75 + 3,75 | 375 + 375 |
| Extensão direita | 11,50 | 1150 |
| Cadeia esquerda | 3,50 + 3,00 + 1,50 + 3,00 | 350 + 300 + 150 + 300 = 1100 |
| Cadeia direita | 3,50 + 1,50 + 3,00 + 3,50 | 350 + 150 + 300 + 350 = 1150 |
| Dois dormitórios ao fundo, cada | 3,50 × 3,75 | 350 × 375 |
| Dormitório esquerdo central | 3,00 × 3,30 | 300 × 330 |
| Dois banheiros, cada | 1,50 × 3,30 | 150 × 330 |
| Cozinha | 3,00 × 3,30 | 300 × 330 |
| Estar | 3,00 × 4,20 | 300 × 420 |
| Jantar | 3,30 × 3,50 | 330 × 350 |
| Frente, trechos externos | 4,20 + 3,30 | 420 + 330 |

Requisitos documentados: lote 1050 × 2000 cm; pé-direito 300 cm; paredes internas 9 cm, externas 15 cm; rua abaixo; terreno plano simplificado; norte dispensado nesta fase; duas vagas; cobertura com platibanda. Área retangular do lote: 210 m², calculada como 10,50 × 20,00. Implantação e área construída não fixadas.

## Inconsistências e acessos

1. Os dois dormitórios não podem manter 375 cm internos cada em 750 cm externos: 375 + 375 + 15 + 9 + 15 = 789 cm. A convenção já autoriza adaptar essa faixa: se simétrica, largura interna de cada um seria (750 - 30 - 9)/2 = 355,5 cm. Valor calculado, ainda não geometria emitida.
2. O mesmo conflito se repete em profundidade: as cotas internas da cadeia direita somam os mesmos 1150 cm da cota externa, sem reservar paredes. Mesmo com três divisórias simples de 9 cm e duas externas de 15 cm, seriam 1207 cm. Este é um teste aritmético de incompatibilidade, não uma dimensão externa proposta. O ajuste autorizado para os dormitórios não resolve automaticamente cozinha, banheiros e jantar.
3. Os trechos frontais 420 e 330 somam 750 cm externos; não podem simultaneamente representar larguras internas completas sem descontar paredes. Corredor e encontro com o estar precisam ser coordenados.
4. A diferença 1150 - 1100 = 50 cm entre laterais é compatível com o avanço desenhado do jantar. Não foi tratada como erro nem como cota explícita do avanço.
5. O banheiro direito aparece com porta para a lateral externa e sem porta desenhada para o corredor. Não é comprovadamente inacessível: depende de acesso externo e implantação ainda não definidos. Proposta para revisão: transferir acesso ao corredor, sem presumir autorização para alterar o croqui.
6. Corredor, vãos, peitoris e platibanda não têm cotas explícitas. As convenções autorizam escolhas do agente; nenhuma foi aplicada antes do fechamento da geometria. Garagem de duas vagas não aparece no croqui da área construída e precisa ser implantada no lote.

## Situação normativa e formatos

Consulta em 2026-09-24: a PBH disponibiliza parâmetros geográficos e cadastrais no Geosiurbe/BHMap: https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/base-de-dados . Referência do Plano Diretor: https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/plano-diretor/proposta .
Não foram confirmados o lote cadastral, zoneamento, sobrezoneamentos e parâmetros específicos deste endereço. Não adotar recuos, permeabilidade ou coeficientes por suposição; conformidade ainda não verificada.
Formatos exigidos: DXF para AutoCAD 2019 e SKP para SketchUp 2016. Nenhum teste de abertura realizado; disponibilidade de gravador SKP compatível ainda não verificada.

## Decisão necessária

Definir se devem prevalecer as cotas externas (750 × 1150 cm, com o avanço frontal indicado), ajustando medidas internas para acomodar paredes, ou as medidas internas dos ambientes, revisando o contorno externo. A autorização atual para adaptar dormitórios não abrange inequivocamente todos os ambientes.
Após essa decisão, resolver implantação, acesso do banheiro e parâmetros urbanísticos, gerar e validar os arquivos da etapa 00. Etapas 01 e seguintes não iniciadas; dependem das validações e aprovações do workflow.
''')
create(f'HIPOTESES_DECISOES/output/{stamp}_start.md', f'''# START — {stamp} — America/Sao_Paulo

Raiz: {ROOT}

Conflito documental: as instruções diretas do usuário exigem input/output nas áreas e seção Step by Step em ENGINEERING.md; `.github/agents/EWP.agent.md` proíbe essas pastas em REQUISITOS/NORMAS e pede workflow apenas externo, além de usar outros status. Aplicadas as instruções diretas: criadas somente pastas e explicações ausentes, mantidos documentos e status existentes; seção central referencia a sequência detalhada existente. Nenhuma etapa ou aprovação removida.

Suposições: somente terreno plano e rua abaixo, já autorizados em REQUISITOS/convencoes.md. Não inferidos norte, parâmetros legais, medidas faltantes ou aprovação. Conversões m→cm usam fator 100.

Etapa 00 parcial: cotas conflitantes impedem geometria definitiva. Diagnóstico, extração normativa e script em 00_dados/output/. Fontes originais preservadas por comparação SHA-256 antes/depois. Projeto não declarado bloqueado ou concluído.

Modificado: ENGINEERING.md por adição de seção e histórico. Criado: este registro; script jose_da_silva_00_diagnostico_v01.py; itens listados no manifesto de validação. Nenhum arquivo de entrada alterado.
''')
after = {str(p.relative_to(ROOT)): digest(p) for p in sources}
assert before == after, 'Fonte alterada'
assert 375*2+15*2+9 == 789
assert (750-30-9)/2 == 355.5
assert 350+150+300+350+30+27 == 1207
for area in areas:
    assert all((ROOT/area/sub).is_dir() for sub in ('input','output'))
create(f'00_dados/output/{stamp}_validacao.json', json.dumps({
    'data_fuso': stamp+' America/Sao_Paulo', 'fontes_sha256': before,
    'fontes_preservadas': before == after, 'criados': created,
    'modificados': ['ENGINEERING.md'], 'verificacoes_aritmeticas': 'PASS',
    'estrutura_minima': 'PASS', 'abertura_dxf_skp': 'NAO EXECUTADA',
    'conformidade_normativa': 'NAO VERIFICADA'}, ensure_ascii=False, indent=2))
print('PASS: estrutura, aritmética e preservação de fontes. Etapa 00 parcial.')
print('Registro:', f'HIPOTESES_DECISOES/output/{stamp}_start.md')
