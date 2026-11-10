from pathlib import Path
import json
import struct
import zlib

root = Path(__file__).parent.parent
items_dir = root / "behavior_pack" / "items"
blocks_dir = root / "behavior_pack" / "blocks"
resource_root = root / "resource_pack"
client_blocks_dir = resource_root / "blocks"
geometry_dir = resource_root / "models" / "blocks"
features_dir = root / "behavior_pack" / "features"
feature_rules_dir = root / "behavior_pack" / "feature_rules"
resource_textures = resource_root / "textures"
item_texture_dir = resource_textures / "items"
block_texture_dir = resource_textures / "blocks"
for directory in (items_dir, blocks_dir, features_dir, feature_rules_dir, client_blocks_dir, geometry_dir, item_texture_dir, block_texture_dir):
    directory.mkdir(parents=True, exist_ok=True)

fruits = ["apple", "banana", "kiwi", "mango", "pineapple", "coconut", "strawberry", "blueberry", "raspberry", "blackberry", "cherry", "peach", "pear", "plum", "apricot", "lemon", "lime", "orange", "grapefruit", "grape", "watermelon", "melonberry", "passionfruit", "dragonfruit", "papaya", "guava", "pomegranate", "cranberry", "elderberry", "fig"]
item_ids = [f"{kind}_{fruit}" for kind in ("fruit", "dried", "tea", "juice", "drink") for fruit in fruits]
item_ids += ["tapioca", "sugar", "sugar_syrup", "boba", "popping_boba", "boba_cup", "sealed_boba", "straw", "seal", "blender", "dough_station", "sealer", "boba_glass"]
block_ids = ["blender", "dough_station", "sealer", "boba_glass", "fruit_bush"]
fruit_biomes = {
    "banana": "jungle", "kiwi": "forest", "mango": "jungle", "pineapple": "jungle", "coconut": "jungle",
    "strawberry": "plains", "blueberry": "taiga", "raspberry": "taiga", "blackberry": "forest", "cherry": "cherry_grove",
    "peach": "plains", "pear": "forest", "plum": "forest", "apricot": "savanna", "lemon": "savanna",
    "lime": "jungle", "orange": "savanna", "grapefruit": "savanna", "grape": "plains", "watermelon": "savanna",
    "melonberry": "jungle", "passionfruit": "jungle", "dragonfruit": "jungle", "papaya": "jungle", "guava": "jungle",
    "pomegranate": "desert", "cranberry": "swamp", "elderberry": "forest", "fig": "desert",
}


def png_chunk(kind, payload):
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xffffffff)


FRUIT_COLORS = {
    "apple": (214, 54, 48), "banana": (244, 205, 58), "kiwi": (113, 166, 67), "mango": (242, 151, 39),
    "pineapple": (226, 179, 53), "coconut": (132, 88, 53), "strawberry": (224, 52, 65), "blueberry": (67, 91, 190),
    "raspberry": (192, 48, 101), "blackberry": (73, 38, 105), "cherry": (181, 39, 52), "peach": (246, 143, 112),
    "pear": (178, 204, 59), "plum": (126, 66, 145), "apricot": (238, 133, 55), "lemon": (242, 218, 53),
    "lime": (111, 190, 55), "orange": (239, 123, 31), "grapefruit": (244, 111, 105), "grape": (111, 67, 164),
    "watermelon": (220, 67, 72), "melonberry": (174, 78, 113), "passionfruit": (196, 113, 42), "dragonfruit": (224, 66, 133),
    "papaya": (239, 125, 43), "guava": (232, 112, 126), "pomegranate": (167, 39, 50), "cranberry": (180, 42, 61),
    "elderberry": (78, 53, 119), "fig": (139, 75, 104),
}
INK = (45, 32, 42)
LEAF = (57, 132, 61)
CREAM = (255, 237, 177)


