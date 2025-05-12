import socket
import sys
from seaBattle import SeaBattleGame

def start_server(ipv6_host='::1', port=60660):
    #create the server and listen for a connection
    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    server_socket.bind((ipv6_host, port))
    server_socket.listen(1)
    print(f"[SERVER] Listening on [{ipv6_host}]:{port}")

    #accept a client connection
    conn, addr = server_socket.accept()
    print(f"[SERVER] Connected by {addr}")

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
    my_board.place_battleship(0,2, False)
    print("This is your board")
    print(my_board)

    """

    #handles the game logic
    my_board.play(enemy_board, conn, True)

    #when the game is over, close the server
    server_socket.close()

#(try to) get the IPv6 and port from the terminal
IPv6 = "::1"
port = 60660
if len(sys.argv) > 1:
    IPv6 = sys.argv[1]
if len(sys.argv) > 2:
    port = sys.argv[2]

start_server(IPv6, port)
