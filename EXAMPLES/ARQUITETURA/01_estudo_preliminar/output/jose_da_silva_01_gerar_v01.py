"""Modelo preliminar paramétrico; cm; fontes da etapa 00 preservadas."""
from pathlib import Path
import os,sys,json,hashlib,math
from collections import Counter
from datetime import datetime
from zoneinfo import ZoneInfo
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
BASE=ROOT/'00_dados/output'
os.environ['MPLCONFIGDIR']=str(OUT/'ferramentas/matplotlib')
import numpy as np
from shapely.geometry import Polygon,Point,box
from shapely.geometry.polygon import orient
from shapely.ops import unary_union
from shapely.affinity import translate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as Patch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from jose_da_silva_01_skp_v01 import StudyAPI

PREFIX='jose_da_silva_01'
def path(kind,suffix):return OUT/f'{PREFIX}_{kind}_v01.{suffix}'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_paths=[BASE/'jose_da_silva_00_geometria_v02.json',BASE/'jose_da_silva_00_paredes_v02.skp',
              BASE/'jose_da_silva_00_planta_v02.dxf',ROOT/'00_dados/input/croqui.jpg',
              ROOT/'REQUISITOS/convencoes.md',ROOT/'REQUISITOS/unidades.md',
              ROOT/'HIPOTESES_DECISOES/output/2026-09-24_1802_aprovacao_00_estudo_01.md']
source_hashes={str(p.relative_to(ROOT)):sha(p) for p in source_paths}
data=json.loads(source_paths[0].read_text(encoding='utf-8'))
PALETTE={
 'Branco_quente':(234,232,222),'Areia':(206,196,175),'Madeira_clara':(173,129,82),
 'Madeira_escura':(107,76,48),'Grafite':(49,55,57),'Cinza_piso':(190,193,189),
 'Pedra_clara':(221,218,207),'Tecido_cru':(213,206,190),'Tecido_azul':(77,106,118),
 'Roupa_cama':(244,241,232),'Oliva':(118,130,95),'Ceramica_branca':(242,243,236),
 'Vidro':(140,184,190,.28),'Espelho':(141,177,184),'Inox':(151,160,162),
 'Preto':(28,32,34),'Grama':(119,145,100),'Folhagem':(70,113,74),
 'Tronco':(115,84,52),'Piso_externo':(171,172,161),'Metal_cobertura':(143,150,150),
 'Carro_prata':(179,188,193),'Carro_cinza':(84,96,105),'Vidro_carro':(59,92,105),
 'Luz_quente':(248,220,154),
}
MESHES=[];FURNITURE=[]
def mesh(name,obj,layer,material,vertices,faces,local=True):
    vertices=np.array(vertices,dtype=float)
    if local:vertices+=np.array([150,600,0])
    edge_count=Counter(tuple(sorted((f[i],f[(i+1)%len(f)]))) for f in faces for i in range(len(f)))
    assert all(v==2 for v in edge_count.values()),name
    m=dict(name=name,object=obj,layer=layer,material=material,vertices=vertices.tolist(),faces=faces)
    MESHES.append(m);return m

def prism(name,obj,layer,material,poly,z0,z1,local=True,slope=0):
    assert poly.geom_type=='Polygon' and not poly.interiors,name
    points=list(orient(poly,sign=1).exterior.coords)[:-1];n=len(points)
    vertices=[(x,y,z0+slope*y) for x,y in points]+[(x,y,z1+slope*y) for x,y in points]
    faces=[list(reversed(range(n))),list(range(n,2*n))]
    faces += [[i,(i+1)%n,(i+1)%n+n,i+n] for i in range(n)]
    return mesh(name,obj,layer,material,vertices,faces,local)

def cub(name,obj,layer,material,bounds,local=True,r=0):
    x,y,z,X,Y,Z=bounds
    assert X>x and Y>y and Z>z,(name,bounds)
    poly=box(x,y,X,Y) if not r else box(x+r,y+r,X-r,Y-r).buffer(r,quad_segs=3)
    return prism(name,obj,layer,material,poly,z,Z,local)

