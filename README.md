# Overview

This is more of a demonstration than a full game. The world is a randomly generated 3D grid of voxels.
The visuals are from a top-down perspective, so you see the world one 2D slice at a time, like Dwarf Fortress.
The player character can be navigated around with WASD, and automatically descends stairs and slopes it comes across.
When standing on an upwards staircase or slope, you can walk into a wall to ascend the voxel and stand on top.
This won't work if there is a block above you or on top of the block you attempt to climb.
Use the MINUS and EQUALS keys on the keyboard to shift the 3D view down or up one z-level, respectively.
ESCAPE quits the game and F4 toggles full screen. Press TAB to change tile sets and SPACE to generate a new world.
The arrow keys will shift the camera around, so you can view the full map if it is off the screen.
There is no end goal and only a few structures and environmental features to discover.
There are no hostile entities or a way to lose or die.

I wrote this software to gain experience writing procedurally generated content.
I had never written a 3D world generator before and really wanted to try it out.

[Software Demo Video](https://youtu.be/Ol91o4UDOEg)

# Development Environment

I used JetBrains Pycharm as my IDE for this project.

I used Python version 3.12.2 for this project.
I used Pygame Community Edition version 2.5.0 for sounds and graphics.
I used opensimplex version 0.4.5.1 for simplex noise generation.

# Useful Websites

* [Pygame CE Documentation](https://pyga.me/docs/)
* [opensimplex on PyPI](https://pypi.org/project/opensimplex/)

# Future Work

* More advanced world generation, with more biomes and cave generation.
* 3D field of view algorithm for player vision and map memory.
* Better system for generating structures.