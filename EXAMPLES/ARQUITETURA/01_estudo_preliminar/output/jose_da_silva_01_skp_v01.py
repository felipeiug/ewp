"""Acrescenta estudo ao SKP aprovado, preservando suas paredes como grupos."""
import sys
from pathlib import Path
import ctypes as C
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'00_dados/output'))
from jose_da_silva_00_skp_api_v02 import API, R, S, B, P, Point, Bounds, Color

class Transform(C.Structure):
    _fields_=[('values',C.c_double*16)]

class StudyAPI(API):
    def __init__(self):
        super().__init__()
        signatures={
            'SUGroupSetTransform':[R,P(Transform)],
            'SUGroupGetTransform':[R,P(Transform)],
            'SUMaterialSetOpacity':[R,C.c_double],
            'SUMaterialSetUseOpacity':[R,C.c_bool],
            'SULayerSetVisibility':[R,C.c_bool],
            'SUCameraCreate':[P(R)],'SUCameraRelease':[P(R)],
            'SUSceneCreate':[P(R)],'SUSceneSetName':[R,C.c_char_p],
            'SUModelAddScenes':[R,S,P(R)],'SUSceneSetCamera':[R,R],
            'SUSceneSetUseCamera':[R,C.c_bool],
            'SUSceneSetUseHiddenLayers':[R,C.c_bool],
            'SUSceneAddLayer':[R,R],
            'SUModelGetNumScenes':[R,P(S)],
            'SUModelGetNumLayers':[R,P(S)],
            'SUModelGetNumMaterials':[R,P(S)],
            'SUEdgeGetFaces':[R,S,P(R),P(S)],'SUFaceGetNormal':[R,P(Point)],
            'SUDrawingElementSetHidden':[R,C.c_bool],
        }
        for name,args in signatures.items():
            fn=getattr(self.dll,name); fn.restype=C.c_int; fn.argtypes=args
        self.dll.SUEdgeToDrawingElement.restype=R
        self.dll.SUEdgeToDrawingElement.argtypes=[R]

    def group(self,entities,name):
        group=self.new('SUGroupCreate')
        self.call('SUGroupSetName',group,name.encode('utf-8'))
        self.call('SUEntitiesAddGroup',entities,group)
        return group,self.new('SUGroupGetEntities',group)

    def fill(self,entities,mesh):
        geometry=self.new('SUGeometryInputCreate')
        vertices=(Point*len(mesh['vertices']))(*[Point(*(c/2.54 for c in v)) for v in mesh['vertices']])
        self.call('SUGeometryInputSetVertices',geometry,len(vertices),vertices)
        for face in mesh['faces']:
            loop=self.new('SULoopInputCreate')
            for index in face:
                self.call('SULoopInputAddVertexIndex',loop,index)
            idx=S()
            self.call('SUGeometryInputAddFace',geometry,B(loop),B(idx))
        self.call('SUEntitiesFill',entities,geometry,True)
        self.call('SUGeometryInputRelease',B(geometry))

    def clean_coplanar_edges(self,entities):
        count=S(); self.call('SUEntitiesGetNumEdges',entities,False,B(count))
        edges=(R*count.value)()
        self.call('SUEntitiesGetEdges',entities,False,len(edges),edges,B(count))
        for edge in edges:
            n=S();self.call('SUEdgeGetNumFaces',edge,B(n))
            if n.value!=2: continue
            faces=(R*2)();self.call('SUEdgeGetFaces',edge,2,faces,B(n))
            normals=[]
            for f in faces:
                normal=Point();self.call('SUFaceGetNormal',f,B(normal))
                normals.append(np.array([normal.x,normal.y,normal.z]))
            if np.dot(*normals)>1-1e-8:
                self.call('SUDrawingElementSetHidden',self.dll.SUEdgeToDrawingElement(edge),True)

    def camera(self,camera,eye,target,up,height):
        self.call('SUCameraSetOrientation',camera,B(Point(*(v/2.54 for v in eye))),
                  B(Point(*(v/2.54 for v in target))),B(Point(*up)))
        self.call('SUCameraSetPerspective',camera,False)
        self.call('SUCameraSetOrthographicFrustumHeight',camera,height/2.54)

    def build(self,base,path,meshes,palette):
        model=R();self.call('SUModelCreateFromFile',B(model),str(base).encode('utf-8'))
        try:
            root=self.new('SUModelGetEntities',model)
            count=S();self.call('SUEntitiesGetNumGroups',root,B(count));assert count.value==16
            basegroups=(R*count.value)();self.call('SUEntitiesGetGroups',root,len(basegroups),basegroups,B(count))
            transformation=Transform((C.c_double*16)(1,0,0,0,0,1,0,0,0,0,1,0,150/2.54,600/2.54,0,1))
            for g in basegroups:
                self.call('SUGroupSetTransform',g,B(transformation))
                self.clean_coplanar_edges(self.new('SUGroupGetEntities',g))
            layers={}
            for name in sorted({m['layer'] for m in meshes}):
                layer=self.new('SULayerCreate');self.call('SULayerSetName',layer,name.encode())
                self.call('SUModelAddLayers',model,1,B(layer));layers[name]=layer
            materials={}
            for name,value in palette.items():
                material=self.new('SUMaterialCreate');self.call('SUMaterialSetName',material,name.encode())
                self.call('SUMaterialSetColor',material,B(Color(*value[:3],255)))
                if len(value)>3:
                    self.call('SUMaterialSetOpacity',material,value[3]);self.call('SUMaterialSetUseOpacity',material,True)
                self.call('SUModelAddMaterials',model,1,B(material));materials[name]=material
            for g in basegroups:
                self.call('SUDrawingElementSetMaterial',self.dll.SUGroupToDrawingElement(g),materials['Branco_quente'])
            assemblies={}
            for mesh in meshes:
                key=mesh['object']
                if key not in assemblies:
                    parent,entities=self.group(root,key)
                    self.call('SUDrawingElementSetLayer',self.dll.SUGroupToDrawingElement(parent),layers[mesh['layer']])
                    assemblies[key]=entities
                group,entities=self.group(assemblies[key],mesh['name'])
                element=self.dll.SUGroupToDrawingElement(group)
                self.call('SUDrawingElementSetMaterial',element,materials[mesh['material']])
                self.fill(entities,mesh)
            scenes=[
                ('01_Interiores_axonometria',(2050,-1800,3000),(525,1100,0),(0,0,1),2200,['COBERTURA','MUROS_PORTOES','GARAGEM_COBERTURA']),
                ('02_Planta_mobiliada',(525,1000,4000),(525,1000,0),(0,1,0),2250,['COBERTURA','GARAGEM_COBERTURA']),
                ('03_Fachada',(1500,-2600,1500),(525,1000,100),(0,0,1),1450,[]),
            ]
            for name,eye,target,up,height,hidden in scenes:
                scene=self.new('SUSceneCreate');self.call('SUSceneSetName',scene,name.encode())
                self.call('SUModelAddScenes',model,1,B(scene))
                camera=self.new('SUCameraCreate');self.camera(camera,eye,target,up,height)
                self.call('SUSceneSetCamera',scene,camera);self.call('SUCameraRelease',B(camera))
                self.call('SUSceneSetUseCamera',scene,True);self.call('SUSceneSetUseHiddenLayers',scene,True)
                for label in hidden:
                    self.call('SUSceneAddLayer',scene,layers[label])
            current=self.new('SUModelGetCamera',model)
            _,eye,target,up,height,hidden=scenes[0]
            self.camera(current,eye,target,up,height)
            for label in hidden:self.call('SULayerSetVisibility',layers[label],False)
            self.call('SUModelSaveToFileWithVersion',model,str(path).encode('utf-8'),9)
        finally:
            self.call('SUModelRelease',B(model))
        return self.inspect(path,len(assemblies)+16)

    def inspect(self,path,root_count):
        model=R();self.call('SUModelCreateFromFile',B(model),str(path).encode('utf-8'))
        totals=dict(groups=0,faces=0,edges=0,nonmanifold_edges=0)
        def walk(entities):
            n=S();self.call('SUEntitiesGetNumFaces',entities,B(n));totals['faces']+=n.value
            self.call('SUEntitiesGetNumEdges',entities,False,B(n));totals['edges']+=n.value
            edges=(R*n.value)();self.call('SUEntitiesGetEdges',entities,False,len(edges),edges,B(n))
            for edge in edges:
                count=S();self.call('SUEdgeGetNumFaces',edge,B(count))
                totals['nonmanifold_edges']+=int(count.value!=2)
            self.call('SUEntitiesGetNumGroups',entities,B(n));totals['groups']+=n.value
            if n.value:
                groups=(R*n.value)();self.call('SUEntitiesGetGroups',entities,len(groups),groups,B(n))
                for group in groups:walk(self.new('SUGroupGetEntities',group))
        try:
            root=self.new('SUModelGetEntities',model)
            n=S();self.call('SUEntitiesGetNumGroups',root,B(n));assert n.value==root_count
            groups=(R*n.value)();self.call('SUEntitiesGetGroups',root,len(groups),groups,B(n))
            bb=[];wall_groups=0;wall_faces=0
            for group in groups:
                transform=Transform();self.call('SUGroupGetTransform',group,B(transform))
                t=np.array(transform.values)
                if np.allclose(t[[12,13,14]],[150/2.54,600/2.54,0]):
                    wall_groups+=1
                    entities=self.new('SUGroupGetEntities',group)
                    nf=S();self.call('SUEntitiesGetNumFaces',entities,B(nf));wall_faces+=nf.value
                    assert np.allclose(t[:12],[1,0,0,0,0,1,0,0,0,0,1,0])
                bounds=Bounds();self.call('SUDrawingElementGetBoundingBox',self.dll.SUGroupToDrawingElement(group),B(bounds))
                bb.append([[getattr(p,axis)*2.54 for axis in ('x','y','z')] for p in (bounds.min,bounds.max)])
            assert wall_groups==16 and wall_faces==466,(wall_groups,wall_faces)
            totals.update(preserved_wall_groups=wall_groups,preserved_wall_faces=wall_faces)
            limits=[[min(b[0][i] for b in bb) for i in range(3)],[max(b[1][i] for b in bb) for i in range(3)]]
            assert np.allclose(limits,[[0,0,-15],[1050,2000,360]],atol=1e-5),limits
            self.call('SUEntitiesGetNumFaces',root,B(n));assert n.value==0
            self.call('SUEntitiesGetNumEdges',root,False,B(n));assert n.value==0
            walk(root)
            assert totals['nonmanifold_edges']==0,totals
            self.call('SUModelGetNumScenes',model,B(n));assert n.value==3;totals['scenes']=n.value
            self.call('SUModelGetNumLayers',model,B(n));totals['layers']=n.value
            self.call('SUModelGetNumMaterials',model,B(n));totals['materials']=n.value
            value=self.new('SUTypedValueCreate');self.call('SUOptionsProviderGetValue',self.units(model),b'LengthUnit',B(value))
            unit=C.c_int32();self.call('SUTypedValueGetInt32',value,B(unit));assert unit.value==3
            self.call('SUTypedValueRelease',B(value))
            return dict(totals,limits_cm=limits,unit='cm',reopen='PASS: SketchUpAPI 16.1.1449',GUI='NAO TESTADA')
        finally:self.call('SUModelRelease',B(model))
