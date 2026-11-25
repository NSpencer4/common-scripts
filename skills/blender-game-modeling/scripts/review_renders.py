"""Render review images of an asset with the Workbench engine.

    blender -b asset.blend --factory-startup --python-exit-code 1 -P review_renders.py -- \
        --out /abs/review [--objects A B] [--views front side threequarter top] \
        [--modes solid wire silhouette] [--res 768] [--gameplay-distance 4]

Orthographic views are framed on the objects' bounds. --gameplay-distance adds a
perspective view from eye height (1.7 m) at that distance, in front of the asset at
three-quarter angle, with a 1.8 m reference box beside it. Prints one JSON line
listing the written files. Nothing is saved to the .blend.
"""

import argparse
import json
import math
import os
import sys

import bpy
from mathutils import Vector

VIEW_DIRECTIONS = {
    "front": Vector((0, -1, 0)),
    "back": Vector((0, 1, 0)),
    "side": Vector((1, 0, 0)),
    "threequarter": Vector((1, -1, 0.6)),
    "top": Vector((0, 0, 1)),
    "low": Vector((0.6, -1, -0.3)),
}

EYE_HEIGHT_M = 1.7
HUMAN_BOX_SIZE_M = (0.5, 0.3, 1.8)


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--objects", nargs="*")
    parser.add_argument("--views", nargs="*", default=["front", "side", "threequarter"])
    parser.add_argument("--modes", nargs="*", default=["solid", "wire", "silhouette"])
    parser.add_argument("--res", type=int, default=768)
    parser.add_argument("--gameplay-distance", type=float)
    return parser.parse_args(argv)


def bounds(objects):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    corners = []
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        corners.extend(evaluated.matrix_world @ Vector(c) for c in evaluated.bound_box)
    low = Vector([min(c[i] for c in corners) for i in range(3)])
    high = Vector([max(c[i] for c in corners) for i in range(3)])
    return low, high


def set_mode(scene, mode, objects, radius):
    # Workbench renders only draw outlines in WIREFRAME shading, so wire mode
    # renders a temporary Wireframe modifier as solid black geometry instead.
    for obj in objects:
        existing = obj.modifiers.get("ReviewWire")
        if existing:
            obj.modifiers.remove(existing)
        if mode == "wire":
            wire = obj.modifiers.new("ReviewWire", "WIREFRAME")
            wire.thickness = radius * 0.004
            wire.use_relative_offset = False
            wire.use_even_offset = False
    shading = scene.display.shading
    shading.type = "SOLID"
    if mode == "solid":
        shading.light = "MATCAP"
        shading.color_type = "MATERIAL"
        scene.world.color = (0.35, 0.35, 0.35)
        return
    shading.light = "FLAT"
    shading.color_type = "SINGLE"
    shading.single_color = (0.0, 0.0, 0.0)
    scene.world.color = (1.0, 1.0, 1.0)


def aim(camera, target):
    direction = target - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def render(scene, path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    return path


def main():
    args = parse_args()
    os.makedirs(args.out, exist_ok=True)
    scene = bpy.context.scene
    objects = (
        [bpy.data.objects[name] for name in args.objects]
        if args.objects
        else [obj for obj in scene.objects if obj.type == "MESH" and obj.visible_get()]
    )
    if not objects:
        raise SystemExit("No mesh objects to render")
    visible = set(objects)
    for obj in scene.objects:
        if obj.type == "MESH" and obj not in visible:
            obj.hide_render = True

    if scene.world is None:
        scene.world = bpy.data.worlds.new("ReviewWorld")
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = scene.render.resolution_y = args.res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.display.shading.show_object_outline = True

    camera = bpy.data.objects.new("ReviewCamera", bpy.data.cameras.new("ReviewCamera"))
    scene.collection.objects.link(camera)
    scene.camera = camera

    low, high = bounds(objects)
    center = (low + high) / 2
    radius = (high - low).length / 2
    written = []

    camera.data.type = "ORTHO"
    camera.data.ortho_scale = radius * 2.2
    camera.data.clip_end = radius * 20
    for view in args.views:
        camera.location = center + VIEW_DIRECTIONS[view].normalized() * radius * 4
        aim(camera, center)
        for mode in args.modes:
            set_mode(scene, mode, objects, radius)
            written.append(render(scene, os.path.join(args.out, f"{view}_{mode}.png")))
    set_mode(scene, "solid", objects, radius)

    if args.gameplay_distance:
        box = bpy.data.objects.new("HumanScale", bpy.data.meshes.new("HumanScale"))
        scene.collection.objects.link(box)
        sx, sy, sz = HUMAN_BOX_SIZE_M
        box.data.from_pydata(
            [(x, y, z) for x in (0, sx) for y in (0, sy) for z in (0, sz)],
            [],
            [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)],
        )
        box.location = (low.x - 0.3 - sx, center.y - sy / 2, low.z)
        camera.data.type = "PERSP"
        camera.data.lens = 35
        camera.data.clip_end = args.gameplay_distance * 20
        heading = Vector((1, -1, 0)).normalized()
        camera.location = Vector((center.x, center.y, low.z + EYE_HEIGHT_M)) + heading * args.gameplay_distance
        aim(camera, Vector((center.x, center.y, low.z + (high.z - low.z) / 2)))
        set_mode(scene, "solid", objects, radius)
        written.append(render(scene, os.path.join(args.out, "gameplay_solid.png")))

    print(json.dumps({"written": written, "size_m": list(high - low)}))


if __name__ == "__main__":
    main()