def ellipsoid(name,obj,layer,material,center,radii,local=True):
    cx,cy,cz=center;rx,ry,rz=radii;sectors=16;rings=7
    vertices=[(cx,cy,cz-rz)]
    for ring in range(1,rings):
        phi=-math.pi/2+math.pi*ring/rings
        for i in range(sectors):
            a=2*math.pi*i/sectors
            vertices.append((cx+rx*math.cos(phi)*math.cos(a),cy+ry*math.cos(phi)*math.sin(a),cz+rz*math.sin(phi)))
    vertices.append((cx,cy,cz+rz));top=len(vertices)-1
    faces=[[0,1+(i+1)%sectors,1+i] for i in range(sectors)]
    for j in range(rings-2):
        a=1+j*sectors;b=a+sectors
        faces += [[a+i,a+(i+1)%sectors,b+(i+1)%sectors,b+i] for i in range(sectors)]
    a=1+(rings-2)*sectors
    faces += [[a+i,a+(i+1)%sectors,top] for i in range(sectors)]
    return mesh(name,obj,layer,material,vertices,faces,local)

def occupy(name,room,bounds):
    FURNITURE.append(dict(name=name,room=room,bounds_cm=bounds))

def bed(name,room,x,y,w,l,blanket):
    layer='MOBILIARIO_QUARTOS';occupy(name,room,[x,y,x+w,y+l])
    cub('Base',name,layer,'Madeira_escura',(x,y,8,x+w,y+l,28),r=3)
    cub('Colchao',name,layer,'Roupa_cama',(x+1,y+1,28,x+w-1,y+l-1,50),r=5)
    cub('Cobre_leito',name,layer,blanket,(x+1,y+1,50,x+w-1,y+l-48,53),r=3)
    cub('Cabeceira',name,layer,'Tecido_cru',(x,y+l-4,28,x+w,y+l,105),r=1)
    for i in range(2 if w>100 else 1):
        pw=(w-15)/ (2 if w>100 else 1)
        cub(f'Travesseiro_{i+1}',name,layer,'Roupa_cama',(x+6+i*(pw+2),y+l-43,51,x+6+i*(pw+2)+pw-3,y+l-9,63),r=5)
    for xx in (x+5,x+w-9):
        for yy in (y+5,y+l-9):cub('Pe',name,layer,'Madeira_escura',(xx,yy,0,xx+4,yy+4,8))

def cabinet(name,room,bounds):
    x,y,X,Y=bounds;layer='MOBILIARIO_QUARTOS';occupy(name,room,bounds)
    cub('Corpo',name,layer,'Madeira_clara',(x,y,0,X,Y,235))
    if X-x>Y-y:
        for xx in np.linspace(x+3,X-3,4):cub('Junta_porta',name,layer,'Madeira_escura',(xx,y-.2,5,xx+.25,y+.2,230))
    else:
        for yy in np.linspace(y+3,Y-3,4):cub('Junta_porta',name,layer,'Madeira_escura',(x-.2,yy,5,x+.2,yy+.25,230))

def chair(name,x,y,orientation='N'):
    obj=name;layer='MOBILIARIO_SOCIAL'
    cub('Assento',obj,layer,'Tecido_cru',(x,y,42,x+45,y+45,49),r=4)
    if orientation in ('N','S'):
        yy=y+40 if orientation=='N' else y
        cub('Encosto',obj,layer,'Madeira_clara',(x,yy,49,x+45,yy+5,88),r=1)
    else:
        xx=x if orientation=='W' else x+40
        cub('Encosto',obj,layer,'Madeira_clara',(xx,y,49,xx+5,y+45,88),r=1)
    for xx in (x+3,x+38):
        for yy in (y+3,y+38):cub('Pe',obj,layer,'Madeira_escura',(xx,yy,0,xx+4,yy+4,42))

