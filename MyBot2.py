#!/usr/bin/env python3
# Python 3.6

# Import the Halite SDK, which will let you interact with the game.
import hlt

# This library contains constant values.
from hlt import constants

# This library contains direction metadata to better interface with the game.
from hlt.positionals import Direction, Position

# This library allows you to generate random numbers.
import random

# Logging allows you to save messages for yourself. This is required because the regular STDOUT
#   (print statements) are reserved for the engine-bot communication.
import logging

""" <<<Game Begin>>> """

# This game object contains the initial game state.
game = hlt.Game()

dropoff_exist = 0
dropoff_data = []

xx = 0 
yy = 0
for xx in range (game.game_map.width):
    for yy in range (game.game_map.width):
        sum = 0
        for tempx in range (-3,3):
            for tempy in range (-3,3):
                sum = sum + game.game_map[Position(xx+tempx, yy+tempy)].halite_amount
        dropoff_data.append([xx,yy,sum])
dropoff_data.sort(key=lambda x: x[2], reverse= True)
logging.info(dropoff_data)
dropoff_dis = []
dropoff_dis.append([dropoff_data[0][0],dropoff_data[0][1],(abs(dropoff_data[0][0]-game.me.shipyard.position.x)+abs(dropoff_data[0][1]-game.me.shipyard.position.y))])
dropoff_dis.append([dropoff_data[1][0],dropoff_data[1][1],(abs(dropoff_data[1][0]-game.me.shipyard.position.x)+abs(dropoff_data[1][1]-game.me.shipyard.position.y))])
dropoff_dis.append([dropoff_data[2][0],dropoff_data[2][1],(abs(dropoff_data[2][0]-game.me.shipyard.position.x)+abs(dropoff_data[2][1]-game.me.shipyard.position.y))])
dropoff_dis.append([dropoff_data[3][0],dropoff_data[3][1],(abs(dropoff_data[3][0]-game.me.shipyard.position.x)+abs(dropoff_data[3][1]-game.me.shipyard.position.y))])
dropoff_dis.append([dropoff_data[4][0],dropoff_data[4][1],(abs(dropoff_data[4][0]-game.me.shipyard.position.x)+abs(dropoff_data[4][1]-game.me.shipyard.position.y))])
dropoff_dis.sort(key=lambda x: x[2], reverse=True)
logging.info(dropoff_dis)
dropoff_position = Position(dropoff_dis[0][0],dropoff_dis[0][1])



# At this point "game" variable is populated with initial map data.
# This is a good place to do computationally expensive start-up pre-processing.
# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("MyPythonBot")

# Now that your bot is initialized, save a message to yourself in the log file with some important information.
#   Here, you log here your id, which you can always fetch from the game object by using my_id.
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
no_of_ships = 0
dropoff_reach = 10
make_dropoff = 0
""" <<<Game Loop>>> """
while True:





    drop_save = len(game.me.get_dropoffs())

    if game.me.halite_amount > 0  and make_dropoff == 0 and game.turn_number > (max_turns/4) :
        for xx in range (game.game_map.width):
            for yy in range (game.game_map.width):
                sum = 0
                for tempx in range (-3,3):
                    for tempy in range (-3,3):
                        sum = sum + game.game_map[Position(xx+tempx, yy+tempy)].halite_amount
                dropoff_data.append([xx,yy,sum])
        dropoff_data.sort(key=lambda x: x[2], reverse= True)
        dropoff_dis = []
        for x in range(5):
            tx=dropoff_data[x][0]
            ty=dropoff_data[x][1]
            td=abs(dropoff_data[0][0]-game.me.shipyard.position.x)+abs(dropoff_data[0][1]-game.me.shipyard.position.y)
            dropoff_dis.append([tx,ty,td])
        dropoff_dis.sort(key=lambda x: x[2], reverse=True)
        logging.info(len(dropoff_data))
        dropoff_position = Position(dropoff_dis[0][0],dropoff_dis[0][1])
        dropoff_ship = me.get_ships()[-1].id
        make_dropoff = 1





    # This loop handles each turn of the game. The game object changes every turn, and you refresh that state by
    #   running update_frame().
    game.update_frame()
    # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    if(game_map.width == 32):
        max_turns = 400
    if(game_map.width == 40):
        max_turns = 425
    if(game_map.width == 48):
        max_turns = 450
    if(game_map.width == 56):
        max_turns = 475
    if(game_map.width == 64):
        max_turns = 500

    # A command queue holds all the commands you will run this turn. You build this list up and submit it at the
    #   end of the turn.
    command_queue = []
    turn = 0
    ship_odd = 0
    dropoff_reach = dropoff_reach - 1
    for ship in me.get_ships():
        ship_odd = ship_odd + 1
        check_dropoff = 128
        if len(me.get_dropoffs()) > 0:
            check_dropoff = game_map.calculate_distance(ship.position, me.get_dropoffs()[0].position)
        check_shipyard = game_map.calculate_distance(ship.position, me.shipyard.position)
        if check_dropoff < check_shipyard:
            to_drop = me.get_dropoffs()[0].position
        else:
            to_drop = me.shipyard.position

        

        if make_dropoff == 1 and ship.id == dropoff_ship and dropoff_exist ==0:
            if game_map.calculate_distance(ship.position, dropoff_position) == 0:
                if me.halite_amount > 5000 - game_map[ship.position].halite_amount:
                    command_queue.append(ship.make_dropoff())
                    dropoff_position = ship.position
                    dropoff_exist = 1
                    logging.info("here3 {}.".format(ship.id))  
                    wait = 0
                else :
                    wait = 1
                    command_queue.append(ship.stay_still())
                    logging.info("here4 {}.".format(ship.id))  
            else:
                list_of_moves = game_map.naive_navigate(ship,dropoff_position)
                command_queue.append(ship.move(list_of_moves))
                logging.info("here5 {}.".format(ship.id))

        elif len(me.get_dropoffs()) > 0 and dropoff_reach > 0 and ship_odd % 1 == 0:
              logging.info("dropoffffffffffffffffffffffffffffffffffffffffffffffffff")
              list_of_moves = game_map.naive_navigate(ship,dropoff_position)
              command_queue.append(ship.move(list_of_moves))
              logging.info("here1 {}.".format(ship.id))


        elif (game.turn_number > (max_turns - 30)) and check_shipyard == 1:
            list_of_moves = game_map.get_unsafe_moves(ship.position, to_drop)
            command_queue.append(ship.move(list_of_moves[0]))
                
        elif (game.turn_number > (max_turns - 30)):
            list_of_moves = game_map.naive_navigate(ship, to_drop)
            command_queue.append(ship.move(list_of_moves))
            
        
        
        
        elif ship.halite_amount > 950 or (ship.halite_amount > 200 and game_map.calculate_distance(ship.position, to_drop) < 3):
            list_of_moves = game_map.naive_navigate(ship, to_drop)
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
                list_of_moves = game_map.naive_navigate(ship, to_drop)
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
