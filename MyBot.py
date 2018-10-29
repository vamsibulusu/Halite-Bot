#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction

from hlt.positionals import Position

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()
# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")



# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
no_of_ships = 0
""" <<<Game Loop>>> """

if(game.game_map.width == 32):
    max_turns = 400
if(game.game_map.width == 40):
    max_turns = 425
if(game.game_map.width == 48):
    max_turns = 450
if(game.game_map.width == 56):
    max_turns = 475
if(game.game_map.width == 64):
    max_turns = 500

x_cor = 0 
y_cor = 0
top_halite = []
while (x_cor < game.game_map.width):
    while (y_cor < game.game_map.width):
        cur_position = Position(x_cor, y_cor)
        top_halite.append([cur_position, 0, game.game_map[cur_position].halite_amount])
        x_cor = x_cor + 1
        y_cor = y_cor + 1
        

top_halite.sort(key=lambda x: x[2], reverse = True)

for xx in top_halite:
    del xx[2]    






while True:
    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map


    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    turn = 0
    for ship in me.get_ships():
        foo = 1
        logging.info(ship.id)
        logging.info(ship.position)
        check = game_map.calculate_distance(ship.position, me.shipyard.position)
        if (game.turn_number > (max_turns - 30)) and check == 1:
            list_of_moves = game_map.get_unsafe_moves(ship.position, me.shipyard.position)
            command_queue.append(ship.move(list_of_moves[0]))
                
        elif (game.turn_number > (max_turns - 30)):
            list_of_moves = game_map.naive_navigate(ship, me.shipyard.position)
            command_queue.append(ship.move(list_of_moves))
                           
            
            
        elif ship.halite_amount > 950 or (ship.halite_amount > 600 and game_map.calculate_distance(ship.position, me.shipyard.position) < 5):
            list_of_moves = game_map.naive_navigate(ship, me.shipyard.position)
            if list_of_moves == Direction.Still:
                if game_map[ship.position.directional_offset(Direction.West)].is_empty:
                    list_of_moves = Direction.West
                elif game_map[ship.position.directional_offset(Direction.East)].is_empty:
                    list_of_moves = Direction.East
                elif game_map[ship.position.directional_offset(Direction.South)].is_empty:
                    list_of_moves = Direction.South
                elif game_map[ship.position.directional_offset(Direction.North)].is_empty:
                    list_of_moves = Direction.North
            command_queue.append(ship.move(list_of_moves))
            game_map[ship.position.directional_offset(list_of_moves)].mark_unsafe(ship)
        # For each of your ships, move randomly if the ship is on a low halite location or the ship is full.
        #   Else, collect halite.
        elif (foo % 2 == 0):
            for posi in top_halite:
                if (posi[1] == 0):
                    list_of_moves = game_map.naive_navigate(ship, posi[0])
                    posi[1] = 1
                    break
            command_queue.append(ship.move(list_of_moves))
            
        
        elif game_map[ship.position].halite_amount < 50:
            maxhal = 0
            if game_map[ship.position.directional_offset(Direction.West)].halite_amount > maxhal and game_map[ship.position.directional_offset(Direction.West)].is_empty:
                list_of_moves = Direction.West
                maxhal = game_map[ship.position.directional_offset(Direction.West)].halite_amount
            if game_map[ship.position.directional_offset(Direction.East)].halite_amount > maxhal and game_map[ship.position.directional_offset(Direction.East)].is_empty:
                list_of_moves = Direction.East
                maxhal = game_map[ship.position.directional_offset(Direction.East)].halite_amount
            if game_map[ship.position.directional_offset(Direction.South)].halite_amount>maxhal and game_map[ship.position.directional_offset(Direction.South)].is_empty:
                list_of_moves = Direction.South
                maxhal = game_map[ship.position.directional_offset(Direction.South)].halite_amount
            if game_map[ship.position.directional_offset(Direction.North)].halite_amount>maxhal and game_map[ship.position.directional_offset(Direction.North)].is_empty:
                list_of_moves = Direction.North
                maxhal = game_map[ship.position.directional_offset(Direction.North)].halite_amount
            if maxhal < 50 and ship.halite_amount > 800:
                list_of_moves = game_map.naive_navigate(ship, me.shipyard.position)
                if list_of_moves == Direction.Still:
                    if game_map[ship.position.directional_offset(Direction.West)].is_empty:
                        list_of_moves = Direction.West
                    elif game_map[ship.position.directional_offset(Direction.East)].is_empty:
                        list_of_moves = Direction.East
                    elif game_map[ship.position.directional_offset(Direction.South)].is_empty:
                        list_of_moves = Direction.South
                    elif game_map[ship.position.directional_offset(Direction.North)].is_empty:
                        list_of_moves = Direction.North
            if maxhal == 0:
                command_queue.append(ship.stay_still())
            else :
                command_queue.append(ship.move(list_of_moves))
                game_map[ship.position.directional_offset(list_of_moves)].mark_unsafe(ship)
        else:
            command_queue.append(ship.stay_still())
    turn = turn + 1
    # If the game is in the first 200 turns and you have enough halite, spawn a ship.
    # Don't spawn a ship if you currently have a ship at port, though - the ships will collide.
    if game.turn_number <= 200 and no_of_ships < 0.5 * game_map.width and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())
        no_of_ships = no_of_ships + 1

    # Send your moves back to the game environment, ending this turn.
    game.end_turn(command_queue)
