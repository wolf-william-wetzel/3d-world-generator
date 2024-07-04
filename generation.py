from enum import Enum, auto
import random

import opensimplex

from utils import array3d, array2d
import structures
from tiles import Tile

from typing import Sequence


WorldArrayType = list[list[list[Tile]]]


def get_tile(array: WorldArrayType, pos: Sequence[float]) -> Tile:
    """Utility function for easily getting tiles from an array using 3D vectors."""
    return array[int(pos[0])][int(pos[1])][int(pos[2])]


class Biome(Enum):
    """Utility class for storing unique biome IDs."""
    SWAMP = auto()
    DESERT = auto()
    PLAINS = auto()
    FOREST = auto()
    OCEAN = auto()
    MOUNTAIN = auto()
    ROCKY_SWAMP = auto()


# These data structures contain the details of decoding the ASCII code in the structures.
wizard_tower_chars = {
    "#": Tile.STONE_BRICKS,
    "+": Tile.WOOD_DOOR,
    "=": Tile.WOOD_PLANKS,
    "<": Tile.WOOD_STAIRS,
    "^": Tile.WOOD_RAMP,
}

dungeon_chars = {
    "#": Tile.STONE_BRICKS,
    "+": Tile.WOOD_DOOR,
    "^": Tile.STONE_STAIRS,
    "0": Tile.STONE_PILLAR,
    "_": Tile.ALTAR,
}


def spawn_structure(structure: list[str], array: WorldArrayType, pos: tuple[int, int, int], key: dict[str, Tile]):
    """Utility function for pasting structures into the world."""
    x, y, z = pos
    for layer in structure:
        for char in layer[1:]:  # Account for leading newline in each layer.
            if char == "\n":  # Next row, shift y down by one.
                x = pos[0]
                y += 1
                continue
            if char != " ":  # Only replace blocks if it isn't the space character.
                # This means structures don't have to be rectangular shaped.
                array[x][y][z] = key.get(char, Tile.AIR)
            x += 1
        x, y = pos[0], pos[1]
        z += 1


def noise_array(size: Sequence[int], scale: float = 1.0, offset: tuple[int, int] = (0, 0)) -> list[list[float]]:
    """Generate a 2D array of noise values with the given scaling and offset applied."""
    def get_point(x: int, y: int) -> float:
        return opensimplex.noise2(x * scale + offset[0], y * scale + offset[1])
    return array2d(size, get_point)


def get_random_offset(size: Sequence[int], rng: random.Random) -> tuple[int, int]:
    """Utility function for generating offsets for noise layers.

    Offsets are needed to produce different layers of noise from the same coordinates on the same seed.
    """
    return rng.randint(size[0], size[0] * 10), rng.randint(size[1], size[1] * 10)


def get_wizard_tower_spawn_pos(sea_level: int, array: WorldArrayType, rng) -> tuple[int, int, int]:
    """Utility function for getting spawn coordinates for structures."""
    width, height = len(array), len(array[0])
    attempts = 100  # Limit to 100 attempts.
    while attempts > 0:
        x, y = rng.randrange(width - 10), rng.randrange(height - 10)
        if array[x][y][sea_level] is not Tile.WATER and array[x][y][sea_level + 2] is Tile.AIR:
            return x, y, sea_level + 1
        attempts -= 1
    return 0, 0, sea_level + 1  # When in doubt, fall back to (0, 0).


def get_dungeon_spawn_pos(sea_level: int, array: WorldArrayType, rng) -> tuple[int, int, int]:
    """Utility function for getting spawn coordinates for structures."""
    width, height = len(array), len(array[0])
    attempts = 100  # Limit to 100 attempts.
    while attempts > 0:
        x, y = rng.randint(20, width - 10), rng.randrange(height - 10)
        if array[x + 4][y + 5][sea_level] is not Tile.WATER and array[x + 4][y + 5][sea_level + 1] is Tile.AIR:
            return x, y, sea_level - 3
        attempts -= 1
    return 0, 0, sea_level - 3  # When in doubt, fall back to (0, 0).


def get_biome_tile(alt, hum) -> Tile:
    if hum > 0:
        if alt < 0:
            return Tile.SWAMP_GRASS
        if alt < 0.4:
            return Tile.GRASS
        return Tile.TREE
    if alt < 0:
        return Tile.SAND
    return Tile.STONE


