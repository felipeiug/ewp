"""Conferencia geometrica da premissa autorizada; nao e planta legal de implantacao."""
from pathlib import Path
import os
import json
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
os.environ['MPLCONFIGDIR']=str(OUT/'ferramentas/matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
from shapely.geometry import Polygon,box
from shapely.affinity import translate

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

data=json.loads((OUT/'jose_da_silva_00_geometria_v02.json').read_text(encoding='utf-8'))
old=json.loads((OUT/'jose_da_silva_00_validacao_v02.json').read_text(encoding='utf-8'))
for name,digest in old['saidas_sha256'].items():
    assert sha(OUT/name)==digest, name
lot=box(0,0,1050,2000)
house=translate(Polygon(data['contorno']),xoff=150,yoff=550)
parking=[box(175,25,425,525),box(450,25,700,525)]
assert lot.covers(house)
assert all(lot.covers(p) and p.intersection(house).area==0 for p in parking)
assert parking[0].intersection(parking[1]).area==0
assert house.bounds==(150,550,900,1700)
assert house.area==841500

fig,ax=plt.subplots(figsize=(8,12),facecolor='white')
ax.add_patch(Patch(list(lot.exterior.coords),facecolor='#f2f5ed',edgecolor='#44544c',lw=1.5))
ax.add_patch(Patch(list(house.exterior.coords),facecolor='#e1e8e9',edgecolor='#526871',lw=1))
for _,bounds in data['paredes']:
    wall=translate(box(*bounds),xoff=150,yoff=550)
    ax.add_patch(Patch(list(wall.exterior.coords),facecolor='#526871',edgecolor='none',alpha=.7))
for i,p in enumerate(parking,1):
    ax.add_patch(Patch(list(p.exterior.coords),facecolor='#c3d4dd',edgecolor='#476776',lw=1))
    ax.text(p.centroid.x,p.centroid.y,f'VAGA {i}\n250 × 500 cm',ha='center',va='center',fontsize=10)
ax.text(525,1840,'FUNDOS 300 cm',ha='center',fontsize=10)
ax.text(75,1100,'150 cm',rotation=90,ha='center',fontsize=9)
ax.text(975,1100,'150 cm',rotation=90,ha='center',fontsize=9)
ax.text(800,280,'FAIXA FRONTAL\n550 cm mínimos',ha='center',fontsize=8)
ax.text(525,1100,'CASA\n750 × 1150 cm\n84,15 m² de contorno',ha='center',va='center',fontsize=10,
        bbox=dict(facecolor='white',edgecolor='none',alpha=.9))
ax.text(525,-75,'FRENTE / RUA',ha='center',fontsize=11)
ax.text(525,2040,'1050 cm',ha='center',fontsize=10)
ax.text(-55,1000,'2000 cm',rotation=90,ha='center',fontsize=10)
ax.set(xlim=(-100,1125),ylim=(-130,2100),aspect='equal')
ax.axis('off')
fig.suptitle('CASA 001 — CONFERÊNCIA DO LOTE',fontsize=15,y=.96)
fig.text(.5,.925,'Etapa 00 • premissa autorizada • revisão documental 03',ha='center',fontsize=10)
fig.text(.5,.025,'Esquema de encaixe, não planta de implantação final.\nDistâncias geométricas; conformidade urbanística não verificada.\nVagas reservadas; acessos e manobras a desenvolver.',ha='center',fontsize=9)
preview=OUT/'jose_da_silva_00_lote_assumido_v03.png'
fig.savefig(preview,dpi=160)
plt.close(fig)

report=OUT/'jose_da_silva_00_lote_assumido_v03.md'
report.write_text('''# Casa 001 — lote assumido — revisão documental 03

## Premissa vigente

Usuário autorizou dispensar identificação cadastral e considerar o projeto viável no local informado, com lote de 1050 × 2000 cm. Registro: `HIPOTESES_DECISOES/output/2026-09-24_1640_lote_assumido.md`. Não solicitar novamente cadastro para avançar no estudo. Conformidade urbanística específica não verificada.

Este adendo supera exclusivamente a exigência cadastral e o impedimento correspondente nos documentos v02. Preserva as cotas externas, o croqui e a geometria da casa. A revisão 03 é documental e de conferência do lote; os arquivos editáveis vigentes continuam sendo `jose_da_silva_00_planta_v02.dxf` e `jose_da_silva_00_paredes_v02.skp`.

## Conferência

- Lote: 1050 × 2000 cm, 210 m²; casa: contorno externo de 84,15 m², conforme JSON v02.
- Casa posicionada para teste em x=150…900, y=550…1700 cm; laterais 150 cm, fundos 300 cm e frente mínima 550 cm. Frente do estar a 600 cm por causa do avanço de 50 cm do jantar.
- Duas reservas de vagas de 250 × 500 cm: x=175…425 e x=450…700, ambas em y=25…525. Contidas no lote e sem sobreposição entre si ou com a casa.
- Distâncias são escolhas geométricas para o estudo, não parâmetros legais confirmados. Sem dimensionamento de muros, portões, cobertura da garagem ou validação de trajetórias e circulação de pedestres.
- Esquema mostra projeções de paredes sem detalhar vãos; consultar DXF/SKP v02 para os acessos. O banheiro direito mantém o acesso externo, com faixa lateral disponível.

## Validação e continuidade

Script `jose_da_silva_00_lote_assumido_v03.py` executado com verificações de contenção, não sobreposição e área. Hashes dos sete derivados v02 comparados com o relatório anterior: preservados. Evidências em `jose_da_silva_00_lote_assumido_validacao_v03.json`; prévia PNG na mesma pasta.

Mantidos os testes geométricos e de arquivos v02: DXF auditado; SKP reaberto pela biblioteca do SketchUp 2016. Testes nas interfaces gráficas continuam pendentes para aceitação final; não são apresentados como realizados.

Etapa 00 com entregáveis disponíveis para revisão do estudo, sem impedimento cadastral. Próxima transição: aprovação da etapa 00, exigida por `WORKFLOW/STEP_BY_STEP.md`, antes de 01 — Render 3D. Esta autorização sobre o lote não foi registrada como aprovação de desenhos ou como liberação para obra.
''',encoding='utf-8')
sources=[ROOT/'ENGINEERING.md',ROOT/'REQUISITOS/convencoes.md',ROOT/'WORKFLOW/STEP_BY_STEP.md',
         ROOT/'HIPOTESES_DECISOES/output/2026-09-24_1640_lote_assumido.md',
         OUT/'jose_da_silva_00_geometria_v02.json']
checks=dict(data=datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),
            fontes_sha256={str(p.relative_to(ROOT)):sha(p) for p in sources},
            fontes_originais_preservadas=all(sha(ROOT/name)==digest for name,digest in old['fontes_sha256'].items()
                                            if 'input' in Path(name).parts or name.startswith('NORMAS')),
            derivados_v02_preservados=True,contencao_casa_e_vagas='PASS',sobreposicoes='ZERO',
            distancia_frontal_min_cm=550,laterais_cm=[150,150],fundos_cm=300,
            conformidade_urbanistica='NAO VERIFICADA; cadastro dispensado para estudo pelo usuario',
            aprovacao_etapa_00='AGUARDANDO REVISAO',
            saidas_sha256={p.name:sha(p) for p in [preview,report,Path(__file__)]})
assert checks['fontes_originais_preservadas']
(OUT/'jose_da_silva_00_lote_assumido_validacao_v03.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print('PASS: casa e duas reservas de vagas contidas no lote; sem sobreposicao; originais e derivados v02 preservados.')
