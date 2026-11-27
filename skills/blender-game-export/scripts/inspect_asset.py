"""Report what a game asset contains, from a .blend or an exported file.

Inspect (runs inside Blender):
    blender -b --factory-startup --python-exit-code 1 -P inspect_asset.py -- \
        --file asset.blend [--objects A B] [--json out.json]
    blender -b --factory-startup --python-exit-code 1 -P inspect_asset.py -- \
        --file export/asset.glb --json export.json

Compare two reports (plain Python, no Blender needed):
    python3 inspect_asset.py --compare source.json export.json

A .blend is opened as is. Any other file is imported into an empty scene.
The report measures evaluated geometry (modifiers applied), which is what
an exporter writes. Exit code 2 means the comparison found differences.
"""

import argparse
import json
import sys

IMPORTERS = {
    ".glb": ("import_scene", "gltf"),
    ".gltf": ("import_scene", "gltf"),
    ".fbx": ("import_scene", "fbx"),
    ".obj": ("wm", "obj_import"),
    ".usd": ("wm", "usd_import"),
    ".usda": ("wm", "usd_import"),
    ".usdc": ("wm", "usd_import"),
    ".usdz": ("wm", "usd_import"),
}

MAP_SOCKETS = ("Base Color", "Metallic", "Roughness", "Normal", "Emission Color", "Alpha")

SIZE_TOLERANCE_M = 0.001


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    parser.add_argument("--objects", nargs="*", default=None)
    parser.add_argument("--json")
    parser.add_argument("--compare", nargs=2, metavar=("SOURCE", "EXPORT"))
    return parser.parse_args(argv)


def load_scene(path):
    import os
    import bpy

    extension = os.path.splitext(path)[1].lower()
    if extension == ".blend":
        bpy.ops.wm.open_mainfile(filepath=path)
        return
    if extension not in IMPORTERS:
        raise SystemExit(f"Unsupported file type: {extension}")
    bpy.ops.wm.read_factory_settings(use_empty=True)
    module, operator = IMPORTERS[extension]
    result = getattr(getattr(bpy.ops, module), operator)(filepath=path)
    if result != {"FINISHED"}:
        raise SystemExit(f"Import failed: {result}")


def images_feeding(socket, seen=None):
    seen = seen if seen is not None else set()
    found = []
    for link in socket.links:
        node = link.from_node
        if node.name in seen:
            continue
        seen.add(node.name)
        if node.type == "TEX_IMAGE" and node.image:
            found.append(node.image)
        for upstream in node.inputs:
            found.extend(images_feeding(upstream, seen))
    return found


def material_report(material):
    if material is None:
        return {"name": None, "maps": {}}
    maps = {}
    principled = [n for n in material.node_tree.nodes if n.type == "BSDF_PRINCIPLED"] if material.node_tree else []
    for node in principled:
        for socket_name in MAP_SOCKETS:
            socket = node.inputs.get(socket_name)
            if socket is None:
                continue
            images = images_feeding(socket)
            if images:
                maps[socket_name] = [
                    {"image": image.name, "colorspace": image.colorspace_settings.name, "size": list(image.size)}
                    for image in images
                ]
    return {"name": material.name, "maps": maps}


def world_bounds(objects, depsgraph):
    from mathutils import Vector

    corners = []
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        corners.extend(evaluated.matrix_world @ Vector(corner) for corner in evaluated.bound_box)
    if not corners:
        return None
    low = [min(c[i] for c in corners) for i in range(3)]
    high = [max(c[i] for c in corners) for i in range(3)]
    return {"min": low, "max": high, "size": [high[i] - low[i] for i in range(3)]}


def mesh_report(obj, depsgraph):
    evaluated = obj.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    try:
        triangles = sum(len(polygon.vertices) - 2 for polygon in mesh.polygons)
        uv_maps = [layer.name for layer in mesh.uv_layers]
        influence_counts = [len(vertex.groups) for vertex in mesh.vertices]
    finally:
        evaluated.to_mesh_clear()
    shape_keys = obj.data.shape_keys
    return {
        "name": obj.name,
        "triangles": triangles,
        "scale": list(obj.scale),
        "rotation_euler": list(obj.rotation_euler),
        "location": list(obj.location),
        "parent": obj.parent.name if obj.parent else None,
        "uv_maps": uv_maps,
        "materials": [material_report(slot.material) for slot in obj.material_slots],
        "shape_keys": [key.name for key in shape_keys.key_blocks] if shape_keys else [],
        "max_influences": max(influence_counts, default=0),
        "armature_modifier": any(m.type == "ARMATURE" for m in obj.modifiers),
    }


def armature_report(obj):
    bones = obj.data.bones
    return {
        "name": obj.name,
        "scale": list(obj.scale),
        "bones": len(bones),
        "deform_bones": sum(1 for bone in bones if bone.use_deform),
        "root_bones": [bone.name for bone in bones if bone.parent is None],
    }


