"""Check the public package with Python 3; no third-party dependencies."""
from pathlib import Path
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


skill = ROOT / "skills" / "gridfinity-designer"
skill_text = (skill / "SKILL.md").read_text(encoding="utf-8")
check(skill_text.startswith("---\nname: gridfinity-designer\n"), "Invalid skill name/frontmatter")
check("\ndescription: " in skill_text.split("---",2)[1], "Missing skill description")
check("$gridfinity-designer" in (skill / "agents" / "openai.yaml").read_text(), "Missing invocation prompt")

local_path = re.compile(r"(?i)(?:[a-z]:[\\/](?:users|documents)[\\/]|/home/[^/\s]+/|/Users/[^/\s]+/)")
secret = re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,})")
text_extensions = {".md",".py",".yaml",".yml",".json",".svg",".step"}
count = 0
for path in ROOT.rglob("*"):
    if not path.is_file() or any(part in {".git","__pycache__","build",".generated"} for part in path.relative_to(ROOT).parts):
        continue
    relative = str(path.relative_to(ROOT))
    count += 1
    check(path.stat().st_size > 0, "Empty file: "+relative)
    if path.suffix.lower() in text_extensions:
        text = path.read_text(encoding="utf-8-sig")
        # This checker necessarily contains the detection patterns themselves.
        if path != Path(__file__).resolve():
            check(not local_path.search(text), "Personal filesystem path: "+relative)
            check(not secret.search(text), "Credential-like content: "+relative)
        if path.suffix == ".py":
            try:
                compile(text,relative,"exec")
            except SyntaxError as exc:
                errors.append("Python syntax: "+str(exc))
        if path.suffix == ".md":
            prose = re.sub(r"(?ms)^```[^\n]*\n.*?^```\s*$", "", text)
            for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)",prose):
                target = target.strip("<>").split("#",1)[0]
                if not target or re.match(r"^[a-z]+:",target):
                    continue
                target = target.split(" ",1)[0]
                check((path.parent / target).exists(),f"Broken link in {relative}: {target}")
        if path.suffix == ".svg":
            try:
                ET.fromstring(text)
            except ET.ParseError as exc:
                errors.append("SVG XML: "+str(exc))
    if path.suffix == ".png":
        raw = path.read_bytes()
        check(raw[:8] == b"\x89PNG\r\n\x1a\n","Bad PNG: "+relative)
        if raw[:8] == b"\x89PNG\r\n\x1a\n":
            w,h = struct.unpack(">II",raw[16:24])
            check(w >= 200 and h >= 100,"Unexpectedly small preview: "+relative)
    if path.suffix.lower() == ".fcstd":
        with zipfile.ZipFile(path) as archive:
            check("Document.xml" in archive.namelist(),"Missing FreeCAD XML")
            check("GuiDocument.xml" in archive.namelist(),"Missing FreeCAD GUI data")
            check(any(n.endswith(".brp") for n in archive.namelist()),"Missing BREP geometry")
            doc = ET.fromstring(archive.read("Document.xml"))
            license_value = doc.find("./Properties/Property[@name='License']/String")
            check(license_value is not None and license_value.get("value")=="MIT","Native license mismatch")
            for name in archive.namelist():
                if name.endswith((".xml",".txt")):
                    content = archive.read(name).decode("utf-8",errors="replace")
                    check(not local_path.search(content),"Personal path in native document: "+name)

evidence = json.loads((ROOT/"examples/pattex-pen/verification/original-r5.json").read_text())
check(evidence["shape_valid"] and evidence["solid_count"]==1,"Original CAD validity")
check(len(evidence["motion_samples"])==31,"Expected 31 original tilt samples")
check(len(evidence["extraction_samples"])==92,"Expected 92 original extraction samples")
check(all(p["collision_mm3"] < 1e-7 for p in evidence["motion_samples"]+evidence["extraction_samples"]),
      "Original motion interference")
check(evidence["stl"]["closed"] and evidence["stl"]["components"]==1,"Original STL topology")
publication = ROOT/"examples/pattex-pen/verification/publication-check.json"
check(publication.exists(),"Missing public artifact recheck")
if publication.exists():
    repeat = json.loads(publication.read_text())
    check(repeat["public_models"]["all_passed"],"Public model verification failed")
    check(repeat["regenerated_models"]["all_passed"],"Portable generator verification failed")
    check(repeat["geometry_preserved"],"Published native geometry differs from original")

if errors:
    print("\n".join("FAIL: "+e for e in errors))
    sys.exit(1)
print(f"PASS: {count} files; skill metadata, links, Python syntax, graphics, native metadata and evidence.")
