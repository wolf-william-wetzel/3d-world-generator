#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
from pathlib import Path
import random
import time

import pygame as pg

import utils
from generation import generate_world, get_tile
from colors import Color, Image, image_scheme
from tiles import Tile, prop_tiles, tile_graphics, passable_tiles, slope_tiles


SCREEN_SIZE = pg.Vector2(800, 600)
WORLD_SIZE = (64, 64, 16)

# PATH_TO_FONT, FONT_SIZE_IN_PIXELS, SCHEME_KEY
font_info = (
    ("cp437_20x20.png", (20, 20), "cp437"),
    ("kenney_16x16.png", (16, 16), "kenney"),
)


def main() -> None:
    # Initialize pygame and set up key repeat.
    pg.init()
    pg.key.set_repeat(500, 100)
    # Load in the music and play it on an infinite loop.
    pg.mixer.music.load("woods.wav")
    pg.mixer.music.play(-1)
    # Set up the window.
    pg.display.set_caption("3D Generation Test")
    fullscreen = False
    screen = utils.toggle_fullscreen(SCREEN_SIZE, fullscreen)
    clock = pg.time.Clock()
    # Get a default font for debug info.
    font = pg.Font(size=30)

    # Get the font info and set up the tile loader.
    current_font = 1
    tile_loader = utils.TileLoader(Path(font_info[current_font][0]), font_info[current_font][1])
    current_scheme = font_info[current_font][2]

    # The starting seed is always the same for testing purposes.
    seed = 1234
    seed_surf = font.render(f"Seed: {seed}", True, Color.WHITE, Color.BLACK)
    gen_time = time.monotonic_ns()

    def display_world_generation() -> list[list[list[Tile]]]:
        """Display the world generation on the screen as it happens."""
        line_counter = -2
        for item in generate_world(WORLD_SIZE, seed):
            if not isinstance(item, str):
                return item
            pg.event.pump()  # Add quit event handling back in if world gen gets really long.
            text_surf = font.render(item, True, Color.WHITE, Color.BLACK)
            screen.blit(text_surf, pg.Vector2(screen.size) // 2 - text_surf.get_rect().center + (0, line_counter * 25))
            pg.display.flip()
            line_counter += 1

    # Generate the world and remember how long it took to generate.
    world = display_world_generation()
    gen_time = time.monotonic_ns() - gen_time

    # Get a spawn point for the player.
    player_pos = pg.Vector3()
    random.seed(seed)
    attempts = 100  # 100 attempts until we give up and place the player at (0, 0, 0).
    while attempts > 0:
        x, y = random.randrange(len(world)), random.randrange(len(world[0]))
        if world[x][y][7] is not Tile.WATER and world[x][y][8] in (Tile.AIR, Tile.RED_FLOWER, Tile.YELLOW_FLOWER):
            player_pos = pg.Vector3(x, y, 8)
            break
        attempts -= 1

    # Calculate the camera center, and set the view variables.
    # z_level should be part of the camera.
    camera_center = pg.Vector2(screen.size).elementwise() / tile_loader.tile_size // 2  # noqa
    camera = player_pos.xy - camera_center
    z_level = int(player_pos.z)

    def get_scheme_image(image: Image, color: tuple[int, int, int]) -> pg.Surface:
        """Utility function for getting a font-agnostic image."""
        return tile_loader.get_tile(image_scheme[current_scheme][image], color)

    def get_player_image() -> pg.Surface:
        """The player needs an opaque background, or it is too hard to see it."""
        return tile_loader.get_tile(image_scheme[current_scheme][Image.PLAYER], Color.WHITE, None)

    def get_tile_image() -> pg.Surface | None:
        """This function is called in a drawing loop in the main loop. x and y are the virtual coordinates."""
        # Convert virtual coordinates into world coordinates with the camera.
        world_x, world_y = int(x + camera.x), int(y + camera.y)
        if (tile := utils.in_bounds3d((world_x, world_y, z_level), world)) is False:
            return  # Don't draw any out of bounds tiles.
        # Draw the tile to the screen.
        if tile is not Tile.AIR:
            # These are the side perspective tiles.
            screen.blit(utils.make_color_image(tile_loader.tile_size, tile_graphics[tile][2]),
                        (x * tile_loader.tile_size[0], y * tile_loader.tile_size[1]))
            return get_scheme_image(tile_graphics[tile][0], tile_graphics[tile][1])
        if z_level > 0:
            # These are the top perspective tiles.
            tile = world[world_x][world_y][z_level - 1]
            if tile is not Tile.AIR:
                return get_scheme_image(tile_graphics[tile][3], tile_graphics[tile][4])
        if z_level > 1:
            # These are the below perspective tiles.
            tile = world[world_x][world_y][z_level - 2]
            if tile not in prop_tiles:  # Props look as though they are down a z-level anyway.
                return get_scheme_image(tile_graphics[tile][3], Color.darken(tile_graphics[tile][4]))

    def move_player(direction: tuple[int, int, int]):
        """Move the player in a direction.

        Movement is not allowed into solid blocks or open air.
        Up and down movement on slope-like tiles is handled here.
        """
        # Check for blocked movement.
        if (try_tile := get_tile(world, player_pos.xyz + direction)) in passable_tiles:
            # Detect pits.
            if try_tile is Tile.AIR:
                # Go downstairs.
                if get_tile(world, player_pos.xyz + direction + (0, 0, -1)) in slope_tiles:
                    player_pos.xyz += direction
                    player_pos.xyz += (0, 0, -1)
                    return
                # Don't fall in pits.
                if get_tile(world, player_pos.xyz + direction + (0, 0, -1)) in passable_tiles:
                    return
            # Occupy the vacant tile.
            player_pos.xyz += direction
        # Check for going upstairs.
        elif get_tile(world, player_pos) in slope_tiles:
            # If there is air above the player and the tile they will be on is passable, it is a legal move.
            if (get_tile(world, player_pos.xyz + (0, 0, 1)) is Tile.AIR and
                    get_tile(world, player_pos.xyz + direction + (0, 0, 1)) in passable_tiles):
                player_pos.xyz += direction
                player_pos.xyz += (0, 0, 1)

    # Enter the main game loop.
    while True:
        for event in pg.event.get():
            # Handle quit events.
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_F4:  # Toggle full screen.
                    fullscreen = not fullscreen
                    screen = utils.toggle_fullscreen(SCREEN_SIZE, fullscreen)
                    camera_center = pg.Vector2(screen.size).elementwise() / tile_loader.tile_size // 2  # noqa
                    camera = player_pos.xy - camera_center
                if event.key == pg.K_TAB:  # Cycle through tile sets.
                    current_font += 1
                    current_font %= len(font_info)
                    tile_loader = utils.TileLoader(Path(font_info[current_font][0]), font_info[current_font][1])
                    current_scheme = font_info[current_font][2]
                    camera_center = pg.Vector2(screen.size).elementwise() / tile_loader.tile_size // 2  # noqa
                    camera = player_pos.xy - camera_center
                if event.key == pg.K_SPACE:  # Generate a new world.
                    # There is a lot of duplicated code here that needs fixing.
                    seed = random.getrandbits(64)
                    seed_surf = font.render(f"Seed: {seed}", True, Color.WHITE, Color.BLACK)
                    gen_time = time.monotonic_ns()
                    world = display_world_generation()
                    gen_time = time.monotonic_ns() - gen_time

                    player_pos = pg.Vector3()
                    random.seed(seed)
                    attempts = 100
                    while attempts > 0:
                        x, y = random.randrange(len(world)), random.randrange(len(world[0]))
                        if world[x][y][7] is not Tile.WATER and world[x][y][8] in (
                           Tile.AIR, Tile.RED_FLOWER, Tile.YELLOW_FLOWER):
                            player_pos = pg.Vector3(x, y, 8)
                            break
                        attempts -= 1

                    camera = player_pos.xy - camera_center
                    z_level = int(player_pos.z)
                # Move the player.
                if event.key == pg.K_w:
                    move_player((0, -1, 0))
                    camera = player_pos.xy - camera_center
                    z_level = int(player_pos.z)
                if event.key == pg.K_s:
                    move_player((0, 1, 0))
                    camera = player_pos.xy - camera_center
                    z_level = int(player_pos.z)
                if event.key == pg.K_a:
                    move_player((-1, 0, 0))
                    camera = player_pos.xy - camera_center
                    z_level = int(player_pos.z)
                if event.key == pg.K_d:
                    move_player((1, 0, 0))
                    camera = player_pos.xy - camera_center
                    z_level = int(player_pos.z)
                # Move the camera.
                if event.key == pg.K_UP:
                    camera.y -= 1
                if event.key == pg.K_DOWN:
                    camera.y += 1
                if event.key == pg.K_LEFT:
                    camera.x -= 1
                if event.key == pg.K_RIGHT:
                    camera.x += 1
                # Move the camera up and down.
                if event.key == pg.K_EQUALS:
                    z_level += 1
                    z_level = min(WORLD_SIZE[2] - 1, z_level)
                if event.key == pg.K_MINUS:
                    z_level -= 1
                    z_level = max(0, z_level)

        clock.tick()  # Detect fps.

        screen.fill(Color.BLACK)  # Clear the screen for drawing.

        # Draw the tiles.
        for x in range(screen.width // tile_loader.tile_size[0]):
            for y in range(screen.height // tile_loader.tile_size[1]):
                if tile_image := get_tile_image():
                    screen.blit(tile_image, (x * tile_loader.tile_size[0], y * tile_loader.tile_size[1]))

        # Draw the player.
        if z_level == int(player_pos.z):
            screen.blit(get_player_image(), (player_pos.xy - camera).elementwise() * tile_loader.tile_size)  # noqa

        # Display the debug info and flip the screen.
        screen.blit(seed_surf, (0, 0))
        fps_surf = font.render(f"Gen: {gen_time // 1000000}ms\nFPS: {clock.get_fps():.2f}\nCamera Z: {z_level}"
                               f"\nPlayer X: {int(player_pos.x)}\nPlayer Y: {int(player_pos.y)}"
                               f"\nPlayer Z: {int(player_pos.z)}",
                               True, Color.WHITE, Color.BLACK)
        screen.blit(fps_surf, (0, seed_surf.height))
        pg.display.flip()


if __name__ == '__main__':
    main()
