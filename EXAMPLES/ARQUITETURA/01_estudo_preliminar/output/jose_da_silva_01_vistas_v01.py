"""Referencias geometricas com teste de profundidade, para orientar a geracao por IA."""
import numpy as np
from shapely.geometry import Polygon
from shapely.ops import triangulate
from PIL import Image

def render(meshes,palette,path,eye=(1600,-2600,1400),target=(525,1000,100),size=(1800,1200)):
    eye=np.array(eye,dtype=float);forward=np.array(target)-eye;forward/=np.linalg.norm(forward)
    right=np.cross(forward,[0,0,1]);right/=np.linalg.norm(right)
    up=np.cross(right,forward)
    rotation=np.array([right,up,forward]).T
    allpts=np.concatenate([np.array(m['vertices']) for m in meshes])
    proj=(allpts-eye)@rotation
    minimum=proj[:,:2].min(axis=0);maximum=proj[:,:2].max(axis=0)
    width,height=size;scale=min((width-100)/(maximum[0]-minimum[0]),(height-100)/(maximum[1]-minimum[1]))
    origin=(minimum+maximum)/2
    pixels=np.full((height,width,3),247,dtype=np.uint8)
    depth=np.full((height,width),np.inf)
    light=np.array([-0.5,-0.6,1.0]);light/=np.linalg.norm(light)
    for mesh in meshes:
        points=np.array(mesh['vertices'],dtype=float)
        base=np.array(palette[mesh['material']][:3],dtype=float)
        for face in mesh['faces']:
            pts=points[face]
            normal=np.cross(pts[1]-pts[0],pts[2]-pts[0]);length=np.linalg.norm(normal)
            if length<1e-10:continue
            normal/=length
            color=np.clip(base*(.67+.33*abs(np.dot(normal,light))),0,255).astype(np.uint8)
            if len(face)<=4:
                triangles=[pts[[0,i,i+1]] for i in range(1,len(face)-1)]
            else:
                drop=int(np.argmax(np.abs(normal)));keep=[i for i in range(3) if i!=drop]
                poly=Polygon(pts[:,keep]);triangles=[]
                for triangle in triangulate(poly):
                    if not poly.covers(triangle.representative_point()):continue
                    tri=[]
                    for p in list(triangle.exterior.coords)[:3]:
                        item=np.zeros(3);item[keep]=p
                        item[drop]=pts[0,drop]-sum(normal[i]*(item[i]-pts[0,i]) for i in keep)/normal[drop]
                        tri.append(item)
                    triangles.append(np.array(tri))
            for tri in triangles:
                p=(tri-eye)@rotation
                screen=np.column_stack(((p[:,0]-origin[0])*scale+width/2,
                                        height/2-(p[:,1]-origin[1])*scale))
                xmin=max(0,int(np.floor(screen[:,0].min())));xmax=min(width-1,int(np.ceil(screen[:,0].max())))
                ymin=max(0,int(np.floor(screen[:,1].min())));ymax=min(height-1,int(np.ceil(screen[:,1].max())))
                if xmin>xmax or ymin>ymax:continue
                x0,y0=screen[0];x1,y1=screen[1];x2,y2=screen[2]
                denominator=(y1-y2)*(x0-x2)+(x2-x1)*(y0-y2)
                if abs(denominator)<1e-8:continue
                yy,xx=np.mgrid[ymin:ymax+1,xmin:xmax+1];xx=xx+.5;yy=yy+.5
                a=((y1-y2)*(xx-x2)+(x2-x1)*(yy-y2))/denominator
                b=((y2-y0)*(xx-x2)+(x0-x2)*(yy-y2))/denominator;c=1-a-b
                z=a*p[0,2]+b*p[1,2]+c*p[2,2]
                region=depth[ymin:ymax+1,xmin:xmax+1]
                mask=(a>=-1e-6)&(b>=-1e-6)&(c>=-1e-6)&(z<region)
                region[mask]=z[mask]
                pixels[ymin:ymax+1,xmin:xmax+1][mask]=color
    Image.fromarray(pixels).save(path)
