"""Etapa 00. Executar com Python 3.12; todos os artefatos ficam nesta pasta.
Fontes: croqui.jpg, REQUISITOS e decisao do usuario em 2026-09-24.
Uma unidade geometrica = 1 cm. Saidas v02 de estudo, sem aprovacao legal.
"""
from pathlib import Path
import sys
import os
import json
import hashlib
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import Counter

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
os.environ['MPLCONFIGDIR'] = str(OUT / 'ferramentas' / 'matplotlib')
sys.path.insert(0, str(OUT / 'ferramentas' / 'python'))
import numpy as np
import shapely
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
import ezdxf
from ezdxf.enums import TextEntityAlignment
from ezdxf import bbox as dxf_bbox
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch, Arc
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from jose_da_silva_00_skp_api_v02 import API

PREFIX = 'jose_da_silva_00'
def destination(kind, suffix):
    return OUT / f'{PREFIX}_{kind}_v02.{suffix}'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

source_files = [ROOT / p for p in (
    '00_dados/input/croqui.jpg', '00_dados/input/carimbo.png',
    'REQUISITOS/convencoes.md', 'REQUISITOS/unidades.md',
    'REQUISITOS/restricoes.md', 'NORMAS/plano_diretor_bh.pdf',
    'WORKFLOW/STEP_BY_STEP.md',
    'HIPOTESES_DECISOES/output/2026-09-24_1631_prioridade_cotas_externas.md',
    'HIPOTESES_DECISOES/output/2026-09-24_1636_consulta_lote.md')]
source_hashes = {str(p.relative_to(ROOT)):sha(p) for p in source_files}

# Paredes sem sobreposicao volumetrica nos encontros. Coordenadas absolutas em cm.
WALLS = [
    ('E01_lateral_esquerda', (0,50,15,1150)),
    ('E02_fundos', (15,1135,735,1150)),
    ('E03_lateral_direita', (735,0,750,1150)),
    ('E04_frente_estar', (15,50,420,65)),
    ('E05_avanco_jantar', (420,0,435,65)),
    ('E06_frente_jantar', (435,0,735,15)),
    ('I01_corredor_esquerda', (311,354.5,320,900)),
    ('I02_corredor_direita', (420,354.5,429,900)),
    ('I03_fundo_corredor', (311,900,429,909)),
    ('I04_divisa_dormitorios', (370.5,909,379.5,1135)),
    ('I05_base_dormitorio_1', (15,795.5,311,804.5)),
    ('I06_base_dormitorio_2', (429,795.5,735,804.5)),
    ('I07_dormitorio_3_banho_1', (15,495.5,311,504.5)),
    ('I08_banho_2_cozinha', (429,645.5,735,654.5)),
    ('I09_banho_1_estar', (15,345.5,320,354.5)),
    ('I10_cozinha_jantar', (420,345.5,735,354.5)),
]

# Vao: parede, posicao ao longo de x (horizontal) ou y (vertical), z inferior/superior.
# A dimensao e geometrica livre; marcos, ferragens e verificacao estrutural sao posteriores.
OPENINGS = [
    dict(id='P01', wall='E04', a=320,b=410,z0=0,z1=210,kind='porta',swing='N',description='Entrada principal'),
    dict(id='P02', wall='I01', a=810,b=890,z0=0,z1=210,kind='porta',swing='W',description='Dormitorio 1'),
    dict(id='P03', wall='I02', a=810,b=890,z0=0,z1=210,kind='porta',swing='E',description='Dormitorio 2'),
    dict(id='P04', wall='I01', a=680,b=760,z0=0,z1=210,kind='porta',swing='W',description='Dormitorio 3'),
    dict(id='P05', wall='I01', a=400,b=480,z0=0,z1=210,kind='porta',swing='W',description='Banheiro 1'),
    dict(id='P06', wall='E03', a=705,b=785,z0=0,z1=210,kind='porta',swing='W',description='Banheiro 2: acesso externo preservado'),
    dict(id='P07', wall='I10', a=635,b=715,z0=0,z1=210,kind='porta',swing='N',description='Cozinha'),
    dict(id='J01', wall='E01', a=950,b=1070,z0=90,z1=210,kind='janela',description='Dormitorio 1'),
    dict(id='J02', wall='E03', a=950,b=1070,z0=90,z1=210,kind='janela',description='Dormitorio 2'),
    dict(id='J03', wall='E01', a=565,b=685,z0=90,z1=210,kind='janela',description='Dormitorio 3'),
    dict(id='J04', wall='E01', a=390,b=450,z0=180,z1=240,kind='janela',description='Banheiro 1: alta'),
    dict(id='J05', wall='E03', a=705,b=785,z0=220,z1=280,kind='janela',description='Banheiro 2: bandeira acima da porta'),
    dict(id='J06', wall='E03', a=420,b=570,z0=110,z1=220,kind='janela',description='Cozinha'),
    dict(id='J07', wall='E04', a=100,b=260,z0=90,z1=210,kind='janela',description='Estar'),
    dict(id='J08', wall='E06', a=500,b=680,z0=90,z1=210,kind='janela',description='Jantar'),
    dict(id='V01', wall='I10', a=450,b=590,z0=110,z1=210,kind='passa_pratos',description='Abertura cozinha/jantar do croqui'),
]
footprint = Polygon([(0,50),(420,50),(420,0),(750,0),(750,1150),(0,1150)])
wall_polygons = [box(*bounds) for _,bounds in WALLS]
solid_plan = unary_union(wall_polygons)
free_plan = footprint.difference(solid_plan)

