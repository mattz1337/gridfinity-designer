# FreeCAD generation and verification

## Connection and document ownership

Discover the actual MCP operations. A read-only document list or status operation establishes connectivity; finding a tool name alone does not. Confirm that the server can access the selected output location; a remote FreeCAD server may not share the client's filesystem.

Create a new document per final variation or copy task-owned geometry. Do not modify unrelated open documents. Keep asynchronous pure geometry work separate from GUI/document mutations according to the server's actual threading contract. Do not assume different MCP implementations offer the same helpers.

## Model and reproducibility

Prefer constrained sketches, editable features and expressions when practical. With script-generated profiles, retain a small reproducible generator and state which dimensions require regeneration. Use named bodies/features for base feet, cavity, lip and supports.

For a shared generator:
- Accept an output directory; do not embed a personal drive, username or task path.
- Create a unique run directory or refuse overwrites.
- Import required modules explicitly and work in a new document.
- Support the documented GUI/headless mode, rather than referencing an implicit GUI global.
- Export only the final model; name any optional item surrogate as an illustration.
- Record interface assumptions and test scope alongside the model.

Do not add custom user-home writes or environment changes merely to make a script convenient.

## Geometric evidence

Recompute and inspect feature states, validity, expected final solid count and bounds. Measure critical cavities, contact positions and remaining material from the finished shape. A few sections substantiate those sections; do not call a general global minimum measured unless the check covers the relevant geometry.

For base/floor interactions, include inter-foot gaps and hardware cavities. For stacking, inspect the lip profile and simulate mating feet where feasible. Reference compatibility and fitting the user's physical baseplate remain separate claims.

For motion, use the access reference and separate intentional contact from interference. Keep construction and surrogate bodies out of final counts.

## Export and delivery

Save native FreeCAD, requested STEP/STL, a useful model view and the current report. Reimport STEP when feasible; check solid count, bounds and volume. Check STL closure/components and numerical bounds; STL itself does not reliably encode a length unit.

Inspect images, not just file creation. Use side/section or illustrative motion views if an isometric exterior hides the mechanism. Keep a dimensioned schematic separate from a photorealistic image: only the former specifies geometry.

Before publishing requested examples, inspect text, STEP headers and native-document metadata for local paths or personal details. Keep user source photographs out of a public package unless their inclusion is authorized; useful model views and dimensioned graphics often suffice. Preserve geometry when neutralizing metadata, and recheck the resulting artifacts.

The report should state: actual revision, files produced, model editability, measured checks, failed/unavailable operations and physical tests actually performed. Do not copy a superseded "pending review" statement into the final deliverable as though it were current.