def bathroom(number,offsetx,offsety):
    layer='LOUCAS_BANCADAS';room=f'Banheiro {number}'
    # Same arrangement translated from left bathroom to right bathroom.
    x=offsetx;y=offsety
    shower=f'B{number}_Box';occupy(shower,room,[x+5,y+5,x+85,y+136])
    cub('Piso_box',shower,layer,'Pedra_clara',(x+5,y+5,0,x+85,y+136,1))
    cub('Painel_vidro',shower,'ESQUADRIAS_VIDRO','Vidro',(x+84,y+5,1,x+85,y+85,205))
    cub('Perfil',shower,layer,'Grafite',(x+83,y+5,1,x+86,y+7,205))
    cub('Ducha',shower,layer,'Inox',(x+10,y+60,210,x+35,y+82,213))
    cub('Ralo',shower,layer,'Inox',(x+38,y+67,1,x+48,y+77,1.3))
    wc=f'B{number}_Sanitario';occupy(wc,room,[x+138,y+6,x+180,y+71])
    cub('Caixa_acoplada',wc,layer,'Ceramica_branca',(x+140,y+6,30,x+178,y+22,78),r=3)
    ellipsoid('Base',wc,layer,'Ceramica_branca',(x+159,y+43,21),(17,23,21))
    ellipsoid('Assento',wc,layer,'Ceramica_branca',(x+159,y+47,43),(21,24,4))
    ellipsoid('Cavidade_indicativa',wc,layer,'Cinza_piso',(x+159,y+47,46.5),(12,16,.7))
    vanity=f'B{number}_Lavatorio';occupy(vanity,room,[x+230,y+5,x+286,y+40])
    cub('Gabinete',vanity,layer,'Madeira_clara',(x+230,y+5,25,x+286,y+40,80),r=1)
    cub('Bancada',vanity,layer,'Pedra_clara',(x+230,y+5,80,x+286,y+40,84),r=1)
    ellipsoid('Cuba',vanity,layer,'Ceramica_branca',(x+258,y+23,87),(19,12,7))
    ellipsoid('Fundo_cuba',vanity,layer,'Cinza_piso',(x+258,y+23,92),(14,8,.5))
    cub('Torneira',vanity,layer,'Inox',(x+255,y+7,84,x+259,y+11,108))
    cub('Espelho',vanity,layer,'Espelho',(x+232,y+.5,110,x+284,y+1.5,180))