def polygons(geometry):
    if geometry.is_empty:
        return []
    return [geometry] if geometry.geom_type == 'Polygon' else list(geometry.geoms)

def wall_openings(name):
    return [o for o in OPENINGS if o['wall'] == name[:3]]

def opening_rect(bounds, opening):
    x0,y0,x1,y1 = bounds
    if x1-x0 < y1-y0:
        return box(x0, opening['a'], x1, opening['b'])
    return box(opening['a'], y0, opening['b'], y1)

def section(height):
    pieces = []
    for name,bounds in WALLS:
        poly = box(*bounds)
        for o in wall_openings(name):
            if o['z0'] < height < o['z1']:
                poly = poly.difference(opening_rect(bounds, o))
        pieces.append(poly)
    return unary_union(pieces)

def wall_mesh(name, bounds):
    x0,y0,x1,y1 = bounds
    vertical = x1-x0 < y1-y0
    openings = wall_openings(name)
    xs,ys,zs = {x0,x1},{y0,y1},{0,300}
    for o in openings:
        (ys if vertical else xs).update([o['a'],o['b']])
        zs.update([o['z0'],o['z1']])
    axes = list(map(sorted, (xs,ys,zs)))
    occupied = set()
    for i in range(len(axes[0])-1):
        for j in range(len(axes[1])-1):
            for k in range(len(axes[2])-1):
                mid = [(axis[n]+axis[n+1])/2 for axis,n in zip(axes,(i,j,k))]
                if not any(o['a'] < mid[1 if vertical else 0] < o['b'] and
                           o['z0'] < mid[2] < o['z1'] for o in openings):
                    occupied.add((i,j,k))
    faces,vertices,indexes = [],[],{}
    volume = 0
    for i,j,k in sorted(occupied):
        x,X = axes[0][i:i+2]
        y,Y = axes[1][j:j+2]
        z,Z = axes[2][k:k+2]
        volume += (X-x)*(Y-y)*(Z-z)
        boundary = [
            ((-1,0,0),[(x,y,z),(x,y,Z),(x,Y,Z),(x,Y,z)]),
            ((1,0,0),[(X,y,z),(X,Y,z),(X,Y,Z),(X,y,Z)]),
            ((0,-1,0),[(x,y,z),(X,y,z),(X,y,Z),(x,y,Z)]),
            ((0,1,0),[(x,Y,z),(x,Y,Z),(X,Y,Z),(X,Y,z)]),
            ((0,0,-1),[(x,y,z),(x,Y,z),(X,Y,z),(X,y,z)]),
            ((0,0,1),[(x,y,Z),(X,y,Z),(X,Y,Z),(x,Y,Z)]),
        ]
        for (di,dj,dk),points in boundary:
            if (i+di,j+dj,k+dk) in occupied:
                continue
            face = []
            for point in points:
                if point not in indexes:
                    indexes[point] = len(vertices)
                    vertices.append(point)
                face.append(indexes[point])
            faces.append(face)
    edge_counts = Counter(tuple(sorted((face[i],face[(i+1)%4]))) for face in faces for i in range(4))
    assert all(n == 2 for n in edge_counts.values()), name
    # Independent signed-volume check validates face orientation and closed shell.
    signed_volume = 0
    for face in faces:
        a,b,c,d = (np.array(vertices[i]) for i in face)
        signed_volume += np.dot(a, np.cross(b,c))/6 + np.dot(a,np.cross(c,d))/6
    assert abs(signed_volume-volume) < 1e-5, (name,signed_volume,volume)
    return dict(name=name,layer='PAREDES_EXTERNAS' if name.startswith('E') else 'PAREDES_INTERNAS',
                bounds_cm=list(bounds),vertices=vertices,faces=faces,volume_cm3=volume)

