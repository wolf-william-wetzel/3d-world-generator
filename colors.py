from enum import Enum, auto

import pygame as pg


class Color:
    """Utility class for holding colors and color manipulating functions."""

    @staticmethod
    def darken(color: tuple[int, int, int], amount: float = 0.75) -> tuple[int, int, int]:
        """Darken a color to true black by linear interpolation."""
        return pg.Color(color).lerp((0, 0, 0), amount).rgb

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    DARK_BLUE = (0, 0, 128)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    YELLOW = (255, 255, 0)
    GRAY = (170, 170, 170)
    DARK_GRAY = (85, 85, 85)
    ORANGE = (255, 128, 0)
    BROWN = (128, 64, 0)
    DARK_BROWN = (64, 32, 0)
    MEMORY = (16, 16, 16)

    SAND = (255, 210, 0)
    SAND_BG = (180, 150, 0)
    STONE = GRAY
    STONE_BG = DARK_GRAY
    STONE_BRICK = DARK_GRAY
    STONE_BRICK_BG = GRAY
    DIRT = BROWN
    DIRT_BG = DARK_BROWN
    WATER = BLUE
    WATER_BG = DARK_BLUE
    WOOD = BROWN
    WOOD_BG = DARK_BROWN
    GRASS = (0, 170, 0)
    LEAVES = GREEN
    SWAMP_GRASS = (0, 170, 64)


class Image(Enum):
    """Utility enum for holding unique image IDs and generating tile graphics."""

    @classmethod
    def ramp_graphic(cls, color: tuple[int, int, int]) -> tuple:
        """The only thing needed for slope-like tiles is a color."""
        return cls.RAMP_UP, color, Color.BLACK, cls.RAMP_DOWN, color

    @classmethod
    def stair_graphic(cls, color: tuple[int, int, int]) -> tuple:
        """The only thing needed for slope-like tiles is a color."""
        return cls.STAIRS_UP, color, Color.BLACK, cls.STAIRS_DOWN, color

    @staticmethod
    def prop_graphic(image: "Image", color: tuple[int, int, int]) -> tuple:
        """Prop blocks appear one z-level further down than they are."""
        return image, color, Color.BLACK, image, Color.darken(color)

    @staticmethod
    def block_graphic(image: "Image", color: tuple[int, int, int], bg_color: tuple[int, int, int]) -> tuple:
        """Full blocks have the same appearance from the top and side."""
        return image, color, bg_color, image, color

    GRASS = auto()
    RAMP_UP = auto()
    RAMP_DOWN = auto()
    STAIRS_UP = auto()
    STAIRS_DOWN = auto()
    DIRT = auto()
    STONE = auto()
    SAND = auto()
    TRUNK = auto()
    LEAVES = auto()
    PILLAR = auto()
    PILLAR_TOP = auto()
    WATER = auto()
    BRICKS = auto()
    PLANKS = auto()
    FLOWER_1 = auto()
    FLOWER_2 = auto()
    ALTAR = auto()
    DOOR = auto()
    DOOR_TOP = auto()
    PLAYER = auto()
    SWAMP_GRASS = auto()


# This image scheme dict allows us to swap fonts whenever we please.
image_scheme = {
    "cp437": {
        Image.PLAYER: (1, 0),
        Image.GRASS: (2, 2),
        Image.SWAMP_GRASS: (4, 15),
        Image.RAMP_UP: (14, 1),
        Image.RAMP_DOWN: (15, 1),
        Image.STAIRS_UP: (14, 1),
        Image.STAIRS_DOWN: (15, 1),
        Image.DIRT: (9, 15),
        Image.STONE: (5, 2),
        Image.SAND: (14, 7),
        Image.TRUNK: (9, 0),
        Image.LEAVES: (5, 0),
        Image.PILLAR: (7, 0),
        Image.PILLAR_TOP: (9, 15),
        Image.WATER: (7, 15),
        Image.BRICKS: (3, 2),
        Image.PLANKS: (0, 15),
        Image.FLOWER_1: (10, 2),
        Image.FLOWER_2: (15, 0),
        Image.ALTAR: (6, 1),
        Image.DOOR: (11, 2),
        Image.DOOR_TOP: (11, 2),
    },
    "kenney": {
        Image.PLAYER: (25, 0),
        Image.GRASS: (5, 0),
        Image.SWAMP_GRASS: (0, 2),
        Image.RAMP_UP: (4, 18),
        Image.RAMP_DOWN: (3, 18),
        Image.STAIRS_UP: (2, 6),
        Image.STAIRS_DOWN: (3, 6),
        Image.DIRT: (6, 0),
        Image.STONE: (7, 0),
        Image.SAND: (2, 0),
        Image.TRUNK: (18, 6),
        Image.LEAVES: (4, 2),
        Image.PILLAR: (27, 21),
        Image.PILLAR_TOP: (27, 20),
        Image.WATER: (1, 17),
        Image.BRICKS: (10, 17),
        Image.PLANKS: (13, 16),
        Image.FLOWER_1: (29, 12),
        Image.FLOWER_2: (28, 12),
        Image.ALTAR: (15, 9),
        Image.DOOR: (8, 9),
        Image.DOOR_TOP: (8, 9),
    },
}
