# Access and motion

Read when a fitted pocket is deep, closed walls matter, or a rocking/lifting mechanism is proposed.

## Choose the simplest useful access

| Method | Useful when | Check |
|---|---|---|
| Item protrudes above pocket | No stacked-bin interference | Graspable height versus lip and drawer clearance |
| Internal finger recess | Closed exterior is wanted | Actual fingertip room at both sides, not merely a visible groove |
| Open side notch | User accepts interrupted walls | Neighboring bins, wall strength and interruption of stacking rim |
| Press-to-lift on a fixed support | Rigid elongated item; limited finger room | Space below pressed end, end sweep, support position and stable resting pose |
| Removable insert or lifting tab | Shape is fragile or cannot rock | Extra parts, grip space and lift path |

Removing a side notch does not solve removal: explain the tradeoff while honoring the requested variant. Do not silently reintroduce a notch later. Retain usable access when a stacking lip is added.

## Specify a press-to-lift concept

A transverse rounded support beneath rigid casing can act as a fulcrum. Leave a deeper cavity under the pressed end and support the other end at rest if needed. Keep pressure off switches, squeezable adhesive grips, fragile caps and release mechanisms.

Define:
- Item plan and side profiles, including underside steps and uncertainty.
- Neutral item position and Z references.
- Support axis/contact geometry; cylinder **center** and top are different.
- Secondary rest and the assumed center-of-mass side of the support.
- Which end is pressed, travel, tilt range, grip height above the lip.
- Removal path after lifting; straight vertical removal in a tilted pose can catch the rim.

A pencil-under-the-item trial can locate a candidate contact point. Offer it when useful; do not require it after the user accepts assumed dimensions.

For rotation about the X axis through (y0, z0), with positive angle raising +Y:

```text
y' = y0 + (y-y0) cos(theta) - (z-z0) sin(theta)
z' = z0 + (y-y0) sin(theta) + (z-z0) cos(theta)
```

These equations describe the selected rigid-body motion. A free item may slide or roll instead; friction and casing curvature determine actual motion. Do not imply that the rounded support provides a hinged constraint.

## Check more than endpoint heights

Create a clearly named, non-exported surrogate from the agreed item geometry. Test the resting pose, intermediate tilt poses, final tilt, and extraction/return path against:
- Perimeter walls and contour shoulders.
- Pocket floor, pivot and secondary rest.
- Stacking lip, especially the rear end while lifting.
- Neighboring stored items and a lid, if relevant.

Record angle/translation step, collision volumes or distances, and intentional contacts. Zero intersection volume allows tangential contact and says nothing about positive manufacturing clearance. Measure critical gaps separately. For sample-only checks, report sample count/range and the sampling limitation. Refine around tight clearances or use a continuous swept envelope when warranted.

A "smallest" static pocket may be too short during rotation: the side projection of an ideal rectangular item is L cos(theta) + T sin(theta). Use the actual shape where available; an endpoint or bounding-box calculation alone is not a full collision check.

Check support stability, potential rolling and finger access as separate physical questions. State that a tested angular range is not necessarily a mechanical stop. If a smaller assumed item is necessary, explicitly revise the envelope instead of quietly weakening an earlier conservative fit claim.
