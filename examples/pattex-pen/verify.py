"""Verify the example in FreeCAD. These are sampled geometric checks."""
from pathlib import Path
import json
import FreeCAD as App
import Part
import Mesh
from FreeCAD import Vector as V


def verify(fcstd_path, step_path, stl_path):
    native = Path(fcstd_path).resolve()
    existing = next(
        (d for d in App.listDocuments().values()
         if d.FileName and Path(d.FileName).resolve() == native), None
    )
    doc = existing or App.openDocument(str(native))
    try:
        doc.recompute()
        final = doc.getObject("PattexPressLift")
        if final is None:
            raise RuntimeError("Expected R5 final feature PattexPressLift")
        shape = final.Shape
        data = json.loads(Path(__file__).with_name("design.json").read_text(encoding="utf-8"))
        assumed = data["item_assumptions"]
        planpts = [(20.75+(x-20.75)*29/31, 63.75+(y-62.75)*118/121)
                   for x, y in assumed["plan_source_polygon_xy"]]
        planwire = Part.makePolygon([V(x,y,0) for x,y in planpts+[planpts[0]]])
        sidepts = assumed["side_polygon_yz"]
        sidewire = Part.makePolygon([V(0,y,z) for y,z in sidepts+[sidepts[0]]])
        item = Part.Face(planwire).extrude(V(0,0,60)).common(
            Part.Face(sidewire).extrude(V(41.5,0,0)))
        axis = V(20.75,46,18)
        motion = []
        for index in range(31):
            angle = index * 0.5
            pose = item.copy()
            pose.rotate(axis,V(1,0,0),angle)
            motion.append({"degrees":angle,"collision_mm3":shape.common(pose).Volume})
        tilted = item.copy()
        tilted.rotate(axis,V(1,0,0),15)
        extraction = []
        for index in range(11):
            pose = tilted.copy()
            pose.translate(V(0,1.5*index/10,index/10))
            extraction.append({"stage":"release","step":index,
                               "collision_mm3":shape.common(pose).Volume})
        for index in range(81):
            pose = tilted.copy()
            pose.translate(V(0,1.5,1+index*.5))
            extraction.append({"stage":"lift","step":index,
                               "collision_mm3":shape.common(pose).Volume})
        upper = Part.makeCompound([doc.getObject("Foot"+str(i)).Shape for i in (1,2,3)])
        upper.translate(V(0,0,42))

        def section(start, end):
            common = shape.common(Part.makeLine(V(*start),V(*end)))
            return [{"length":edge.Length,
                     "endpoints":[list(edge.Vertexes[0].Point),list(edge.Vertexes[-1].Point)]}
                    for edge in common.Edges]

        floor = section((20.75,41.75,-1),(20.75,41.75,50))
        ends = section((20.75,-1,30),(20.75,126.5,30))
        sides = section((-1,65,30),(42.5,65,30))
        step = Part.Shape()
        step.read(str(Path(step_path).resolve()))
        mesh = Mesh.Mesh(str(Path(stl_path).resolve()))

        def bounds(value):
            b = value.BoundBox
            return [b.XLength,b.YLength,b.ZLength]

        def near(actual, expected, tolerance=1e-5):
            return len(actual) == len(expected) and all(
                abs(a-b) < tolerance for a,b in zip(actual,expected))

        checks = {
            "valid_single_solid":shape.isValid() and len(shape.Solids)==1,
            "recompute":not any("Invalid" in obj.State for obj in doc.Objects),
            "bounds":near(bounds(shape),data["outer"]),
            "floor_section_3_25":near([s["length"] for s in floor],[3.25]),
            "end_wall_sections":near(sorted(s["length"] for s in ends),[1.5,2.25]),
            "side_wall_sections":near(sorted(s["length"] for s in sides),[5.25,5.25]),
            "stacking":shape.common(upper).Volume < 1e-7,
            "sampled_tilt":all(p["collision_mm3"] < 1e-7 for p in motion),
            "sampled_extraction":all(p["collision_mm3"] < 1e-7 for p in extraction),
            "step":step.isValid() and len(step.Solids)==1 and
                   near(bounds(step),data["outer"]) and abs(step.Volume-shape.Volume)<1e-5,
            "stl":mesh.isSolid() and mesh.countComponents()==1 and near(bounds(mesh),data["outer"])
        }
        report = {
            "revision":"R5","freecad_version":".".join(App.Version()[:3]),
            "checks":checks,"all_passed":all(checks.values()),
            "bounds_mm":bounds(shape),"volume_mm3":shape.Volume,
            "floor_section":floor,"end_wall_sections":ends,"side_wall_sections":sides,
            "motion_samples":motion,"extraction_samples":extraction,
            "scope":"Assumed item, finite pose samples; no physical test or continuous-sweep proof"
        }
        if not report["all_passed"]:
            raise RuntimeError("Failed checks: "+", ".join(k for k,v in checks.items() if not v))
        return report
    finally:
        if existing is None:
            App.closeDocument(doc.Name)