def warnings_for(report):
    warnings = []
    for mesh in report["meshes"]:
        if any(abs(s - 1.0) > 1e-4 for s in mesh["scale"]):
            warnings.append(f"{mesh['name']}: scale {mesh['scale']} is not applied")
        if any(s < 0 for s in mesh["scale"]):
            warnings.append(f"{mesh['name']}: negative scale flips normals on export")
        if not mesh["uv_maps"]:
            warnings.append(f"{mesh['name']}: no UV map")
        if any(material["name"] is None for material in mesh["materials"]):
            warnings.append(f"{mesh['name']}: empty material slot")
        if not mesh["materials"]:
            warnings.append(f"{mesh['name']}: no material")
        if mesh["max_influences"] > 4:
            warnings.append(f"{mesh['name']}: {mesh['max_influences']} weights on one vertex (most engines keep 4)")
    for armature in report["armatures"]:
        if len(armature["root_bones"]) > 1:
            warnings.append(f"{armature['name']}: {len(armature['root_bones'])} root bones {armature['root_bones']}")
        if any(abs(s - 1.0) > 1e-4 for s in armature["scale"]):
            warnings.append(f"{armature['name']}: armature scale {armature['scale']}")
    bounds = report["bounds"]
    if bounds and abs(bounds["min"][2]) > SIZE_TOLERANCE_M:
        warnings.append(f"asset base sits at z={bounds['min'][2]:.4f}, not on the floor (z=0)")
    return warnings


def inspect(path, names):
    import bpy

    load_scene(path)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    bone_shapes = {
        bone.custom_shape.name
        for obj in bpy.context.scene.objects
        if obj.type == "ARMATURE"
        for bone in obj.pose.bones
        if bone.custom_shape
    }
    if names:
        objects = [bpy.data.objects[name] for name in names]
    else:
        # The glTF importer adds a display mesh for bones; it is not part of the asset.
        objects = [obj for obj in bpy.context.scene.objects if obj.name not in bone_shapes]
    meshes = [obj for obj in objects if obj.type == "MESH"]
    armatures = [obj for obj in objects if obj.type == "ARMATURE"]
    report = {
        "file": path,
        "blender": bpy.app.version_string,
        "unit_scale": bpy.context.scene.unit_settings.scale_length,
        "meshes": [mesh_report(obj, depsgraph) for obj in meshes],
        "armatures": [armature_report(obj) for obj in armatures],
        "actions": [
            {"name": action.name, "frame_range": list(action.frame_range)} for action in bpy.data.actions
        ],
        "bounds": world_bounds(meshes, depsgraph),
    }
    report["triangles"] = sum(mesh["triangles"] for mesh in report["meshes"])
    report["warnings"] = warnings_for(report)
    return report


def material_maps(report):
    return {
        material["name"]: sorted(material["maps"])
        for mesh in report["meshes"]
        for material in mesh["materials"]
        if material["name"]
    }


def compare(source, exported):
    differences = []
    if source["bounds"] and exported["bounds"]:
        for axis, (a, b) in enumerate(zip(source["bounds"]["size"], exported["bounds"]["size"])):
            if abs(a - b) > SIZE_TOLERANCE_M:
                differences.append(f"size axis {'XYZ'[axis]}: {a:.4f} -> {b:.4f} m")
        if abs(source["bounds"]["min"][2] - exported["bounds"]["min"][2]) > SIZE_TOLERANCE_M:
            differences.append(
                f"base height: {source['bounds']['min'][2]:.4f} -> {exported['bounds']['min'][2]:.4f} m"
            )
    if source["triangles"] != exported["triangles"]:
        differences.append(f"triangles: {source['triangles']} -> {exported['triangles']}")
    source_maps, exported_maps = material_maps(source), material_maps(exported)
    for name, maps in source_maps.items():
        if name not in exported_maps:
            differences.append(f"material {name}: missing after export")
            continue
        lost = sorted(set(maps) - set(exported_maps[name]))
        if lost:
            differences.append(f"material {name}: lost {lost}")
    source_actions = {a["name"] for a in source["actions"]}
    exported_actions = {a["name"] for a in exported["actions"]}
    if len(exported_actions) < len(source_actions):
        differences.append(f"actions: {sorted(source_actions)} -> {sorted(exported_actions)}")
    source_keys = sum(len(m["shape_keys"]) for m in source["meshes"])
    exported_keys = sum(len(m["shape_keys"]) for m in exported["meshes"])
    if source_keys != exported_keys:
        differences.append(f"shape keys: {source_keys} -> {exported_keys}")
    source_bones = sum(a["deform_bones"] for a in source["armatures"])
    exported_bones = sum(a["deform_bones"] for a in exported["armatures"])
    if source_bones != exported_bones:
        differences.append(f"deform bones: {source_bones} -> {exported_bones}")
    for armature in exported["armatures"]:
        if any(abs(s - 1.0) > 1e-4 for s in armature["scale"]):
            differences.append(f"armature {armature['name']} imports at scale {armature['scale']}")
    return differences


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:]
    args = parse_args(argv)
    if args.compare:
        with open(args.compare[0]) as a, open(args.compare[1]) as b:
            differences = compare(json.load(a), json.load(b))
        print(json.dumps({"differences": differences}, indent=2))
        sys.exit(2 if differences else 0)
    if not args.file:
        raise SystemExit("Pass --file to inspect or --compare SOURCE EXPORT")
    report = inspect(args.file, args.objects)
    text = json.dumps(report, indent=2)
    if args.json:
        with open(args.json, "w") as handle:
            handle.write(text)
    print(text)


if __name__ == "__main__":
    main()
