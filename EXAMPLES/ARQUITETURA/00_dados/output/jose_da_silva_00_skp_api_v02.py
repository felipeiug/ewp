"""Gravacao e auditoria com a biblioteca instalada do SketchUp 2016 (cm -> inch)."""
import ctypes as C
import os
from pathlib import Path


class Ref(C.Structure):
    _fields_ = [('ptr', C.c_void_p)]


class Point(C.Structure):
    _fields_ = [('x', C.c_double), ('y', C.c_double), ('z', C.c_double)]


class Bounds(C.Structure):
    _fields_ = [('min', Point), ('max', Point)]


class Color(C.Structure):
    _fields_ = [('red', C.c_ubyte), ('green', C.c_ubyte),
                ('blue', C.c_ubyte), ('alpha', C.c_ubyte)]


P = C.POINTER
R = Ref
S = C.c_size_t
B = C.byref


class API:
    def __init__(self):
        folder = Path('C:/Program Files/SketchUp/SketchUp 2016')
        self.dll_folder = os.add_dll_directory(str(folder))
        self.dll = C.CDLL(str(folder / 'SketchUpAPI.dll'))
        specs = {
            'SUInitialize': (None, []), 'SUTerminate': (None, []),
            'SUModelCreate': (C.c_int, [P(R)]),
            'SUModelRelease': (C.c_int, [P(R)]),
            'SUModelCreateFromFile': (C.c_int, [P(R), C.c_char_p]),
            'SUModelSaveToFileWithVersion': (C.c_int, [R, C.c_char_p, C.c_int]),
            'SUModelGetEntities': (C.c_int, [R, P(R)]),
            'SUGroupCreate': (C.c_int, [P(R)]),
            'SUGroupSetName': (C.c_int, [R, C.c_char_p]),
            'SUGroupGetEntities': (C.c_int, [R, P(R)]),
            'SUGroupToDrawingElement': (R, [R]),
            'SUEntitiesAddGroup': (C.c_int, [R, R]),
            'SUEntitiesGetNumGroups': (C.c_int, [R, P(S)]),
            'SUEntitiesGetGroups': (C.c_int, [R, S, P(R), P(S)]),
            'SUEntitiesGetNumFaces': (C.c_int, [R, P(S)]),
            'SUEntitiesGetNumEdges': (C.c_int, [R, C.c_bool, P(S)]),
            'SUEntitiesGetEdges': (C.c_int, [R, C.c_bool, S, P(R), P(S)]),
            'SUEdgeGetNumFaces': (C.c_int, [R, P(S)]),
            'SUDrawingElementGetBoundingBox': (C.c_int, [R, P(Bounds)]),
            'SUGeometryInputCreate': (C.c_int, [P(R)]),
            'SUGeometryInputRelease': (C.c_int, [P(R)]),
            'SUGeometryInputSetVertices': (C.c_int, [R, S, P(Point)]),
            'SULoopInputCreate': (C.c_int, [P(R)]),
            'SULoopInputAddVertexIndex': (C.c_int, [R, S]),
            'SUGeometryInputAddFace': (C.c_int, [R, P(R), P(S)]),
            'SUEntitiesFill': (C.c_int, [R, R, C.c_bool]),
            'SULayerCreate': (C.c_int, [P(R)]),
            'SULayerSetName': (C.c_int, [R, C.c_char_p]),
            'SUModelAddLayers': (C.c_int, [R, S, P(R)]),
            'SUDrawingElementSetLayer': (C.c_int, [R, R]),
            'SUMaterialCreate': (C.c_int, [P(R)]),
            'SUMaterialSetName': (C.c_int, [R, C.c_char_p]),
            'SUMaterialSetColor': (C.c_int, [R, P(Color)]),
            'SUModelAddMaterials': (C.c_int, [R, S, P(R)]),
            'SUDrawingElementSetMaterial': (C.c_int, [R, R]),
            'SUModelGetOptionsManager': (C.c_int, [R, P(R)]),
            'SUOptionsManagerGetOptionsProviderByName': (C.c_int, [R, C.c_char_p, P(R)]),
            'SUTypedValueCreate': (C.c_int, [P(R)]),
            'SUTypedValueRelease': (C.c_int, [P(R)]),
            'SUTypedValueSetInt32': (C.c_int, [R, C.c_int32]),
            'SUTypedValueGetInt32': (C.c_int, [R, P(C.c_int32)]),
            'SUOptionsProviderSetValue': (C.c_int, [R, C.c_char_p, R]),
            'SUOptionsProviderGetValue': (C.c_int, [R, C.c_char_p, P(R)]),
            'SUModelGetCamera': (C.c_int, [R, P(R)]),
            'SUCameraSetOrientation': (C.c_int, [R, P(Point), P(Point), P(Point)]),
            'SUCameraSetPerspective': (C.c_int, [R, C.c_bool]),
            'SUCameraSetOrthographicFrustumHeight': (C.c_int, [R, C.c_double]),
        }
        for name, (restype, argtypes) in specs.items():
            fn = getattr(self.dll, name)
            fn.restype, fn.argtypes = restype, argtypes
        self.dll.SUInitialize()

    def call(self, name, *args):
        result = getattr(self.dll, name)(*args)
        if result != 0:
            raise RuntimeError(f'{name}: SUResult={result}')

    def new(self, name, *args):
        ref = R()
        self.call(name, *args, B(ref))
        return ref

    def units(self, model):
        manager = self.new('SUModelGetOptionsManager', model)
        return self.new('SUOptionsManagerGetOptionsProviderByName', manager, b'UnitsOptions')

    def create(self, path, meshes):
        model = self.new('SUModelCreate')
        try:
            root = self.new('SUModelGetEntities', model)
            provider = self.units(model)
            value = self.new('SUTypedValueCreate')
            for key, number in [('LengthFormat', 0), ('LengthUnit', 3), ('LengthPrecision', 1)]:
                self.call('SUTypedValueSetInt32', value, number)
                self.call('SUOptionsProviderSetValue', provider, key.encode(), value)
            self.call('SUTypedValueRelease', B(value))
            layers, materials = {}, {}
            for label, rgb in [('PAREDES_EXTERNAS', (221, 218, 208)),
                               ('PAREDES_INTERNAS', (238, 234, 220))]:
                layer = self.new('SULayerCreate')
                self.call('SULayerSetName', layer, label.encode())
                self.call('SUModelAddLayers', model, 1, B(layer))
                layers[label] = layer
                material = self.new('SUMaterialCreate')
                self.call('SUMaterialSetName', material, ('Alvenaria_' + label).encode())
                self.call('SUMaterialSetColor', material, B(Color(*rgb, 255)))
                self.call('SUModelAddMaterials', model, 1, B(material))
                materials[label] = material
            for mesh in meshes:
                group = self.new('SUGroupCreate')
                self.call('SUGroupSetName', group, mesh['name'].encode())
                self.call('SUEntitiesAddGroup', root, group)
                element = self.dll.SUGroupToDrawingElement(group)
                self.call('SUDrawingElementSetLayer', element, layers[mesh['layer']])
                self.call('SUDrawingElementSetMaterial', element, materials[mesh['layer']])
                entities = self.new('SUGroupGetEntities', group)
                geometry = self.new('SUGeometryInputCreate')
                vertices = (Point * len(mesh['vertices']))(*[
                    Point(*(coordinate / 2.54 for coordinate in vertex))
                    for vertex in mesh['vertices']])
                self.call('SUGeometryInputSetVertices', geometry, len(vertices), vertices)
                for face in mesh['faces']:
                    loop = self.new('SULoopInputCreate')
                    for index in face:
                        self.call('SULoopInputAddVertexIndex', loop, index)
                    face_index = S()
                    self.call('SUGeometryInputAddFace', geometry, B(loop), B(face_index))
                self.call('SUEntitiesFill', entities, geometry, True)
                self.call('SUGeometryInputRelease', B(geometry))
            camera = self.new('SUModelGetCamera', model)
            position = Point(1750/2.54, -1600/2.54, 2400/2.54)
            target = Point(375/2.54, 575/2.54, 100/2.54)
            self.call('SUCameraSetOrientation', camera, B(position), B(target), B(Point(0, 0, 1)))
            self.call('SUCameraSetPerspective', camera, False)
            self.call('SUCameraSetOrthographicFrustumHeight', camera, 1550/2.54)
            # SU2016 is enumerator 9; library itself is version 16.1.1449.
            self.call('SUModelSaveToFileWithVersion', model, str(path).encode('utf-8'), 9)
        finally:
            self.call('SUModelRelease', B(model))
        return self.audit(path, meshes)

    def audit(self, path, meshes):
        model = R()
        self.call('SUModelCreateFromFile', B(model), str(path).encode('utf-8'))
        try:
            root = self.new('SUModelGetEntities', model)
            count = S()
            self.call('SUEntitiesGetNumFaces', root, B(count))
            assert count.value == 0, 'Faces soltas na raiz'
            self.call('SUEntitiesGetNumEdges', root, False, B(count))
            assert count.value == 0, 'Arestas soltas na raiz'
            self.call('SUEntitiesGetNumGroups', root, B(count))
            assert count.value == len(meshes)
            groups = (R * count.value)()
            self.call('SUEntitiesGetGroups', root, len(groups), groups, B(count))
            bounds = []
            totals = {'grupos': count.value, 'faces': 0, 'arestas': 0, 'arestas_nao_manifold': 0}
            for group in groups:
                entities = self.new('SUGroupGetEntities', group)
                self.call('SUEntitiesGetNumFaces', entities, B(count))
                totals['faces'] += count.value
                self.call('SUEntitiesGetNumEdges', entities, False, B(count))
                edges = (R * count.value)()
                self.call('SUEntitiesGetEdges', entities, False, len(edges), edges, B(count))
                totals['arestas'] += count.value
                for edge in edges:
                    incidence = S()
                    self.call('SUEdgeGetNumFaces', edge, B(incidence))
                    totals['arestas_nao_manifold'] += int(incidence.value != 2)
                bb = Bounds()
                self.call('SUDrawingElementGetBoundingBox', self.dll.SUGroupToDrawingElement(group), B(bb))
                bounds.append([[getattr(p, axis)*2.54 for axis in ('x','y','z')] for p in (bb.min, bb.max)])
            minimum = [min(bb[0][i] for bb in bounds) for i in range(3)]
            maximum = [max(bb[1][i] for bb in bounds) for i in range(3)]
            assert all(abs(a-b) < 1e-6 for a,b in zip(minimum+maximum, [0,0,0,750,1150,300]))
            assert totals['arestas_nao_manifold'] == 0, totals
            value = self.new('SUTypedValueCreate')
            self.call('SUOptionsProviderGetValue', self.units(model), b'LengthUnit', B(value))
            unit = C.c_int32()
            self.call('SUTypedValueGetInt32', value, B(unit))
            self.call('SUTypedValueRelease', B(value))
            assert unit.value == 3
            return dict(totals, unidade='cm', limites_cm=[minimum,maximum],
                        reabertura='PASS: SketchUpAPI 16.1.1449', interface_grafica='NAO TESTADA')
        finally:
            self.call('SUModelRelease', B(model))

    def close(self):
        self.dll.SUTerminate()