def write_texture(path, name):
    canvas = [[(0, 0, 0, 0) for _ in range(16)] for _ in range(16)]

    def pixel(x, y, color, alpha=255):
        if 0 <= x < 16 and 0 <= y < 16:
            canvas[y][x] = (*color, alpha)

    def rect(x0, y0, x1, y1, color, alpha=255):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                pixel(x, y, color, alpha)

    def fruit_shape(color):
        rect(5, 3, 10, 4, color)
        rect(3, 5, 12, 11, color)
        rect(4, 12, 11, 13, color)
        rect(6, 2, 7, 3, INK)
        rect(8, 1, 10, 2, LEAF)
        pixel(4, 6, tuple(min(255, c + 55) for c in color))
        pixel(5, 5, tuple(min(255, c + 35) for c in color))
        rect(3, 11, 4, 12, tuple(max(0, c - 45) for c in color))

    fruit = next((value for key, value in FRUIT_COLORS.items() if key in name), (174, 112, 66))
    if name.startswith("fruit_"):
        fruit_shape(fruit)
    elif name.startswith("dried_"):
        rect(3, 4, 12, 11, tuple(max(0, c - 30) for c in fruit))
        rect(5, 3, 10, 12, tuple(min(255, c + 25) for c in fruit))
        for x, y in ((5, 5), (8, 7), (10, 10), (6, 10)):
            pixel(x, y, tuple(max(0, c - 45) for c in fruit))
    elif name.startswith("tea_"):
        rect(4, 3, 11, 13, CREAM)
        rect(5, 5, 10, 11, fruit)
        rect(3, 2, 12, 4, INK)
        rect(6, 1, 9, 2, INK)
        pixel(11, 8, CREAM)
    elif name.startswith("juice_") or name.startswith("drink_"):
        rect(5, 2, 10, 4, CREAM)
        rect(4, 5, 11, 13, fruit)
        rect(5, 6, 10, 7, tuple(min(255, c + 45) for c in fruit))
        rect(4, 4, 11, 5, INK)
        rect(7, 1, 8, 3, INK)
        if name.startswith("drink_"):
            rect(9, 0, 10, 4, (245, 245, 230))
    elif name in ("tapioca", "boba", "popping_boba"):
        ball = (238, 219, 175) if name == "tapioca" else ((76, 42, 32) if name == "boba" else fruit)
        for x, y in ((5, 5), (9, 5), (7, 9), (11, 9), (4, 12), (9, 12)):
            rect(x, y, x + 2, y + 2, ball)
            pixel(x, y, tuple(min(255, c + 35) for c in ball))
    elif name in ("sugar", "sugar_syrup", "salt"):
        rect(3, 5, 12, 12, CREAM)
        rect(4, 4, 11, 5, (244, 221, 151))
        pixel(6, 7, (255, 255, 236))
    elif name in ("boba_cup", "sealed_boba", "straw", "seal"):
        rect(4, 5, 11, 13, (224, 238, 231), 185)
        rect(5, 7, 10, 12, fruit, 210)
        rect(3, 4, 12, 5, (245, 245, 235), 230)
        rect(7, 1, 8, 4, (240, 75, 100))
        if name == "straw":
            rect(7, 1, 8, 14, (240, 75, 100))
        if name == "seal":
            rect(3, 3, 12, 5, (240, 75, 100))
    else:
        rect(2, 3, 13, 13, (116, 84, 62))
        rect(3, 4, 12, 11, (191, 139, 77))
        rect(4, 5, 11, 10, (91, 143, 145))
        rect(5, 6, 10, 9, (224, 183, 91))
        rect(6, 7, 9, 8, INK)
        if name == "boba_glass":
            rect(4, 4, 11, 12, (180, 235, 235), 110)
            rect(5, 10, 10, 12, (70, 45, 45), 220)
        if name == "fruit_bush":
            rect(3, 8, 12, 12, LEAF)
            rect(4, 5, 11, 9, (70, 158, 70))
            pixel(6, 6, fruit)
            pixel(9, 8, fruit)

    raw = b"".join(b"\x00" + bytes(channel for pixel_value in row for channel in pixel_value) for row in canvas)
    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 6, 0, 0, 0))
    png += png_chunk(b"IDAT", zlib.compress(raw, 9)) + png_chunk(b"IEND", b"")
    path.write_bytes(png)