ROOMS = []
for name,seed,original in [
    ('Dormitorio 1',(150,1000),'350 x 375'),
    ('Dormitorio 2',(580,1000),'350 x 375'),
    ('Dormitorio 3',(150,600),'300 x 330'),
    ('Banheiro 1',(150,425),'150 x 330'),
    ('Banheiro 2',(580,720),'150 x 330'),
    ('Cozinha',(580,500),'300 x 330'),
]:
    poly = next(p for p in polygons(free_plan) if p.contains(Point(*seed)))
    minx,miny,maxx,maxy = poly.bounds
    ROOMS.append(dict(name=name,seed=seed,original_cm=original,
                      width_cm=maxx-minx,depth_cm=maxy-miny,
                      area_m2=poly.area/10000,polygon=list(poly.exterior.coords)))

def draw_dxf(meshes):
    doc = ezdxf.new('R2013', setup=True)
    doc.units = 5
    doc.header['$MEASUREMENT'] = 1
    doc.header['$LUNITS'] = 2
    doc.header['$LUPREC'] = 1
    for layer,color,weight in [('PAREDES_EXTERNAS',7,40),('PAREDES_INTERNAS',7,30),
                              ('PORTAS',3,15),('JANELAS',4,15),('COTAS_EXTERNAS',1,15),
                              ('COTAS_INTERNAS',8,13),('TEXTOS',7,15),('PROJECOES',8,13)]:
        doc.layers.new(layer,dxfattribs={'color':color,'lineweight':weight})
    msp = doc.modelspace()
    for name,bounds in WALLS:
        poly = box(*bounds)
        for o in wall_openings(name):
            if o['z0'] < 120 < o['z1']:
                poly = poly.difference(opening_rect(bounds,o))
        for part in polygons(poly):
            points = list(part.exterior.coords)[:-1]
            layer = 'PAREDES_EXTERNAS' if name.startswith('E') else 'PAREDES_INTERNAS'
            msp.add_lwpolyline(points,close=True,dxfattribs={'layer':layer})
            hatch = msp.add_hatch(color=7,dxfattribs={'layer':layer})
            hatch.paths.add_polyline_path(points,is_closed=True)
    for o in OPENINGS:
        name,bounds = next(w for w in WALLS if w[0].startswith(o['wall']))
        x0,y0,x1,y1 = bounds
        vertical = x1-x0 < y1-y0
        a,b=o['a'],o['b']
        if o['kind']=='porta':
            if vertical:
                hinge = (x0 if o['swing']=='W' else x1,a)
                leaf = (hinge[0] + (-1 if o['swing']=='W' else 1)*(b-a),a)
                angles = (90,180) if o['swing']=='W' else (0,90)
            else:
                hinge,leaf,angles=(a,y1),(a,y1+b-a),(0,90)
            msp.add_line(hinge,leaf,dxfattribs={'layer':'PORTAS'})
            msp.add_arc(hinge,b-a,*angles,dxfattribs={'layer':'PORTAS'})
        else:
            layer = 'PROJECOES' if o['z0']>=120 else 'JANELAS'
            for fraction in (0.25,0.75):
                if vertical:
                    points=[(x0+(x1-x0)*fraction,a),(x0+(x1-x0)*fraction,b)]
                else:
                    points=[(a,y0+(y1-y0)*fraction),(b,y0+(y1-y0)*fraction)]
                msp.add_line(*points,dxfattribs={'layer':layer})
        tx,ty = ((x0+x1)/2,(a+b)/2) if vertical else ((a+b)/2,(y0+y1)/2)
        # Tags outside exterior walls; interior doors annotated in corridor.
        if vertical:
            tx += -30 if x0==0 else (35 if x1==750 else (32 if o['wall']=='I01' else -32))
        else:
            ty -= 24
        msp.add_text(o['id'],dxfattribs={'height':9,'layer':'TEXTOS'}).set_placement((tx,ty),align=TextEntityAlignment.MIDDLE_CENTER)
    def text(value,point,height=14):
        msp.add_text(value,dxfattribs={'height':height,'layer':'TEXTOS'}).set_placement(point,align=TextEntityAlignment.MIDDLE_CENTER)
    for room in ROOMS:
        x,y=room['seed']
        text(room['name'].upper(),(x,y+15))
        text(f"{room['width_cm']:g} x {room['depth_cm']:g} cm",(x,y-7),11)
        text(f"{room['area_m2']:.2f} m2"+(' (com recorte)' if room['name'] in ('Dormitorio 1','Dormitorio 2') else ''),(x,y-26),10)
    text('ESTAR',(185,220),17)
    text('JANTAR',(580,170),17)
    text('AMBIENTES INTEGRADOS',(375,120),10)
    text('CIRCULACAO',(370,570),9)
    text('100 cm livres',(370,550),8)
    dimstyle={'dimtxt':11,'dimasz':7,'dimgap':4,'dimexo':3,'dimexe':5,'dimtad':1,'dimdec':1,'dimzin':8,'dimlfac':1,'dimclrd':1,'dimclre':1,'dimclrt':7}
    def dimension(a,b,base,angle=0,layer='COTAS_EXTERNAS'):
        dim=msp.add_linear_dim(base=base,p1=a,p2=b,angle=angle,override=dimstyle,dxfattribs={'layer':layer})
        dim.render()
    dimension((0,1150),(750,1150),(0,1260))
    dimension((0,1150),(375,1150),(0,1205))
    dimension((375,1150),(750,1150),(0,1205))
    dimension((750,0),(750,1150),(905,0),90)
    for a,b in [(0,350),(350,650),(650,800),(800,1150)]:
        dimension((750,a),(750,b),(850,0),90)
    for a,b in [(50,350),(350,500),(500,800),(800,1150)]:
        dimension((0,a),(0,b),(-90,0),90)
    dimension((0,50),(0,1150),(-145,0),90)
    dimension((0,50),(420,50),(0,-75))
    dimension((420,0),(750,0),(0,-75))
    dimension((420,0),(420,50),(790,0),90)
    dimension((320,600),(420,600),(320,625),layer='COTAS_INTERNAS')
    text('CASA 001 | JOSE DA SILVA | ETAPA 00 | REVISAO 02',(375,1350),20)
    text('ESTUDO PARA REVISAO - COTAS EM cm - NAO LIBERADO PARA OBRA',(375,1310),12)
    text('FRENTE / RUA - NORTE NAO DEFINIDO NESTA ETAPA',(375,-135),13)
    text('Paredes externas 15 cm | internas 9 cm | pe-direito 300 cm',(375,-175),11)
    text('Cadeias externas referem-se a faces externas e eixos das divisoes.',(375,-200),10)
    text('Banheiro 2 com acesso externo, conforme croqui. Implantacao e legislacao pendentes.',(375,-225),10)
    text('Portas 80 x 210 cm; entrada 90 x 210 cm. Ver quadro de vaos no memorial.',(375,-250),10)
    doc.set_modelspace_vport(1600,center=(375,560))
    path=destination('planta','dxf')
    doc.saveas(path)
    loaded=ezdxf.readfile(path)
    audit=loaded.audit()
    assert not audit.has_errors and not audit.has_fixes, (audit.errors,audit.fixes)
    assert loaded.units==5
    wall_entities=[e for e in loaded.modelspace().query('LWPOLYLINE') if e.dxf.layer.startswith('PAREDES_')]
    ext=dxf_bbox.extents(wall_entities)
    assert np.allclose(ext.extmin,(0,0,0)) and np.allclose(ext.extmax,(750,1150,0))
    reloaded_plan=unary_union([Polygon([(p[0],p[1]) for p in e.get_points()]) for e in wall_entities])
    assert reloaded_plan.symmetric_difference(section(120)).area<1e-8
    for dim in loaded.modelspace().query('DIMENSION'):
        label=list(loaded.blocks[dim.dxf.geometry].query('MTEXT'))
        assert len(label)==1
        assert abs(float(label[0].plain_text())-dim.get_measurement())<1e-7
    from ezdxf.addons.drawing import RenderContext, Frontend
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    from ezdxf.addons.drawing.config import Configuration, ColorPolicy, BackgroundPolicy
    fig=plt.figure(figsize=(10,14))
    ax=fig.add_axes([0,0,1,1])
    config=Configuration(color_policy=ColorPolicy.BLACK,background_policy=BackgroundPolicy.WHITE)
    Frontend(RenderContext(loaded),MatplotlibBackend(ax),config=config).draw_layout(loaded.modelspace(),finalize=True)
    fig.savefig(destination('conferencia_dxf','png'),dpi=170)
    plt.close(fig)
    return {'auditoria_ezdxf':'PASS, sem erros ou reparos','versao':loaded.dxfversion,'unidade':'cm',
            'secao_120cm_contra_fonte':'PASS','textos_cotas_iguais_medidas_cm':'PASS','abertura_AutoCAD_2019':'NAO TESTADA',
            'limites_paredes_cm':[[0,0],[750,1150]],'entidades':len(loaded.modelspace())}