def generate():
    footprint=Polygon(data['contorno'])
    cub('Terreno','Lote','TERRENO','Grama',(0,0,-15,1050,2000,-5),local=False)
    prism('Base_geometrica','Base_casa','PISOS','Pedra_clara',footprint,-12,-1)
    walls=unary_union([box(*bounds) for _,bounds in data['paredes']])
    free=footprint.difference(walls)
    for i,poly in enumerate(free.geoms):
        room=next((r for r in data['ambientes'] if poly.contains(Point(*r['seed']))),None)
        mat='Madeira_clara' if room and room['name'].startswith('Dormitorio') else 'Cinza_piso'
        prism('Acabamento',f'Piso_{room["name"] if room else "Estar_Jantar_Circulacao"}','PISOS',mat,poly,-1,0)
    bed('D1_Cama_1','Dormitorio 1',35,940,90,188,'Tecido_azul')
    bed('D1_Cama_2','Dormitorio 1',200,940,90,188,'Oliva')
    cabinet('D1_Armario','Dormitorio 1',[20,810,210,865])
    occupy('D1_Criado','Dormitorio 1',[140,1080,185,1125])
    cub('Criado','D1_Criado','MOBILIARIO_QUARTOS','Madeira_clara',(140,1080,0,185,1125,48),r=2)
    bed('D2_Cama_casal','Dormitorio 2',520,930,158,198,'Areia')
    cabinet('D2_Armario','Dormitorio 2',[520,810,730,865])
    for i,x in enumerate((475,690)):
        occupy(f'D2_Criado_{i}','Dormitorio 2',[x,1080,x+35,1125])
        cub('Criado',f'D2_Criado_{i}','MOBILIARIO_QUARTOS','Madeira_clara',(x,1080,0,x+35,1125,48),r=2)
    bed('D3_Cama_casal','Dormitorio 3',45,540,138,188,'Oliva')
    cabinet('D3_Armario','Dormitorio 3',[251,515,306,645])
    bathroom(1,15,354.5)
    bathroom(2,429,654.5)
    # Kitchen: three work zones; no island obstructing circulation.
    layer='COZINHA'
    occupy('Cozinha_bancada','Cozinha',[435,585,730,642])
    cub('Gabinetes','Cozinha_bancada',layer,'Madeira_clara',(435,585,10,730,642,86))
    cub('Tampo','Cozinha_bancada',layer,'Pedra_clara',(435,585,86,730,642,90))
    cub('Cuba','Cozinha_bancada',layer,'Inox',(530,595,90,585,632,91),r=4)
    cub('Interior_cuba','Cozinha_bancada',layer,'Grafite',(535,600,91,580,627,91.3),r=4)
    cub('Torneira','Cozinha_bancada',layer,'Inox',(555,634,90,559,638,115))
    cub('Cooktop','Cozinha_bancada',layer,'Preto',(650,592,90,710,636,92),r=2)
    for x in (664,696):
        for y in (604,624):prism('Queimador','Cozinha_bancada',layer,'Inox',Point(x,y).buffer(7,quad_segs=5),92,93)
    cub('Armario_superior','Cozinha_superior',layer,'Branco_quente',(435,612,150,625,642,230))
    cub('Coifa','Cozinha_coifa',layer,'Inox',(646,610,165,716,642,185))
    occupy('Geladeira','Cozinha',[435,505,500,575])
    cub('Corpo','Geladeira',layer,'Inox',(435,505,0,500,575,185),r=3)
    cub('Puxador','Geladeira',layer,'Grafite',(497,510,100,503,514,160))
    occupy('Bancada_apoio','Cozinha',[435,390,490,495])
    cub('Gabinete','Bancada_apoio',layer,'Madeira_clara',(435,390,10,490,495,86))
    cub('Tampo','Bancada_apoio',layer,'Pedra_clara',(435,390,86,490,495,90))
    # Living and dining room.
    layer='MOBILIARIO_SOCIAL'
    occupy('Sofa','Estar',[22,110,107,330])
    cub('Base','Sofa',layer,'Tecido_cru',(22,110,10,107,330,33),r=6)
    cub('Encosto','Sofa',layer,'Tecido_cru',(22,110,33,43,330,88),r=6)
    for i,y in enumerate((125,190,255)):
        cub('Almofada_assento','Sofa',layer,'Areia',(44,y,33,100,y+60,49),r=6)
    for y in (110,315):cub('Braco','Sofa',layer,'Tecido_cru',(30,y,33,107,y+15,68),r=5)
    cub('Tapete','Tapete_estar','DECORACAO','Areia',(115,110,.1,267,310,.6),r=4)
    occupy('Mesa_centro','Estar',[147,180,217,240])
    cub('Tampo','Mesa_centro',layer,'Madeira_clara',(147,180,34,217,240,39),r=9)
    cub('Base','Mesa_centro',layer,'Grafite',(166,195,0,198,226,34),r=4)
    occupy('Rack_TV','Estar',[282,150,307,285])
    cub('Rack','Rack_TV',layer,'Madeira_clara',(282,150,0,307,285,45),r=1)
    cub('Tela','Rack_TV',layer,'Preto',(297,172,85,301,268,145))
    cub('Pe_TV','Rack_TV',layer,'Grafite',(292,205,45,301,235,85))
    occupy('Mesa_jantar','Jantar',[530,100,610,250])
    cub('Tampo','Mesa_jantar',layer,'Madeira_clara',(530,100,73,610,250,78),r=6)
    for x in (538,599):
        for y in (112,235):cub('Pe','Mesa_jantar',layer,'Madeira_escura',(x,y,0,x+4,y+4,73))
    for i,(x,y,side) in enumerate([(480,110,'W'),(480,200,'W'),(615,110,'E'),(615,200,'E'),(547,50,'S'),(547,255,'N')]):
        occupy(f'Cadeira_{i+1}','Jantar',[x,y,x+45,y+45]);chair(f'Cadeira_{i+1}',x,y,side)
    ellipsoid('Vaso','Centro_mesa','DECORACAO','Ceramica_branca',(570,175,85),(9,9,7))
    # Doors in their 90-degree open position and window frames in approved openings.
    for o in data['vaos']:
        _,bounds=next(w for w in data['paredes'] if w[0].startswith(o['wall']))
        x0,y0,x1,y1=bounds;a,b=o['a'],o['b'];z,Z=o['z0'],o['z1'];v=x1-x0<y1-y0
        obj=o['id']+'_'+o['description'];layer='ESQUADRIAS'
        if o['kind']=='porta':
            if v:
                xx=x0-(b-a) if o['swing']=='W' else x1
                cub('Folha_aberta',obj,layer,'Madeira_clara',(xx,a,0,xx+b-a,a+3,208))
            else:cub('Folha_aberta',obj,layer,'Madeira_clara',(a,y1,0,a+3,y1+b-a,208))
        else:
            if v:
                xc=(x0+x1)/2
                cub('Vidro',obj,'ESQUADRIAS_VIDRO','Vidro',(xc-.4,a+4,z+4,xc+.4,b-4,Z-4))
                for yy in (a,b-4):cub('Montante',obj,layer,'Grafite',(xc-2,yy,z,xc+2,yy+4,Z))
                for zz in (z,Z-4):cub('Travessa',obj,layer,'Grafite',(xc-2,a,zz,xc+2,b,zz+4))
            else:
                yc=(y0+y1)/2
                cub('Vidro',obj,'ESQUADRIAS_VIDRO','Vidro',(a+4,yc-.4,z+4,b-4,yc+.4,Z-4))
                for xx in (a,b-4):cub('Montante',obj,layer,'Grafite',(xx,yc-2,z,xx+4,yc+2,Z))
                for zz in (z,Z-4):cub('Travessa',obj,layer,'Grafite',(a,yc-2,zz,b,yc+2,zz+4))
    # Roof hidden in the interior scene, available in the facade scene.
    prism('Forro_volume','Cobertura_casa','COBERTURA','Branco_quente',footprint,300,310)
    for name,bounds in data['paredes']:
        if name.startswith('E'):
            x,y,X,Y=bounds;cub('Platibanda_'+name,'Platibanda','COBERTURA','Branco_quente',(x,y,300,X,Y,360))
    prism('Telhado_oculto','Cobertura_casa','COBERTURA','Metal_cobertura',footprint.buffer(-15,join_style=2),315,318,slope=.03)
    # Site, pedestrian route and two parking envelopes.
    routes=[(25,15,125,625),(125,525,560,625),(470,625,560,650),(900,525,1035,1750)]
    for i,(x,y,X,Y) in enumerate(routes):cub('Piso',f'Caminho_{i}','EXTERIORES','Piso_externo',(x,y,-5,X,Y,0),local=False)
    cub('Piso','Garagem_piso','EXTERIORES','Piso_externo',(150,15,-5,730,525,0),local=False)
    for i,(x,X) in enumerate(((175,425),(450,700)),1):
        body='Carro_'+str(i);col='Carro_prata' if i==1 else 'Carro_cinza'
        cub('Carroceria',body,'VEICULOS',col,(x+28,60,30,X-28,490,100),local=False,r=20)
        cub('Cabine',body,'VEICULOS','Vidro_carro',(x+42,185,100,X-42,370,148),local=False,r=20)
        cub('Teto',body,'VEICULOS',col,(x+48,215,148,X-48,340,152),local=False,r=15)
        for xx in (x+29,X-29):
            for yy in (145,410):ellipsoid('Pneu',body,'VEICULOS','Preto',(xx,yy,32),(12,31,31),local=False)
    for x in (150,722):
        for y in (25,517):cub('Pilar','Garagem_estrutura','EXTERIORES','Grafite',(x,y,0,x+8,y+8,250),local=False)
    cub('Cobertura','Garagem_cobertura','GARAGEM_COBERTURA','Grafite',(150,25,250,730,525,257),local=False)
    # Perimeter and gates: controlled pedestrian entrance separate from vehicle gate.
    for i,b in enumerate([(0,15,0,15,1985,210),(1035,15,0,1050,1985,210),(0,1985,0,1050,2000,210),
                          (0,0,0,25,15,210),(125,0,0,150,15,210),(730,0,0,1050,15,210)]):
        cub('Muro',f'Muro_{i}','MUROS_PORTOES','Branco_quente',b,local=False)
    for label,x,X in [('Portao_pedestre',25,125),('Portao_veiculos',150,730)]:
        for z in range(0,210,10):cub('Lamina',label,'MUROS_PORTOES','Grafite',(x,5,z,X,10,z+6),local=False)
    for i,(x,y,radius) in enumerate([(220,1860,65),(800,1870,80)]):
        prism('Tronco',f'Arvore_{i}','PAISAGISMO','Tronco',Point(x,y).buffer(7,quad_segs=4),-5,165,local=False)
        ellipsoid('Copa',f'Arvore_{i}','PAISAGISMO','Folhagem',(x,y,210),(radius,radius,75),local=False)
    for i,(x,y) in enumerate([(80,760),(80,1040),(80,1420),(80,1650),(830,430),(980,1840)]):
        ellipsoid('Arbusto',f'Jardim_{i}','PAISAGISMO','Folhagem',(x,y,30),(35,35,35),local=False)

