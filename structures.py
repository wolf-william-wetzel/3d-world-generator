# This file holds structure data for the game.
# Blocks are encoded as ASCII symbols.
# Each element of the array represents a 2D plane, starting from z level 0.
# Each element is a 1D string, with newlines marking the end of a row of blocks.
# After each newline, the y value shifts down by one.
wizard_tower = [
    """
  ###
 #===#
<#===#
 #===#
  ###
    """,
    """
  ###
 #..<#
 +..=#
 #..<#
  ###
    """,
    """
  ###
 #==.#
 #==<#
 #==.#
  ###
    """,
    """
  ###
 #...#
 #<..#
 #...#
  ###
    """,
    """
  ===
 =====
 <.===
 =====
  ===
    """,
    """
  ^^^
 ^===^
 .===^
 ^===^
  ^^^
    """,
    """

  ^^^
  ^=^
  ^^^
    """,
    """


   ^
    """,
]

dungeon_entrance = [
    """
#######
#######
#######
#######
#######
#######
#######
    """,
    """
###+###
#.....#
#.....#
+.....+
#.....#
#.^##.#
#######
    """,
    """
#######
#######
#######
#######
#######
##.^###
#######
    """,
    """





   .^
    """,
]

dungeon_altar_room = [
    """
  ########
 #########
##########
##########
##########
 #########
  ########
    """,
    """
  ##############
 ##.0.0.0#######
##......^#######
#_......^#######
##......^#######
 ##.0.0.0#######
  ##############
    """,
    """
  ##############
 ##.0.0.0.0.0.0#
##.............#
#..............+
##.............#
 ##.0.0.0.0.0.0#
  ##############
    """,
    """
  ##############
 ###############
################
################
################
 ###############
  ##############
    """,
]