def write_atlas(path, texture_name, names, folder):
    atlas = {"resource_pack_name": "Tea & Boba Resources", "texture_name": texture_name,
             "texture_data": {name: {"textures": f"textures/{folder}/{name}"} for name in names}}
    path.write_text(json.dumps(atlas, indent=2) + "\n", encoding="utf-8")


for name in item_ids:
    write_texture(item_texture_dir / f"{name}.png", name)
    components = {"minecraft:icon": {"texture": name}, "minecraft:display_name": {"value": name.replace("_", " ").title()}, "minecraft:max_stack_size": 64}
    if name.startswith("drink_"):
        components.update({"minecraft:food": {"nutrition": 4, "saturation_modifier": 0.6, "can_always_eat": False}, "minecraft:use_animation": "drink", "minecraft:use_duration": 32})
    definition = {"format_version": "1.20.50", "minecraft:item": {"description": {"identifier": f"tea_boba:{name}", "menu_category": {"category": "items"}}, "components": components}}
    (items_dir / f"{name}.json").write_text(json.dumps(definition, indent=2) + "\n", encoding="utf-8")


def cuboid(origin, size, uv):
    return {"origin": origin, "size": size, "uv": uv}


def block_geometry(name):
    cubes = []
    if name in ("blender", "dough_station", "sealer"):
        cubes.extend([cuboid([1, 0, 1], [14, 3, 14], [0, 0]), cuboid([2, 3, 2], [12, 8, 12], [0, 0]), cuboid([3, 11, 3], [10, 2, 10], [0, 0])])
        if name == "blender":
            cubes.extend([cuboid([4, 13, 4], [8, 7, 8], [0, 0]), cuboid([5, 20, 5], [6, 1, 6], [0, 0]), cuboid([6, 21, 6], [4, 1, 4], [0, 0])])
        elif name == "dough_station":
            cubes.extend([cuboid([2, 13, 2], [12, 2, 12], [0, 0]), cuboid([4, 15, 4], [8, 1, 8], [0, 0])])
        else:
            cubes.extend([cuboid([4, 13, 4], [8, 6, 8], [0, 0]), cuboid([3, 19, 3], [10, 2, 10], [0, 0]), cuboid([7, 21, 7], [2, 5, 2], [0, 0])])
    elif name == "boba_glass":
        cubes.extend([cuboid([2, 0, 2], [12, 1, 12], [0, 0]), cuboid([2, 1, 2], [2, 11, 12], [0, 0]), cuboid([12, 1, 2], [2, 11, 12], [0, 0]), cuboid([4, 1, 2], [8, 11, 2], [0, 0]), cuboid([4, 1, 12], [8, 11, 2], [0, 0]), cuboid([1, 12, 1], [14, 1, 14], [0, 0])])
        for x in (4, 8, 12):
            for z in (4, 8):
                cubes.append(cuboid([x, 3, z], [2, 2, 2], [0, 0]))
    else:
        cubes.extend([cuboid([6, 0, 6], [4, 6, 4], [0, 0]), cuboid([3, 4, 3], [10, 7, 10], [0, 0]), cuboid([1, 7, 4], [4, 5, 8], [0, 0]), cuboid([11, 7, 4], [4, 5, 8], [0, 0]), cuboid([4, 8, 1], [8, 4, 4], [0, 0]), cuboid([4, 8, 11], [8, 4, 4], [0, 0])])
        for x, y, z in ((4, 10, 5), (9, 8, 6), (6, 7, 10)):
            cubes.append(cuboid([x, y, z], [2, 2, 2], [0, 0]))
    return {"format_version": "1.16.0", "minecraft:geometry": [{"description": {"identifier": f"geometry.tea_boba.{name}", "texture_width": 16, "texture_height": 16, "visible_bounds_width": 2.5, "visible_bounds_height": 2.5, "visible_bounds_offset": [0, 0.75, 0]}, "bones": [{"name": "root", "pivot": [8, 0, 8], "cubes": cubes}]}]}