def validate():
    room_polys={r['name']:Polygon(r['polygon']) for r in data['ambientes']}
    footprint=Polygon(data['contorno']);walls=unary_union([box(*b) for _,b in data['paredes']])
    free=footprint.difference(walls)
    for f in FURNITURE:
        region=room_polys.get(f['room'],free)
        assert region.covers(box(*f['bounds_cm'])),('Fora do ambiente',f)
    for i,a in enumerate(FURNITURE):
        for b in FURNITURE[i+1:]:
            assert box(*a['bounds_cm']).intersection(box(*b['bounds_cm'])).area<1e-8,('Sobreposicao de mobiliario',a['name'],b['name'])
    for o in data['vaos']:
        if o['kind']!='porta':continue
        _,bounds=next(w for w in data['paredes'] if w[0].startswith(o['wall']))
        x0,y0,x1,y1=bounds;a,b=o['a'],o['b'];r=b-a
        if x1-x0<y1-y0:
            hinge=(x0 if o['swing']=='W' else x1,a);angles=(90,180) if o['swing']=='W' else (0,90)
        else:hinge=(a,y1);angles=(0,90)
        sweep=Polygon([hinge]+[(hinge[0]+r*math.cos(t),hinge[1]+r*math.sin(t)) for t in np.radians(np.linspace(*angles,49))])
        for f in FURNITURE:
            assert sweep.intersection(box(*f['bounds_cm'])).area<1e-6,('Giro da porta',o['id'],f['name'])
    lot=box(0,0,1050,2000);house=translate(footprint,150,600)
    paths=[box(25,15,125,625),box(125,525,560,625),box(470,625,560,650)]
    assert all(lot.covers(p) and p.intersection(house).area==0 for p in paths)
    for parking in (box(175,25,425,525),box(450,25,700,525)):
        assert lot.covers(parking) and parking.intersection(house).area==0
        assert all(parking.intersection(p).area==0 for p in paths)
    assert source_hashes=={str(p.relative_to(ROOT)):sha(p) for p in source_paths}
    return dict(mobiliario_contido='PASS',colisoes_mobiliario='ZERO',giros_portas_livres='PASS',
                caminho_pedonal_sem_sobreposicao='PASS',caminho_pedonal_nominal_cm=100,
                passagem_D3_entre_cama_armario_cm=68,acessibilidade_normativa='NAO VERIFICADA',
                manobras_veiculos='NAO SIMULADAS',fontes_preservadas=True)

