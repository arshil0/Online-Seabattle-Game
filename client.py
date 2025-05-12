import socket
import sys
from seaBattle import SeaBattleGame

def join_server(server_ipv6='::1', port=60660):
    #try to join a server
    client_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    client_socket.connect((server_ipv6, port))
    print(f"[CLIENT] Connected to [{server_ipv6}]:{port}")

    print("\nYou have succesfully joined a server!")
    print("Let's start by putting the ship locations (make sure that your opponent doesn't know their locations.) \n")
    my_board = SeaBattleGame()

    #the enemy board will be an empty board, to visualize the opponent's board and what tiles were shot
    enemy_board = SeaBattleGame()

    #place all the ships from the player's input
    my_board.take_ship_placement_input(5, "Carrier")
    my_board.take_ship_placement_input(4, "Battleship")
    my_board.take_ship_placement_input(3, "Cruiser")
    my_board.take_ship_placement_input(3, "Submarine")
    my_board.take_ship_placement_input(2, "Destroyer")

    print("This is your board")
    print(my_board)

    """
    #for testing:
    my_board.place_battleship(2,4)
    my_board.place_cruisesr(5, 5)
    my_board.place_carrier(1, 0)
    """

    print("This is your board")
    print(my_board)

    #everything is handled in the play function
    my_board.play(enemy_board, client_socket)

#(try to) get the IPv6 and port from the terminal
IPv6 = "::1"
port = 60660
if len(sys.argv) > 1:
    IPv6 = sys.argv[1]
if len(sys.argv) > 2:
    port = sys.argv[2]

join_server(IPv6, port)
