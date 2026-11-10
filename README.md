# Minecraft Bedrock Tea and Boba Mod

Boba & Orchard is a Minecraft Bedrock mod and add-on source project for Minecraft 1.21 that adds fruit items, dried fruit, teas, juices, boba ingredients, drink items, custom blocks, fruit bushes, resource-pack textures, and basic scripted tea and boba interactions.

## Install

1. Use Minecraft Bedrock Edition 1.21 or a compatible version.
2. Ensure Python 3 is installed if you need to regenerate the definitions and textures.
3. From the project root, run:

   `python scripts/generate_defs.py`

4. Create a behavior pack folder in the Bedrock development behavior packs directory.
5. Copy `manifest.json`, the `scripts` folder, and the `behavior_pack` folder contents into the behavior pack root.
6. Create a separate resource pack folder in the Bedrock development resource packs directory.
7. Copy `resources_manifest.json` into the resource pack root.
8. Copy the `resource_pack/textures`, `resource_pack/blocks`, and `resource_pack/models` folders into the resource pack root.
9. Create or open a Minecraft world.
10. Enable both the behavior pack and resource pack for the world.
11. Enable Script API or creator experiments if required by the installed Minecraft version.
12. This project is source material and is not packaged as a `.mcaddon` file.

## Use

1. Enter the world with both packs enabled.
2. Use commands to obtain sample items, such as:

   `/give @s tea_boba:fruit_kiwi`

   `/give @s tea_boba:blender`

   `/give @s tea_boba:drink_kiwi`

3. Interact with fruit bushes to collect their assigned fruit.
4. Use a fruit item to trigger the currently implemented fruit-to-juice interaction.
5. Use a dried fruit item to trigger the currently implemented dried-fruit-to-tea interaction.
6. Use the generated drink items as food and drink items.
7. The script checks for a straw when using sealed boba and consumes a straw when the required interaction succeeds.
8. The project includes definitions and textures for the blender, dough station, sealer, boba glass, and fruit bush.
9. The project includes 30 fruit item families, including apple and 29 additional fruits. The additional fruit bushes are assigned to biome tags such as jungle, forest, plains, taiga, savanna, desert, swamp, and cherry grove.
10. Regenerate the definitions after changing `scripts/generate_defs.py`.
11. The machines currently do not provide complete recipe interfaces or automated machine processing. Full glass filling, boba recipes, sealer controls, selectable seal and straw colors, and complete biome generation gameplay are not implemented.

---

More Minecraft mod projects by EnderDevelopment: https://github.com/EnderDevelopment

Project page: https://dash.enderdevelopment.com/community/6c78b8ec-8d01-4b12-b702-1710f2ea4698?utm_source=github&utm_medium=readme&utm_campaign=auto_publish&utm_content=6c78b8ec-8d01-4b12-b702-1710f2ea4698
