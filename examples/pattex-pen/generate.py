"""Reproduce the approved R5 prototype in a FreeCAD Python environment.

Call generate(output_directory). Each call creates a unique run directory.
Profiles are script-generated; this is not a general parametric bin library.
"""
from pathlib import Path
import tempfile
import math
import FreeCAD as App
import Part
import MeshPart
from FreeCAD import Vector as V


def generate(output_directory):
    output_directory = Path(output_directory).expanduser().resolve()
    output_directory.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix="pattex-r5-", dir=str(output_directory)))
    doc=App.newDocument('Pattex_1x3_6U_PressLift')
    def rr(w,h,r,z,cx=20.75,cy=62.75):
        x=cx-w/2; y=cy-h/2; k=math.sqrt(.5)
        edges=[]
        def line(a,b): edges.append(Part.makeLine(V(*a,z),V(*b,z)))
        def arc(a,m,b): edges.append(Part.Arc(V(*a,z),V(*m,z),V(*b,z)).toShape())
        line((x+r,y),(x+w-r,y))
        arc((x+w-r,y),(x+w-r+r*k,y+r-r*k),(x+w,y+r))
        line((x+w,y+r),(x+w,y+h-r))
        arc((x+w,y+h-r),(x+w-r+r*k,y+h-r+r*k),(x+w-r,y+h))
        line((x+w-r,y+h),(x+r,y+h))
        arc((x+r,y+h),(x+r-r*k,y+h-r+r*k),(x,y+h-r))
        line((x,y+h-r),(x,y+r))
        arc((x,y+r),(x+r-r*k,y+r-r*k),(x+r,y))
        return Part.Wire(edges)
    def obj(name,shape):
        o=doc.addObject('PartDesign::Feature',name);o.Shape=shape;return o
    feet=[]
    for i,cy in enumerate([20.75,62.75,104.75]):
        profiles=[rr(35.6,35.6,.8,0,cy=cy),rr(37.2,37.2,1.6,.8,cy=cy),rr(37.2,37.2,1.6,2.6,cy=cy),rr(41.5,41.5,3.75,4.75,cy=cy)]
        feet.append(obj('Foot'+str(i+1),Part.makeLoft(profiles,True,True)))
    body=obj('BodyTo6U',Part.Face(rr(41.5,125.5,3.75,4.75)).extrude(V(0,0,37.25)))
    lipouter=Part.Face(rr(41.5,125.5,3.75,42)).extrude(V(0,0,4.4))
    inner=Part.makeLoft([rr(36.3,120.3,1.15,42),rr(37.7,121.7,1.85,42.7),rr(37.7,121.7,1.85,44.5),rr(41.5,125.5,3.75,46.4)],True,True)
    lip=obj('StackingLip',lipouter.cut(inner))
    blank=doc.addObject('Part::MultiFuse','Blank');blank.Shapes=feet+[body,lip]
    cavitypts=[(5.25,1.5),(36.25,1.5),(36.25,101.5),(31.25,105.5),(31.25,123.25),(10.25,123.25),(10.25,105.5),(5.25,101.5)]
    cw=Part.makePolygon([V(x,y,8) for x,y in cavitypts+[cavitypts[0]]])
    cavity=obj('DeepPocketTool',Part.Face(cw).extrude(V(0,0,34)))
    shell=doc.addObject('Part::Cut','ContinuousWallShell');shell.Base=blank;shell.Tool=cavity;shell.Refine=True
    pivot=doc.addObject('Part::Cylinder','RoundedPivot');pivot.Radius=2;pivot.Height=31;pivot.Placement=App.Placement(V(5.25,46,18),App.Rotation(V(0,0,1),V(1,0,0)))
    stem=doc.addObject('Part::Box','PivotPedestal');stem.Length=31;stem.Width=4;stem.Height=10;stem.Placement.Base=V(5.25,44,8)
    rest=doc.addObject('Part::Box','CapRest');rest.Length=13;rest.Width=8;rest.Height=15;rest.Placement.Base=V(14.25,111,8)
    final=doc.addObject('Part::MultiFuse','PattexPressLift');final.Shapes=[shell,pivot,stem,rest];final.Refine=True
    final.addProperty('App::PropertyString','DesignRevision');final.DesignRevision='R5 approved press-to-lift prototype'
    final.addProperty('App::PropertyString','ModelNote');final.ModelNote='Script-generated profiles, dependent booleans, editable support primitives'
    doc.recompute()
    doc.License='MIT'
    doc.LicenseURL='https://opensource.org/license/mit'
    doc.CreatedBy=''
    doc.LastModifiedBy=''
    shape=final.Shape
    if not shape.isValid() or len(shape.Solids) != 1:
        raise RuntimeError('Expected one valid organizer solid')
    if App.GuiUp:
        import FreeCADGui as Gui
        for feature in doc.Objects:
            feature.ViewObject.Visibility=False
        final.ViewObject.Visibility=True
        final.ViewObject.ShapeColor=(.20,.65,.60)
        Gui.activeDocument().activeView().viewAxonometric()
        Gui.activeDocument().activeView().fitAll()
    paths={ext: str(out / ('press-lift.'+ext)) for ext in ('FCStd','step','stl')}
    doc.recompute()
    doc.saveAs(paths['FCStd'])
    Part.export([final],paths['step'])
    MeshPart.meshFromShape(Shape=shape,LinearDeflection=.05,AngularDeflection=.15,Relative=False).write(paths['stl'])
    if App.GuiUp:
        Gui.activeDocument().activeView().saveImage(str(out / 'preview.png'),1200,900,'White')
    return {'directory':str(out),'fcstd':paths['FCStd'],'step':paths['step'],'stl':paths['stl']}