def previews(meshes):
    fig,ax=plt.subplots(figsize=(10,14),facecolor='white')
    for part in polygons(section(120)):
        ax.add_patch(Patch(list(part.exterior.coords),facecolor='#35434a',edgecolor='#1d292f',lw=0.5))
    for o in OPENINGS:
        _,bounds=next(w for w in WALLS if w[0].startswith(o['wall']))
        x0,y0,x1,y1=bounds; a,b=o['a'],o['b']
        vertical=x1-x0<y1-y0
        if o['kind']=='porta':
            if vertical:
                hinge=(x0 if o['swing']=='W' else x1,a)
                leaf=(hinge[0]+(-1 if o['swing']=='W' else 1)*(b-a),a)
                angles=(90,180) if o['swing']=='W' else (0,90)
            else:
                hinge,leaf,angles=(a,y1),(a,y1+b-a),(0,90)
            ax.plot([hinge[0],leaf[0]],[hinge[1],leaf[1]],color='#a26738',lw=1)
            ax.add_patch(Arc(hinge,2*(b-a),2*(b-a),theta1=angles[0],theta2=angles[1],color='#a26738',lw=.6))
        else:
            center=(x0+x1)/2 if vertical else (y0+y1)/2
            ax.plot([center,center] if vertical else [a,b],[a,b] if vertical else [center,center],
                    color='#238997',lw=2,linestyle='--' if o['z0']>=120 else '-')
    for room in ROOMS:
        label=f"{room['name'].upper()}\n{room['width_cm']:g} × {room['depth_cm']:g} cm\n{room['area_m2']:.2f} m²"
        if room['name'] in ('Dormitorio 1','Dormitorio 2'):
            label+='\n(com recorte de acesso)'
        ax.text(*room['seed'],label,ha='center',va='center',fontsize=8.3,color='#20343e',linespacing=1.5)
    ax.text(190,205,'ESTAR',ha='center',fontsize=12,color='#20343e')
    ax.text(580,150,'JANTAR',ha='center',fontsize=12,color='#20343e')
    ax.text(370,560,'100 cm\nlivres',ha='center',fontsize=7,color='#20343e')
    ax.text(775,745,'Acesso\nexterno',ha='left',va='center',fontsize=7,color='#a26738')
    def dim(p,q,label,orientation='h'):
        ax.annotate('',q,p,arrowprops=dict(arrowstyle='|-|',lw=.8,color='#576b74'))
        mid=((p[0]+q[0])/2,(p[1]+q[1])/2)
        ax.text(mid[0]+(13 if orientation=='v' else 0),mid[1]+(0 if orientation=='v' else 12),label,
                ha='left' if orientation=='v' else 'center',va='center',rotation=90 if orientation=='v' else 0,fontsize=9)
    dim((0,1195),(750,1195),'750 cm')
    dim((855,0),(855,1150),'1150 cm','v')
    dim((-65,50),(-65,1150),'1100 cm','v')
    dim((0,-45),(420,-45),'420 cm')
    dim((420,-45),(750,-45),'330 cm')
    ax.text(375,-105,'FRENTE / RUA',ha='center',fontsize=10,color='#20343e')
    ax.set(xlim=(-115,970),ylim=(-135,1240),aspect='equal')
    ax.axis('off')
    fig.suptitle('CASA 001  /  ETAPA 00  /  REVISÃO 02',fontsize=17,color='#20343e',y=.97)
    fig.text(.5,.94,'Cotas externas preservadas • paredes 15/9 cm • pé-direito 300 cm',ha='center',fontsize=10)
    fig.text(.5,.045,'ESTUDO PARA REVISÃO — não liberado para obra\nDimensões dos dormitórios do fundo indicam o retângulo envolvente, com recorte.\nImplantação, ventilação e parâmetros urbanísticos ainda não validados.',ha='center',fontsize=9,linespacing=1.6)
    fig.savefig(destination('conferencia_planta','png'),dpi=160)
    plt.close(fig)
    fig=plt.figure(figsize=(12,11),facecolor='white')
    ax=fig.add_subplot(111,projection='3d')
    for mesh in meshes:
        faces=[[mesh['vertices'][i] for i in face] for face in mesh['faces']]
        ax.add_collection3d(Poly3DCollection(faces,facecolors='#d5d7d3' if mesh['name'][0]=='E' else '#e6dfca',
                                           edgecolors='#65716f',linewidths=.18,alpha=1))
    ax.set(xlim=(0,750),ylim=(0,1150),zlim=(0,320))
    ax.set_box_aspect((750,1150,450))
    ax.view_init(elev=57,azim=-65)
    ax.set_axis_off()
    fig.suptitle('CASA 001 — PAREDES / VÃOS — REVISÃO 02',fontsize=16,y=.93)
    fig.text(.5,.09,'Conferência geométrica da etapa 00 • 750 × 1150 × 300 cm\nSem cobertura, pisos ou mobiliário nesta etapa. Não é a renderização da etapa 01.',ha='center',fontsize=10)
    fig.savefig(destination('conferencia_3d','png'),dpi=150)
    plt.close(fig)

