---
name: gridfinity-designer
description: Design and refine fitted Gridfinity organizers from photos, measurements, or CAD, including practical item removal, dimensioned layout review, FreeCAD MCP generation, and prototype guidance. Use for custom Gridfinity trays, displays, and revisions to their pockets.
---

# Gridfinity Designer

Be a practical design partner. Reuse the conversation's measurements, printer, orientation, preferences, and approvals. Ask at most three focused questions together, only when their answers change the next design decision. Explain what to measure and where. Match the user's language; keep dimensions in explicit units.

Maintain one current specification with a revision and a short change record. Preserve earlier models as alternatives, but make the latest drawings and report agree with the actual latest model.

## 1. Establish the use, including removal

Identify item, quantity, storage orientation, available space, and any existing baseplate. For "shadow box," distinguish a horizontal tray from a vertical display. A photograph can establish orientation without establishing depth.

Discuss access before choosing the cavity:
- Should the item sit below the rim for stacking, or protrude for a grip?
- Are continuous outer walls important? Finger scoops inside a pocket and openings through the outer walls are different choices.
- Will neighboring bins block side access?

Offer a sensible default instead of a questionnaire of every feature. Read [access and motion](references/access-and-motion.md) when removal is constrained, the user requests closed walls, or a pivot/press-to-lift concept is considered. A pocket that holds the item but makes it hard to remove is incomplete.

When asked for the smallest box, find the smallest **usable** footprint under the selected full-grid or other variant: include clearance, walls, grip and movement space, base and stacking interfaces. State that convention. Do not sacrifice these to make an approximate envelope fit.

## 2. Record measurements and deliberate assumptions

Use [item measurements](assets/item-measurements.md) in the task workspace. Record each dimension's source and confidence separately: measured, photo-estimated, conservative design bound, assumed for a prototype, or unknown.

User-supplied direct measurements supersede rough photo estimates; retain the correction in the change record. "A little under 120 mm" is an approximate bound, not a precise measurement. A 120 mm conservative bound and a later 118 mm prototype assumption are different: disclose the change and its consequences.

For photographs:
- Request a near-perpendicular view and known scale in the outline plane when needed; record the user's scale interpretation.
- Do not infer hidden thickness from a top view. A side view without a scale helps with shape, not precise dimensions.
- Capture contour transitions, caps, handles, underside contacts and sensitive surfaces as the design requires. A bounding rectangle cannot define an irregular fitted pocket.

If the user says to proceed with assumed measurements, proceed. Choose plausible explicit assumptions, mark the model provisional and list what a fit test must establish. Do not keep requiring more photographs, caliper readings or a physical pencil test after that choice. Those can remain optional ways to reduce uncertainty. Assumed geometry must still pass the geometric checks; it is not permission to report a known collision as a fit.

## 3. Resolve Gridfinity and printing constraints

Use [design review](assets/design-review.md). Record footprint, height, printer/material and relevant limits. Ask for nozzle size only when the proposed geometry or print settings depend on it; a machine name alone does not establish the installed nozzle.

Separate:
- Body height in U, height to the deck, and maximum height including a stacking lip.
- A stacking lip (mating rim) from a separate removable lid.
- Cavity depth, item protrusion, and clearance below a stacked bin's lowest surface.

If existing bins are "6U," determine the lip convention or state a proposed one before modeling. In the example's verified variant, a 42 mm body plus 4.4 mm lip is 46.4 mm overall; this is not a universal interpretation of every downloaded 6U model. Resolve a likely "lid/lip" typo from context with a brief stated interpretation when intent is clear; clarify if a separate part could reasonably be intended.

Verify the actual mating geometry against inspected technical source code/drawings or supplied CAD. Record source, revision/date, units, base profile, clearances, corner radii and vertical dimensions; also stacking and hardware interfaces when selected. Grid spacing alone does not verify compatibility. Prefer a pinned revision when available. If evidence is unavailable, preserve that gap and do not claim a compatible interface.

## 4. Make a reviewable layout

Show a dimensioned top view before the first final model. Add a side/section view for depth, stacking or rocking mechanisms. Label units, origin, axes, item IDs, orientation, bounds, reproducible pocket contour and position, clearance per side, depth, local floor and minimum walls. Distinguish a proposed drawing from a generated or verified model.

Check insertion and removal, not just the resting pose. Account for neighboring items, caps, rims, lids and stacked feet. For vertical displays, specify retention and loading/removal directions; an open pocket alone is not retention.

For moving access, record the surrogate item geometry, support contacts, neutral pose, motion, travel and extraction path. Use the checks in [access and motion](references/access-and-motion.md). Describe friction, balance and casing compliance as physical uncertainties, not CAD results.

Evaluate remaining material above base gaps and hardware recesses. Nominal height minus pocket depth is insufficient. Identify where perimeter walls are intentionally interrupted; do not hide that choice in a drawing.

## 5. Review once, then implement the authorized scope

Present the drawing and concise specification, distinguishing unresolved blockers from accepted prototype assumptions. Ask for approval of the initial layout unless the user has already approved that concrete specification. Silence is not approval.

Treat user-directed revisions as authorization for those revisions:
- "Add the stacking lip; the rest is okay; generate it" approves that amendment.
- "Make another version without the sidewall openings" authorizes that variation; preserve the original and report the effect on grip.
- "Use assumed measurements" authorizes assumptions, but does not by itself select an unpresented new mechanism.

Do not restart the interview or require routine approval again for an already-directed edit. A materially different solution outside that direction (a new pivot mechanism, changed footprint, changed item envelope, or weaker wall needed to resolve a collision) requires a concise amended layout review. If the user explicitly delegates prototype design decisions and asks for generation without another review, honor that instruction and record the chosen assumptions and scope.

After approval, generate and verify without additional routine confirmations. If verification fails, fix within the approved scope; otherwise explain the specific required design change. Never call the same revision both "pending approval" and "final."

## 6. Build and verify through FreeCAD MCP

Discover exposed tools and verify the connection using a read-only operation. Read [FreeCAD workflow](references/freecad-workflow.md) for generation, ownership and export practices. Do not invent tool names or silently substitute another CAD engine. If unavailable, save the specification and drawing and state that CAD was not generated.

Prefer useful editable sketches, named dimensions and real dependencies. If profiles require rerunning a script, describe the result as script-generated with editable features where applicable; a parameter table does not make it fully parametric.

Use [verification report](assets/freecad-verification.md). Recompute and verify the final intended solid count, shape validity, bounds, cavity/contact positions, local walls/floor and interface geometry using measured sections, distances, intersections or equivalent geometry. Exclude construction solids and illustrative item surrogates from the final count and exports.

For motion, record the poses/path actually checked and any interference. Finite pose sampling is not proof of continuous clearance. CAD fit, a closed mesh, and a user's satisfaction with the workflow are not evidence of physical fit, print success or rocking stability.

Save native FreeCAD plus requested STEP/STL, inspect a useful preview, and check export selection, file existence and dimensions/scale. Import unitless STL as millimeters when that is the design unit. Preserve previous revisions. Report actual failures and unverified checks.

## 7. Help with the first print and subsequent feedback

When material or time matters, read [prototype printing](references/prototype-printing.md). Preserve the dimensions and features the test is meant to evaluate. Explain which settings save material versus mainly time; do not promise a reduction without slicing.

Lead delivery with the new behavior, a model image, downloadable files and the important verification limit. State the latest revision and how it differs when useful. If sharing the project is requested, package portable scripts, neutral metadata and a curated case study rather than publishing machine paths or a raw conversation.