for name in block_ids:
    write_texture(block_texture_dir / f"{name}.png", name)
    (geometry_dir / f"{name}.geo.json").write_text(json.dumps(block_geometry(name), indent=2) + "\n", encoding="utf-8")
    client_definition = {"format_version": "1.20.80", "minecraft:block": {"description": {"identifier": f"tea_boba:{name}"}, "components": {"minecraft:geometry": {"identifier": f"geometry.tea_boba.{name}"}, "minecraft:material_instances": {"*": {"texture": name, "render_method": "blend" if name == "boba_glass" else "alpha_test" if name == "fruit_bush" else "opaque"}}}}}
    (client_blocks_dir / f"{name}.json").write_text(json.dumps(client_definition, indent=2) + "\n", encoding="utf-8")
    components = {"minecraft:geometry": "minecraft:geometry.full_block", "minecraft:material_instances": {"*": {"texture": name, "render_method": "opaque"}}, "minecraft:destructible_by_mining": {"seconds_to_destroy": 1.5}, "minecraft:destructible_by_explosion": {"explosion_resistance": 3}}
    if name == "fruit_bush":
        components["minecraft:states"] = {"tea_boba:fruit": {"values": fruits}, "tea_boba:ripe": [False, True]}
    definition = {"format_version": "1.20.50", "minecraft:block": {"description": {"identifier": f"tea_boba:{name}", "menu_category": {"category": "construction"}}, "components": components}}
    (blocks_dir / f"{name}.json").write_text(json.dumps(definition, indent=2) + "\n", encoding="utf-8")

for fruit, biome in fruit_biomes.items():
    feature = {"format_version": "1.13.0", "minecraft:single_block_feature": {"description": {"identifier": f"tea_boba:{fruit}_bush_feature"}, "places_block": f"tea_boba:fruit_bush", "may_place_on": ["minecraft:grass_block", "minecraft:dirt", "minecraft:podzol", "minecraft:sand"], "may_replace": ["minecraft:air", "minecraft:short_grass", "minecraft:tall_grass", "minecraft:fern"], "can_replace": False, "may_place": True, "enforce_placement_rule": True, "block_states": {"tea_boba:fruit": fruit, "tea_boba:ripe": True}}}
    rule = {"format_version": "1.13.0", "minecraft:feature_rules": {"description": {"identifier": f"tea_boba:{fruit}_bush_rule", "places_feature": f"tea_boba:{fruit}_bush_feature"}, "conditions": {"placement_pass": "surface_pass", "minecraft:biome_filter": [{"test": "has_biome_tag", "operator": "==", "value": biome}]}, "distribution": {"iterations": 1, "coordinate_eval_order": "xzy", "x": {"distribution": "uniform", "extent": [0, 15]}, "y": "q.heightmap(variable.worldx, variable.worldz)", "z": {"distribution": "uniform", "extent": [0, 15]}}}}
    (features_dir / f"{fruit}_bush_feature.json").write_text(json.dumps(feature, indent=2) + "\n", encoding="utf-8")
    (feature_rules_dir / f"{fruit}_bush.json").write_text(json.dumps(rule, indent=2) + "\n", encoding="utf-8")

write_atlas(resource_textures / "item_texture.json", "atlas.items", item_ids, "items")
write_atlas(resource_textures / "terrain_texture.json", "atlas.terrain", block_ids, "blocks")