def ocean_biome(z: int, altitude: float, sea_level: int) -> Tile:
    if z > sea_level:
        return Tile.AIR
    if z < sea_level:
        return Tile.SAND
    if altitude < -0.7:
        return Tile.SAND
    if altitude > -0.3:
        return Tile.SAND
    return Tile.WATER


def mountain_biome(z: int, altitude: float, humidity: float, sea_level: int) -> Tile:
    relative_height = z - sea_level
    if relative_height <= 0:
        return Tile.STONE if humidity < 0.5 else Tile.GRASS
    if altitude - relative_height * 0.05 < 0.4:
        return Tile.AIR
    if altitude - relative_height * 0.05 < 0.5:
        return Tile.STONE_SLOPE if humidity < 0.5 else Tile.GRASS_SLOPE
    return Tile.STONE


def generate_world(size: tuple[int, int, int], seed: int):
    """Create the entire world array.

    This function is a generator that yields status strings to tell the user what is happening.
    """
    # Seed the random generators.
    rng = random.Random(seed)
    opensimplex.seed(seed)

    # Sea level will be at 7, this can be adjusted.
    sea_level = 7

    # Create the noise arrays.
    yield "Generating altitude..."
    altitude_array = noise_array(size, 0.05)
    yield "Generating humidity..."
    humidity_array = noise_array(size, 0.05, get_random_offset(size, rng))

    # def get_cell2(x: int, y: int, z: int) -> Tile:
    #     altitude = altitude_array[x][y]
    #     humidity = humidity_array[x][y]
    #     if z < sea_level - 1:
    #         return Tile.STONE
    #     if z > sea_level + 2:
    #         return Tile.AIR
    #     if altitude < -0.2:
    #         return ocean_biome(z, altitude, sea_level)
    #     if altitude > 0.4:
    #         return mountain_biome(z, altitude, humidity, sea_level)
    #     return Tile.GRASS

    def get_cell(x: int, y: int, z: int) -> Tile:
        """This function is called once for each coordinate and decides what each block is."""
        altitude = altitude_array[x][y]
        humidity = humidity_array[x][y]
        land_level = sea_level + round(altitude * 2)
        biome_tile = Tile.GRASS if humidity > -0.2 else Tile.SAND
        if altitude < -0.1:
            biome_tile = Tile.SAND
        if altitude > 0.5:
            biome_tile = Tile.STONE
        if 0.25 < altitude < 0.3:
            biome_tile = Tile.GRASS_SLOPE if humidity > -0.2 else Tile.SAND_SLOPE
        if z < land_level:
            return Tile.STONE
        if z == land_level:
            if z < sea_level:
                return Tile.SAND
            return biome_tile
        if z > land_level:
            if z < sea_level + 1:
                return Tile.WATER
            if z == land_level + 1 and rng.random() < 0.2 and biome_tile is Tile.GRASS:
                if humidity > 0.3:
                    return Tile.TREE
                return Tile.RED_FLOWER if rng.random() < 0.5 else Tile.YELLOW_FLOWER
            if z == land_level + 1 and altitude > 0.6:
                if altitude < 0.625:
                    return Tile.STONE_SLOPE
                return Tile.STONE
            return Tile.AIR

    # Create the main 3D array of blocks.
    yield "Building terrain..."
    array = array3d(size, get_cell)

    # Spawn a wizard tower and a basic dungeon entrance.
    yield "Spawning structures..."
    wizard_tower_spawn_pos = get_wizard_tower_spawn_pos(sea_level, array, rng)
    spawn_structure(structures.wizard_tower, array, wizard_tower_spawn_pos, wizard_tower_chars)
    dungeon_spawn_pos = get_dungeon_spawn_pos(sea_level, array, rng)
    spawn_structure(structures.dungeon_entrance, array, dungeon_spawn_pos, dungeon_chars)
    altar_room_pos = dungeon_spawn_pos[0] - 15, dungeon_spawn_pos[1], dungeon_spawn_pos[2] - 1
    spawn_structure(structures.dungeon_altar_room, array, altar_room_pos, dungeon_chars)

    yield array