def references():
    # Geometric references for image generation, not substitutes for requested AI renders.
    roof={'COBERTURA','GARAGEM_COBERTURA'}
    fig,ax=plt.subplots(figsize=(9,15))
    for m in sorted(MESHES,key=lambda m:np.max(np.array(m['vertices'])[:,2])):
        if m['layer'] in roof or m['layer']=='MUROS_PORTOES':continue
        vertices=np.array(m['vertices']);color=np.array(PALETTE[m['material']][:3])/255
        for face in m['faces']:
            points=vertices[face];poly=Polygon(points[:,:2])
            if poly.is_valid and poly.area>1:
                ax.add_patch(Patch(points[:,:2],facecolor=color,edgecolor='#535953',linewidth=.18))
    for name,bounds in data['paredes']:
        wall=box(*bounds);x,y,X,Y=bounds
        for opening in data['vaos']:
            if opening['wall']==name[:3] and opening['z0']<120<opening['z1']:
                a,b=opening['a'],opening['b']
                wall=wall.difference(box(x,a,X,b) if X-x<Y-y else box(a,y,b,Y))
        for poly in ([wall] if wall.geom_type=='Polygon' else wall.geoms):
            pts=np.array(poly.exterior.coords)+[150,600]
            ax.add_patch(Patch(pts,facecolor='#e6e4d7',edgecolor='#5d655f',lw=.3))
    ax.set(xlim=(-30,1080),ylim=(-30,2030),aspect='equal');ax.axis('off')
    fig.tight_layout(pad=.2);fig.savefig(path('referencia_superior','png'),dpi=160);plt.close(fig)
    from jose_da_silva_01_vistas_v01 import render
    wall_meshes=[dict(vertices=(np.array(m['vertices'])+[150,600,0]).tolist(),faces=m['faces'],material='Branco_quente') for m in data['meshes']]
    render(MESHES+wall_meshes,PALETTE,path('referencia_fachada','png'))

def main():
    generate();tests=validate()
    source=dict(units='cm',house_origin_cm=[150,600,0],house_source='00_dados/output/jose_da_silva_00_geometria_v02.json',
                palette=PALETTE,furniture=FURNITURE,meshes=MESHES)
    path('geometria','json').write_text(json.dumps(source,ensure_ascii=False,indent=2),encoding='utf-8')
    api=StudyAPI()
    try:tests['skp']=api.build(BASE/'jose_da_silva_00_paredes_v02.skp',path('mobiliado','skp'),MESHES,PALETTE)
    finally:api.close()
    references()
    tests.update(data=datetime.now(ZoneInfo('America/Sao_Paulo')).isoformat(),fontes_sha256=source_hashes,
                 numero_itens_mobiliario=len(FURNITURE),numero_partes=len(MESHES),
                 saidas_sha256={p.name:sha(p) for p in OUT.glob(f'{PREFIX}_*_v01.*') if p.suffix in ('.skp','.json','.png') and 'validacao' not in p.name})
    path('validacao','json').write_text(json.dumps(tests,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(tests,ensure_ascii=True,indent=2))

if __name__=='__main__':main()
