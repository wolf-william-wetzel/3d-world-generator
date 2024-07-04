from enum import IntEnum, auto

from colors import Color, Image


class Tile(IntEnum):
    """Utility class for storing all unique Tile IDs."""
    STONE = auto()
    DIRT = auto()
    GRASS = auto()
    TREE = auto()
    WATER = auto()
    SAND = auto()
    AIR = auto()
    GRASS_SLOPE = auto()
    STONE_SLOPE = auto()
    SAND_SLOPE = auto()
    RED_FLOWER = auto()
    YELLOW_FLOWER = auto()
    SWAMP_GRASS = auto()

    STONE_BRICKS = auto()
    WOOD_PLANKS = auto()
    WOOD_DOOR = auto()
    WOOD_STAIRS = auto()
    WOOD_RAMP = auto()
    STONE_STAIRS = auto()
    STONE_PILLAR = auto()
    ALTAR = auto()


# These data structures hold tile data, like whether they block movement.

prop_tiles = (
    Tile.AIR,
    Tile.ALTAR,
    Tile.RED_FLOWER,
    Tile.YELLOW_FLOWER,
    Tile.SWAMP_GRASS,
)

passable_tiles = (
    Tile.AIR,
    Tile.ALTAR,
    Tile.RED_FLOWER,
    Tile.YELLOW_FLOWER,
    Tile.SWAMP_GRASS,
    Tile.STONE_STAIRS,
    Tile.WOOD_STAIRS,
    Tile.SAND_SLOPE,
    Tile.GRASS_SLOPE,
    Tile.STONE_SLOPE,
    Tile.WOOD_DOOR,
    Tile.WOOD_RAMP,
)

slope_tiles = (
    Tile.STONE_SLOPE,
    Tile.SAND_SLOPE,
    Tile.GRASS_SLOPE,
    Tile.WOOD_RAMP,
    Tile.STONE_STAIRS,
    Tile.WOOD_STAIRS,
)

# Each graphic consists of IMAGE, COLOR, BG_COLOR, IMAGE, COLOR.
# The first three are used for the side perspective, the last two for the top perspective.
# No tiles from a top perspective should have background color.
# This allows easy visual difference for the player to notice.
tile_graphics = {
    Tile.STONE: Image.block_graphic(Image.STONE, Color.STONE, Color.STONE_BG),
    Tile.DIRT: Image.block_graphic(Image.DIRT, Color.DIRT, Color.DIRT_BG),
    Tile.WATER: Image.block_graphic(Image.WATER, Color.WATER, Color.WATER_BG),
    Tile.SAND: Image.block_graphic(Image.SAND, Color.SAND, Color.SAND_BG),
    Tile.STONE_BRICKS: Image.block_graphic(Image.BRICKS, Color.STONE_BRICK, Color.STONE_BRICK_BG),
    Tile.WOOD_PLANKS: Image.block_graphic(Image.PLANKS, Color.WOOD, Color.WOOD_BG),

    Tile.GRASS: (Image.DIRT, Color.DIRT, Color.DIRT_BG, Image.GRASS, Color.GRASS),
    Tile.TREE: (Image.TRUNK, Color.WOOD, Color.BLACK, Image.LEAVES, Color.LEAVES),
    Tile.WOOD_DOOR: (Image.DOOR, Color.WOOD, Color.WOOD_BG, Image.DOOR_TOP, Color.WOOD),
    Tile.STONE_PILLAR: (Image.PILLAR, Color.STONE, Color.BLACK, Image.PILLAR_TOP, Color.STONE),

    Tile.ALTAR: Image.prop_graphic(Image.ALTAR, Color.STONE),
    Tile.RED_FLOWER: Image.prop_graphic(Image.FLOWER_1, Color.RED),
    Tile.YELLOW_FLOWER: Image.prop_graphic(Image.FLOWER_2, Color.YELLOW),
    Tile.SWAMP_GRASS: Image.prop_graphic(Image.SWAMP_GRASS, Color.SWAMP_GRASS),

    Tile.STONE_STAIRS: Image.stair_graphic(Color.STONE),
    Tile.WOOD_STAIRS: Image.stair_graphic(Color.WOOD),
    Tile.GRASS_SLOPE: Image.ramp_graphic(Color.GRASS),
    Tile.STONE_SLOPE: Image.ramp_graphic(Color.STONE),
    Tile.SAND_SLOPE: Image.ramp_graphic(Color.SAND),
    Tile.WOOD_RAMP: Image.ramp_graphic(Color.WOOD),
}