def memorial():
    room_table='\n'.join(f"| {r['name']} | {r['original_cm']} | {r['width_cm']:g} × {r['depth_cm']:g} | {r['area_m2']:.4f} |" for r in ROOMS)
    opening_table='\n'.join(f"| {o['id']} | {o['description']} | {o['b']-o['a']:g} × {o['z1']-o['z0']:g} | {o['z0']:g} |" for o in OPENINGS)
    destination('memorial','md').write_text(f'''# Casa 001 — etapa 00 — revisão 02

Situação: ajuste dimensional executado; etapa 00 parcial, para revisão. Não liberado para obra nem apresentado como projeto legal. A autorização para ajustar medidas não constitui aprovação da etapa.

## Decisão e fontes

Prevalecem as cotas externas, por instrução expressa do usuário em 2026-09-24. Registro: `HIPOTESES_DECISOES/output/2026-09-24_1631_prioridade_cotas_externas.md`.

Fontes: `00_dados/input/croqui.jpg`, `ENGINEERING.md`, `REQUISITOS/convencoes.md`, `unidades.md`, `restricoes.md`, `WORKFLOW/STEP_BY_STEP.md` e `NORMAS/plano_diretor_bh.pdf`. Carimbo preservado para a etapa de pranchas. O diagnóstico v01 permanece como histórico do conflito anterior à decisão.

## Critério geométrico

Coordenadas em centímetros: x=0 na face externa esquerda; y=0 na frente do jantar; z=0 no piso de referência; rua em y negativo. Conversões: cotas originais em m × 100 = cm; gravação interna do SketchUp em polegadas = cm / 2,54, com exibição configurada para cm.

Contorno externo: (0,50), (420,50), (420,0), (750,0), (750,1150), (0,1150). Mantidos 750 cm de largura, 1150 cm à direita, 1100 cm à esquerda e trechos frontais de 420/330 cm. Avanço do jantar calculado em 50 cm. Área geométrica encerrada pelo contorno: (750 × 1150 - 420 × 50)/10000 = 84,15 m²; não equivale a área computável legal verificada.

Intermediárias longitudinais do croqui interpretadas como eixos das divisórias: y=350/500/800 à esquerda e y=350/650/800 à direita. As faces externas das extremidades permanecem fixas. Esta referência de eixo é uma decisão de representação explicitada, pois o croqui não resolve as espessuras.

Paredes externas 15 cm, internas 9 cm e altura 300 cm. Corredor livre entre x=320 e x=420, com 100 cm de largura; fundo do vestíbulo em y=900 cm. Divisória entre dormitórios posteriores centrada em x=375 cm. A largura máxima de cada um resulta em (750 - 2 × 15 - 9)/2 = 355,5 cm. A profundidade máxima é 1150 - 15 - (800 + 4,5) = 330,5 cm. Os recortes retiram área dos retângulos máximos.

## Ambientes fechados

Dimensões antigas transcritas do texto do croqui, sem uniformizar sua ordem. Dimensões novas em x × y; áreas calculadas pelos polígonos livres, sem soleiras. Nos dormitórios posteriores, as dimensões são do retângulo envolvente e a área já desconta o recorte de acesso.

| Ambiente | Texto anterior (cm) | Dimensões novas (cm) | Área livre (m²) |
|---|---|---|---|
{room_table}

Estar e jantar permanecem integrados à circulação, sem parede divisória adicionada. Faixa do estar: x=15…420, y=65…345,5, correspondente a 405 × 280,5 cm. Faixa do jantar: x=420…735, y=15…345,5, com desconto da parede do avanço de x=420…435 até y=65; largura junto à fachada de 300 cm e no trecho interno de 315 cm. Essas faixas são referências de uso, sem áreas legais independentes atribuídas.

Área interna geométrica total, excluindo projeções de paredes e soleiras: {free_plan.area/10000:.4f} m². A circulação continua dentro dessa área; não somar novamente as faixas de uso.

## Vãos escolhidos pelo agente

Posições exatas em `jose_da_silva_00_geometria_v02.json`. Dimensões abaixo são vãos geométricos livres, não medidas comerciais de folhas. Portas, janelas e materiais de esquadrias não são sólidos do SKP nesta etapa de paredes; as portas têm representação simbólica no DXF.

| Vão | Uso | Largura × altura (cm) | Base acima do piso (cm) |
|---|---|---|---|
{opening_table}

O banheiro 2 mantém o acesso externo do croqui; depende de passagem lateral na implantação. A bandeira acima da porta é proposta do agente, não cota observada. Janelas altas são indicadas por projeção na prévia. Abertura V01 representa o vão entre cozinha e jantar, não ventilação direta ao exterior. Ventilação efetiva, iluminação, segurança, acessibilidade e dimensionamento de vergas ainda não foram validados; a geometria não constitui dimensionamento estrutural.

## Lote e conferência urbanística

Lote informado de 1050 × 2000 cm = 210 m². A casa deixa uma diferença dimensional de 300 cm na largura e 850 cm no comprimento, antes de definir implantação e muros. Como teste de encaixe, uma distribuição de 150 cm em cada lateral e 550 cm à frente / 300 cm atrás fecha essas dimensões. São valores hipotéticos de teste, não recuos legais adotados.

Dois envelopes hipotéticos de veículos de 250 × 500 cm cabem lado a lado na faixa frontal desse teste; isto não valida garagem, manobras, portões, passeio, cobertura ou área permeável. A posição final da casa e as duas vagas ainda dependem da conferência do lote. Não foi iniciada a planta de implantação da etapa 02.

A [PBH indica Geosiurbe/BHMap para consulta cadastral e dos parâmetros geográficos](https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/base-de-dados). A [página oficial do Plano Diretor](https://prefeitura.pbh.gov.br/politica-urbana/planejamento-urbano/plano-diretor/proposta), consultada em 2026-09-24, distingue o texto legal dos e-books explicativos. O e-book local não identifica sozinho as condições específicas do lote. Após autorização do usuário para buscar pelo lote, foi consultado o serviço WFS publicado na [página oficial de acesso aos dados](https://prefeitura.pbh.gov.br/bhgeo/acesso-aos-dados): 43 registros de endereço da Rua Oliveira no Cruzeiro, nenhum com número 1356; a pesquisa alternativa por CEP 30310150 e número 1356 também retornou zero registros. Isso não prova inexistência do imóvel, mas impede identificá-lo com os dados atuais. Evidências integrais, filtros e horários preservados em `consulta_lote_v02/`. Não inferir zoneamento pelo bairro nem escolher lote por similaridade de área. Registro: `HIPOTESES_DECISOES/output/2026-09-24_1636_consulta_lote.md`.

Pendente: índice cadastral do IPTU ou identificação de zona/quadra/lote para consulta confiável; depois verificar recuos, ocupação, permeabilidade, eventuais restrições e aberturas. Nenhum valor normativo foi inventado e nenhuma conformidade legal é declarada.

## Arquivos, método e testes

- `jose_da_silva_00_planta_v02.dxf`: DXF AC1027, modelspace em cm, paredes, símbolos de vãos, ambientes e cotas de conferência. Para abertura no AutoCAD 2019; não testado pela interface do AutoCAD.
- `jose_da_silva_00_paredes_v02.skp`: formato SketchUp 2016, 16 grupos de paredes, layers e materiais; sem faces ou arestas soltas na raiz. Sem pisos, mobiliário e cobertura, conforme saída de paredes da etapa 00.
- `jose_da_silva_00_geometria_v02.json`: fonte comum de coordenadas, ambientes, vãos e malhas.
- `jose_da_silva_00_conferencia_planta_v02.png` e `jose_da_silva_00_conferencia_3d_v02.png`: prévias técnicas calculadas da mesma fonte; não são os renders por IA da etapa 01 nem pranchas finais.
- `jose_da_silva_00_conferencia_dxf_v02.png`: visualização do próprio DXF reaberto, usada para conferir sua representação e os textos de cotas.
- `jose_da_silva_00_validacao_v02.json`: resultados e hashes das fontes/saídas; versões das ferramentas.
- Scripts `jose_da_silva_00_gerar_v02.py` e `jose_da_silva_00_skp_api_v02.py`: geração reproduzível. ezdxf 1.4.4 instalado apenas em `00_dados/output/ferramentas/python`; demais versões no relatório de validação. Biblioteca SketchUpAPI 16.1.1449 da instalação local.

Reprodução a partir da raiz: `python 00_dados/output/jose_da_silva_00_gerar_v02.py`. Regenera os derivados v02; para uma nova decisão emitida, criar nova revisão antes de alterar parâmetros. Não executar o script de diagnóstico v01 para gerar a geometria.

Testes executados: contorno e espessuras; ausência de sobreposição volumétrica entre paredes; vãos contidos e sem colisão entre si; cada malha fechada e volume orientado coerente; DXF reaberto sem erros/reparos e seção a 120 cm idêntica à fonte; textos de todas as cotas comparados numericamente com suas medidas em cm (fator de exibição explicitamente 1); SKP salvo e reaberto pela biblioteca 2016, limites 750 × 1150 × 300 cm, cm como unidade exibida e duas faces por aresta de cada grupo. Inspeção visual das prévias e da visualização do DXF. Testes pela interface gráfica dos aplicativos permanecem pendentes.

## Continuidade

A correção dimensional está concluída nesta revisão. A etapa 00 permanece parcial, com conferência cadastral/urbanística, implantação e revisão dos entregáveis pendentes. Somente depois de satisfeitas as validações e aprovada a etapa 00 executar as etapas seguintes, conforme `WORKFLOW/STEP_BY_STEP.md`. A solicitação de dados cadastrais não altera as cotas externas nem reabre a decisão já autorizada.
''',encoding='utf-8')

