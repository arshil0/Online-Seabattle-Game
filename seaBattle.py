import subprocess
#this allows us to print colored text on the console (at least for me)
subprocess.call('', shell=True)

#this array will keep an array of positions for each ship, and its size
#the size will shrink as the ship gets hit, if it reaches 0, the ship is gone, send that signal to the opponent
list_of_ships = []

board_size = 10

class SeaBattleGame:
    def __init__(self):
        self.board = [["o"] * board_size for i in range(board_size)]

    #print the board in a nice format
    def __str__(self):
        result = "\t"
        for row in range(-1, board_size):
            if row == -1:
                result += "  "
                for i in range(board_size):
                    result += str(i) + " "
            else:
                for column in range(board_size):
                    if(column == 0):
                        result += str(row) + " "

                    tile = self.board[row][column]

                    #if it's a regular tile, print it out regularly (white)
                    if tile == "o":
                        result +=  tile + " "
                    #if the tile has been attacked before (print it red)
                    elif tile == "X":
                        result += "\033[31m" + tile + "\033[0m "
                    #if I hit the opponent's ship, but still not sure about the ship formation (print it yellow)
                    elif tile == "?":
                        result += "\033[36m" + tile + "\033[0m "
                    #otheriwse, if it's an unattacked ship part, print it green
                    else:
                        result += "\033[32m" + tile + "\033[0m "
            result += "\n\t"
        return result
    
    #this is the ship with length 5
    def place_carrier(self, posX, posY, vertical = True):
        return self.place_ship(5, posX, posY, vertical)

    #functions for placing the rest of the ships...
    def place_battleship(self, posX, posY, vertical = True):
        return self.place_ship(4, posX, posY, vertical)

    def place_cruisesr(self, posX, posY, vertical = True):
        return self.place_ship(3, posX, posY, vertical)

    def place_submarine(self, posX, posY, vertical = True):
        return self.place_ship(3, posX, posY, vertical)

    def place_destroyer(self, posX, posY, vertical = True):
        return self.place_ship(2, posX, posY, vertical)

    #handle ship placement feedback and taking input
    def take_ship_placement_input(self, ship_size, ship_name):
        ship_vertical = True
        while True:
            print("[IMPORTANT]: You can always type 'flip' to flip the ship to be vertical or horizontal \n")
            print("This is how the board looks like:")
            print(self)
            self.print_ship_blueprint(ship_size, ship_name, ship_vertical)
            x = ""
            y = ""
            try:
                if ship_vertical:
                    x = input("[INPUT]: provide the x coordinate of where you want to place the TOP of the ship: ")
                    if x.lower() == "flip":
                        ship_vertical = False
                        continue

                    y = input("[INPUT]: provide the y coordinate of where you want to place the TOP of the ship: ")
                    if y.lower() == "flip":
                        ship_vertical = False
                        continue
                else:
                    x = input("[INPUT]: provide the x coordinate of where you want to place the LEFT of the ship: ")
                    if x.lower() == "flip":
                        ship_vertical = True
                        continue

                    y = input("[INPUT]: provide the y coordinate of where you want to place the LEFT of the ship: ")
                    if y.lower() == "flip":
                        ship_vertical = False
                        continue
                
                x = int(x)
                y = int(y)
            except ValueError:
                continue

            print("\n")

            #try to place the ship at the given coordinates, if it was succesfull, then continue
            if ship_name.lower() == "carrier":
                if(self.place_carrier(x, y, ship_vertical)):
                    break
            elif ship_name.lower() == "battleship":
                if(self.place_battleship(x, y, ship_vertical)):
                    break
            elif ship_name.lower() == "cruiser":
                if(self.place_cruisesr(x, y, ship_vertical)):
                    break
            elif ship_name.lower() == "submarine":
                if(self.place_submarine(x, y, ship_vertical)):
                    break
            elif ship_name.lower() == "destroyer":
                if(self.place_destroyer(x, y, ship_vertical)):
                    break

    #print the ship in the console to showcase its size and rotation
    def print_ship_blueprint(self, ship_size, ship_name, vertical = True):
        print(f"Currently placing the {ship_name}:")
        if vertical:
            for i in range(ship_size):
                if i == 0:
                    print("^")
                elif i == ship_size - 1:
                    print("v")
                else:
                    print("|")
        else:
            for i in range(ship_size):
                if i == 0:
                    print("<", end=" ")
                elif i == ship_size - 1:
                    print(">")
                else:
                    print("-", end=" ")

    #try to place a ship, given its size, if placement was succesful, returns True, otherwise returns False (another ship already is occupying the space or the ship would be outside of the board)
    def place_ship(self, ship_size, posX, posY, vertical = True, force_place = False):
        #check to see if any of the given positions are negative
        if posX < 0 or posY < 0:
            print("[WRONG INPUT]: You can't put a ship on a negative coordinate")
            return False
        #check to see if the ship will be inside of the board
        if posX >= board_size or posY >= board_size:
            print("[WRONG INPUT]: The ship would be outside of the board with the provided coordinates")
            return False
        
        #now check if the ship will fit in the board with its size
        if vertical:
            if posY + ship_size > board_size:
                print("[WRONG INPUT]: The ship would be outside of the board with the provided coordinates")
                return False
        else:
            if posX + ship_size > board_size:
                print("[WRONG INPUT]: The ship would be outside of the board with the provided coordinates")
                return False

        #if the ship is vertical
        if vertical:

            if not force_place:
                #check to see if any of the spots are already occupied by another ship
                for row in range(ship_size):
                    tile = self.board[posY + row][posX]
                    if tile != "o" and tile != "?":
                        print("[WRONG INPUT]: Another ship is already occupying an area you are trying to put the ship on")
                        return False
                
            #now start placing the ship in the board
            if not force_place:
                list_of_ships.append([])
            for row in range(ship_size):
                if not force_place:
                    list_of_ships[-1].append([posX, posY + row])
                if row == 0:
                    self.board[posY][posX] = "^"
                elif row == ship_size - 1:
                    self.board[posY + row][posX] = "v"
                else:
                    self.board[posY + row][posX] = "|" 
            if not force_place:
                list_of_ships[-1].append(ship_size)

        #if the ship is placed horizontally
        else:

            if not force_place:
                #check to see if any of the spots are already occupied by another ship
                for column in range(ship_size):
                    tile = self.board[posY][posX + column]
                    if tile != "o" and tile != "?":
                        print("[WRONG INPUT]: Another ship is already occupying an area you are trying to put the ship on")
                        return False
                
            #now start placing the ship in the board
            if not force_place:
                list_of_ships.append([])
            for column in range(ship_size):
                if not force_place:
                    list_of_ships[-1].append([posX + column, posY])
                if column == 0:
                    self.board[posY][posX] = "<"
                elif column == ship_size - 1:
                    self.board[posY][posX + column] = ">"
                else:
                    self.board[posY][posX + column] = "-" 

            if not force_place:
                list_of_ships[-1].append(ship_size)

        return True

    #the opponent shot the coordinate (x, y), try to see if it was a valid shot or if it hit something
    #returns -1 if the coordinate is off the board or the hit are has already been hit
    #returns 0 if the shot was valid and hit nothing.
    #returns 1 if the shot was valid and hit a ship.
    def shoot_point(self, x, y, shooting_opponent = True):
        #trying to shoot outside of the board
        if(x < 0 or x >= board_size or y < 0 or y >= board_size):
            return -1
        
        tile = self.board[y][x].lower()
        #trying to shoot a tile that's already been shot
        if tile == "x" or tile == "?":
            return -1
        
        #shot was succesful but hit nothing
        elif tile == "o":
            self.board[y][x] = "X"
            return 0
        
        else:
            #if you are shooting an opponent, you can ONLY shoot an "o" spot (a place you haven't shot yet)
            if shooting_opponent and tile != "o":
                return -1
            self.board[y][x] = "X"
            return 1
    
    #mark a point on the board with a question mark "?", this is where the opponent's part of a ship is, but you still don't know its formation
    def mark_point(self, x, y):
        #trying to shoot outside of the board
        if(x < 0 or x >= board_size or y < 0 or y >= board_size):
            return -1
        
        self.board[y][x] = "?"

    #handles the logic of sending and recieving data until someone loses or leaves
    def play(self, enemy_board, socket, skip_turn = False):
        while True:
            if not skip_turn:
                # Send data

                #iterate until a valide move was inputted
                while True:
                    print("[GAME]: This is how the enemy board looks:")
                    print(enemy_board)
                    
                    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    print("[GAME]: Your move:")
                    
                    try:
                        #I am doing .split()[0] to ignore any extra input and not crash the game
                        x = input("[INPUT] X position to attack on:")
                        y = input("[INPUT] Y position to attack on:")
                        if(enemy_board.shoot_point(int(x), int(y), True) != -1):
                            break
                        else:
                            print("\n\033[31m[WRONG INPUT]: you are hitting outside of the board or a tile that has already been hit, try again!\033[0m \n")
                    except ValueError:
                        print("\n\033[31m[WRONG INPUT]: you need to input numbers as coordinates to attack on\033[0m\n")

                socket.sendall((x + " " + y).encode())

            # Receive data about the game state after shooting
            data = socket.recv(1024).decode()

            #there are 4 in-game keywords:
            #miss: you missed your shot, it's now the opponent's turn
            #hit: you hit a ship, but you still don't know its formation, it's your turn again
            #destroy: you destroyed a ship, and it's still your turn
            #won: you won the game!
            if not skip_turn:
                if data.lower() == "hit":
                    print("\n\033[32m[GAME]: You hit something!\033[0m\n")
                    enemy_board.mark_point(int(x), int(y))

                elif data.lower() == "destroy":
                    print("\n\033[32m[GAME]: YOU DESTROYED A SHIP!\033[0m\n")

                    #when you destroyed a ship, you should receive data about the destroyed ship:
                    #The format is the following: {posX, posY, ship_size, vertical}
                    destroyed_ship_data = socket.recv(1024).decode().split()
                    x = int(destroyed_ship_data[0])
                    y = int(destroyed_ship_data[1])

                    vertical = True
                    if(destroyed_ship_data[3].lower() == "false"):
                        vertical = False
                    enemy_board.place_ship(int(destroyed_ship_data[2]), x, y, vertical, True)

                elif data.lower() == "won":
                    print("\n\033[32m[GAME]: YOU WON THE GAME!!!\033[0m\n")

                    #when you destroyed a ship, you should receive data about the destroyed ship:
                    #The format is the following: {posX, posY, ship_size, vertical}
                    destroyed_ship_data = socket.recv(1024).decode().split()
                    x = int(destroyed_ship_data[0])
                    y = int(destroyed_ship_data[1])

                    vertical = True
                    if(destroyed_ship_data[3].lower() == "false"):
                        vertical = False
                    enemy_board.place_ship(int(destroyed_ship_data[2]), x, y, vertical, True)

                    #print the enemy board
                    print("[GAME]: Enemy board:")
                    print(enemy_board)

                    #print your own board
                    print("\n[GAME]: Your board:")
                    print(self)

                    #send your board layout to the opponent:
                    for ship_info in list_of_ships:
                         #try to find if the ship is vertical or horizontal
                        vertical = True
                        if ship_info[0][0] < ship_info[1][0]:
                            vertical = False
                        socket.send(f"{ship_info[0][0]} {ship_info[0][1]} {len(ship_info) - 1} {vertical}".encode())

                        #wait for a response before sending the next data
                        socket.recv(1024)
                    
                    #finally, when you are done, send a "good game" message to the opponent
                    socket.send("good game".encode())
                    break
                
                elif data.lower() == "miss":
                    print("\n\033[31m[GAME]: You missed:\033[0m\n")
                    print(enemy_board)
                    data = socket.recv(1024).decode()

                    print(f"[HOST] shooting: {data}")
                    data = data.split(" ")
                    x = int(data[0])
                    y = int(data[1])

                    hit_state = self.shoot_point(x, y, False)
                    #if one of my ships were hit
                    if(hit_state == 1):
                        skip_turn = True

                        #find out which ship was hit
                        for ship_info in list_of_ships:
                            for coordinates in ship_info:
                                if type(coordinates) is list:
                                    if coordinates[0] == x and coordinates[1] == y:
                                        #if the ship was found, reduce its health by 1
                                        ship_info[-1] = ship_info[-1] - 1

                                        #if the ship health reached 0, it got destroyed, send that data to the opponent
                                        if ship_info[-1] == 0:

                                            game_ended = False
                                            #before that, check if all the ships have been destroyed, if so, send a "won" message, you lost.
                                            for ships in list_of_ships:
                                                if ships[-1] > 0:
                                                    socket.sendall("destroy".encode())
                                                    break

                                            #if the for loop was finished succesfully (didn't reach the break line), you have lost the game
                                            else:
                                                socket.sendall("won".encode())
                                                game_ended = True
                                            
                                            #try to find if the ship is vertical or horizontal
                                            vertical = True
                                            if ship_info[0][0] < ship_info[1][0]:
                                                vertical = False
                                            socket.sendall(f"{ship_info[0][0]} {ship_info[0][1]} {len(ship_info) - 1} {vertical}".encode())

                                            if game_ended:
                                                print("\n\033[31m[GAME]: You lost...\033[0m\n")
                                            
                                                print("[GAME]: this is your board")
                                                print(self)

                                                #find out what the opponoent's layout looked like
                                                data = socket.recv(1024).decode()
                                                while data != "good game":

                                                    data = data.split()

                                                    x = int(data[0])
                                                    y = int(data[1])

                                                    vertical = True
                                                    if(data[3].lower() == "false"):
                                                        vertical = False
                                                    enemy_board.place_ship(int(data[2]), x, y, vertical, True)

                                                    socket.sendall("got the data".encode())


                                                    data = socket.recv(1024).decode()


                                                print("[GAME]: This is the opponent's board")
                                                print(enemy_board)

                                                socket.close()
                                                return

                                        #if the ship wasn't destroyed, send a regular hit
                                        else:
                                            socket.sendall("hit".encode())
                    #if the opponent missesd (or sent an illegal move)
                    elif (hit_state == 0 or hit_state == -1):
                        socket.sendall("miss".encode())

                    print("[GAME]: This is how your board looks like:")
                    print(self)
            
            
            else:
                skip_turn = False

                #I just copy pasted the following code from the above section

                print(f"[HOST] shooting: {data}")
                data = data.split(" ")
                x = int(data[0])
                y = int(data[1])

                hit_state = self.shoot_point(x, y, False)
                #if one of my ships were hit
                if(hit_state == 1):
                    skip_turn = True

                    #find out which ship was hit
                    for ship_info in list_of_ships:
                        for coordinates in ship_info:
                            if type(coordinates) is list:
                                if coordinates[0] == x and coordinates[1] == y:
                                    #if the ship was found, reduce its health by 1
                                    ship_info[-1] = ship_info[-1] - 1

                                    #if the ship health reached 0, it got destroyed, send that data to the opponent
                                    if ship_info[-1] == 0:

                                        game_ended = False
                                        #before that, check if all the ships have been destroyed, if so, send a "won" message, you lost.
                                        for ships in list_of_ships:
                                            if ships[-1] > 0:
                                                socket.sendall("destroy".encode())
                                                break

                                        #if the for loop was finished succesfully (didn't reach the break line), you have lost the game
                                        else:
                                            socket.sendall("won".encode())
                                            game_ended = True

                                        #try to find if the ship is vertical or horizontal
                                        vertical = True
                                        if ship_info[0][0] < ship_info[1][0]:
                                            vertical = False
                                        socket.sendall(f"{ship_info[0][0]} {ship_info[0][1]} {len(ship_info) - 1} {vertical}".encode())

                                        if game_ended:
                                            print("\n\033[31m[GAME]: You lost...\033[0m\n")
                                            
                                            print("[GAME]: this is your board")
                                            print(self)

                                            #find out what the opponoent's layout looked like
                                            data = socket.recv(1024).decode()
                                            while data != "good game":

                                                data = data.split()

                                                x = int(data[0])
                                                y = int(data[1])

                                                vertical = True
                                                if(data[3].lower() == "false"):
                                                    vertical = False
                                                enemy_board.place_ship(int(data[2]), x, y, vertical, True)

                                                socket.sendall("got the data".encode())

                                                data = socket.recv(1024).decode()

                                            print("[GAME]: This is the opponent's board ")
                                            print(enemy_board)

                                            socket.close()
                                            return

                                    #if the ship wasn't destroyed, send a regular hit
                                    else:
                                        socket.sendall("hit".encode())
                #if the opponent missesd (or sent an illegal move)
                elif (hit_state == 0 or hit_state == -1):
                    socket.sendall("miss".encode())

                print("[GAME]: This is how your board looks like:")
                print(self)

        socket.close()