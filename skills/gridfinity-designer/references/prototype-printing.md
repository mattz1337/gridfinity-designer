# Material-saving prototypes

Read when the user asks about test-print cost, slicer settings or fit coupons.

Start with what must be tested: pocket clearance, Gridfinity interface, lip/stacking, grip, or full rocking motion. A small contour coupon can test local clearance; it cannot validate a full extraction mechanism or center-of-mass balance. Preserve full scale. Cropping the model can remove exactly the floor, fulcrum or rim being tested.

For a low-load PLA fit prototype with an assumed 0.4 mm nozzle, the following is a **starting proposal**, not a tested profile:
- 0.20 mm layer height.
- 2 wall loops.
- 5% sparse infill, e.g. gyroid.
- 3 top and 3 bottom layers at that height (0.6 mm).
- No supports only if inspection shows the actual geometry is support-free in the selected orientation.
- No brim only when adhesion is reliable.

Adapt to nozzle, material, bridges and load. Thin supported geometry may already be all perimeters; reducing infill then has little effect. Extremely sparse infill may produce poor top surfaces. Inspect sliced layers at cavity floors and support tops.

In slicers with both shell-layer count and minimum shell thickness, adjust both: a larger thickness can override a reduced layer count. Keep necessary closed surfaces; zero infill and vase mode are poor defaults for a fitted pocket with raised supports.

Higher layer height mainly saves printing time; it does not inherently remove much material. Fewer walls, solid layers and lower infill can save material, but compare slicer-estimated grams before and after. Do not invent savings or claim a printer-specific profile was tested.

Use the current slicer's primary documentation when naming settings or describing behavior. The example used Bambu Studio terminology, but that does not make Bambu Studio or a P2S mandatory for the skill.

After printing, ask for the observed failure (too tight where, rocks at rest, insufficient lift, catches lip, layer failure) and change the relevant geometry or setting. Keep geometric, slicer and physical evidence distinct.