def main():
    assert footprint.area==841500
    assert all(footprint.covers(p) for p in wall_polygons)
    assert abs(sum(p.area for p in wall_polygons)-solid_plan.area)<1e-8
    assert 420-320==100
    for name,bounds in WALLS:
        x0,y0,x1,y1=bounds
        assert min(x1-x0,y1-y0)==(15 if name[0]=='E' else 9)
        openings=wall_openings(name)
        for o in openings:
            assert box(*bounds).covers(opening_rect(bounds,o))
            assert 0<=o['z0']<o['z1']<=300
        for i,a in enumerate(openings):
            for b in openings[i+1:]:
                assert not (max(a['a'],b['a'])<min(a['b'],b['b']) and max(a['z0'],b['z0'])<min(a['z1'],b['z1']))
    meshes=[wall_mesh(*wall) for wall in WALLS]
    data=dict(revisao='02',unidade='cm',origem='x=0 na face externa esquerda; y=0 na frente do jantar; rua em y negativo',
              contorno=list(footprint.exterior.coords),paredes=WALLS,vaos=OPENINGS,
              ambientes=ROOMS,meshes=meshes,area_contorno_m2=footprint.area/10000,
              area_interna_sem_soleiras_m2=free_plan.area/10000,area_lote_m2=210)
    destination('geometria','json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    dxf_result=draw_dxf(meshes)
    api=API()
    try:
        previous = destination('validacao','json')
        hashes = json.loads(previous.read_text(encoding='utf-8')).get('saidas_sha256',{}) if previous.exists() else {}
        stable = all(p.exists() and hashes.get(p.name)==sha(p)
                     for p in (destination('paredes','skp'),destination('geometria','json')))
        # Reuse an already validated identical model; do not replace an open SKP unnecessarily.
        skp_result=(api.audit(destination('paredes','skp'),meshes) if stable
                    else api.create(destination('paredes','skp'),meshes))
    finally:
        api.close()
    previews(meshes)
    memorial()
    timestamp=datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat()
    assert source_hashes=={str(p.relative_to(ROOT)):sha(p) for p in source_files}
    checks=dict(data=timestamp,fontes_sha256=source_hashes,fontes_preservadas=True,
                contorno_area_m2=84.15,corredor_livre_cm=100,paredes_sem_sobreposicao=True,
                malhas_fechadas_e_volume_orientado='PASS',dxf=dxf_result,skp=skp_result,
                versoes=dict(python=sys.version,ezdxf=ezdxf.__version__,shapely=shapely.__version__,
                             numpy=np.__version__,matplotlib=matplotlib.__version__,sketchup_api='16.1.1449'),
                conformidade_legal='PENDENTE',aprovacao_etapa_00='PENDENTE')
    checks['saidas_sha256']={p.name:sha(p) for p in OUT.glob(f'{PREFIX}_*_v02.*')
                             if p.suffix not in ('.py','.pyc') and 'validacao' not in p.name}
    destination('validacao','json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'DXF':dxf_result,'SKP':skp_result,'areas':ROOMS},ensure_ascii=True,indent=2))

if __name__=='__main__':
    main()
