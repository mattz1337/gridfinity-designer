# Verification evidence

`original-r5.json` records checks executed during the original design session. Its numbers concern the approved assumed pen, not a scanned or physically measured item.

`publication-check.json` records the repeat check of the public model files and the portable generator. Neither report is a physical test.

The published native model preserves the original feature geometry. Only native license metadata and STEP header metadata were normalized for distribution. Package checks reject local user paths and inspect the native ZIP's text entries.

## Limits

- Tilt checking uses 31 discrete poses, not a continuous sweep.
- Extraction checking uses 11 release samples and 81 lift samples.
- Tangential pivot/rest contact is intentional. Zero overlapping volume does not establish a tolerance margin.
- Wall/floor evidence uses specified sections; no exhaustive global thickness solver was run.
- Virtual stacking is against the generated reference feet, not the user's physical plate.
- The 0.15 mm cap-side throat gap is tight and depends on the assumed item.
- No physical print, grip, center-of-mass, rolling/sliding, load or adhesion test is recorded.

Read [the case study](../README.md) before treating the example as a ready-made fit for another pen.
