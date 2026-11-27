# Matching references

For building an asset from orthographic turnarounds, concept art, or photos.

## Separate what is visible from what is inferred

Before modeling, list for each reference which parts of the object it shows and which it hides. A front and side turnaround shows the outline in two planes but not the cross-section between them; a single concept painting shows one side and a perspective guess. Model visible geometry to match, and mark inferred geometry (the back, the underside, the cross-section) as a decision to confirm or state in the report.

## Orthographic turnarounds

1. Check the views agree: the same feature (top of the head, a belt line, the bottom of the wheels) must sit at the same height in front and side views. If they disagree, ask which wins, or pick one and say so.
2. Load each image as a reference empty (`bpy.data.objects.new(name, None)`, `empty_display_type = "IMAGE"`, `data = image`) aligned to its axis: front view on the XZ plane facing -Y, side view on the YZ plane.
3. Scale the images so a known dimension matches real size (overall height, wheelbase), and put the ground line on z = 0.
4. Pick three or four landmarks visible in two views (tips, corners, joints) and confirm their 3D positions agree between views before building.
5. Block out against the images, then render the same orthographic views with `review_renders.py` and compare outlines with the reference. Overlay by setting the reference empty's opacity, or compare silhouettes side by side.

## Photos and concept art in perspective

1. Estimate the camera: lens, height, and angle. A camera matched to the image (Blender camera with the image as a camera background in a live session) lets you compare the render and the reference from the same view.
2. Match proportions in that matched view, then check the other views for plausibility, since the reference cannot confirm them.
3. Report which dimensions came from the reference and which were inferred.

## Comparing

Compare silhouettes first: outline mismatches are the ones players notice. Then landmark positions. Interior detail last. When the model and reference disagree, say which one you followed and why. A reference with a perspective error should not be copied into an orthographic model.
