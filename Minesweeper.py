from random import randint
from math import sqrt
from tkinter import *
import time

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

"""This is the gameboard tile class. The properties determine
the game board index, number of surrounding mines, if it has been
revealed, if it is a mine or not and whether or not it has been marked
with a flag, respectivley."""
class Tile:
    def __init__(self, index, surrounding, revealed, type, has_flag):
        self.index = index
        self.surrounding = surrounding
        self.revealed = revealed
        self.type = type
        self.has_flag = has_flag

    """Determines the color of the digit shown on the gameboard,
    representing the number of surrounding mines."""
    def get_surrounding_digit_color(self):
        colors = ["#3371FF", "#196F3D", "#B7950B", "#EC6623", "#EC2923", "#AF1C18", "#6D110E", "#000000"]
        return colors[self.surrounding-1]

"""This is the flag class. Objects of this class have a gameboard index and a flag_drawing,
which is the actual drawing of the flag on the canvas."""
class Flag:
    def __init__(self, index, flag_drawing):
        self.index = index
        self.flag_drawing = flag_drawing

"""This is a class for the graphical menu that is loaded when the game starts.
It takes the master window as a parameter. The menu_selection property simply
states which part of the menu that is currently displayed. It is used
to check for button presses. This will be explained further on."""
class Menu:
    def __init__(self, master):
        self.master = master
        self.menu_selection = "main"

    """This method loads the main menu by creating a new canvas and drawing buttons on it."""
    def load_main_menu(self):
        self.file_name = "scores" + str(game.SIDE_LENGTH) + "x" + str(game.SIDE_LENGTH) + ".txt"

        try:
            scores_file = open(self.file_name, "r")
            self.score_list = scores_file.read().splitlines()
            scores_file.close()
        except:
            scores_file = open(self.file_name, "w")
            scores_file.close()
            scores_file = open(self.file_name, "r")
            self.score_list = scores_file.read().splitlines()
            scores_file.close()

        self.menu_canvas = Canvas(self.master, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg="#FDEBD0")
        self.menu_canvas.pack()
        self.menu_canvas.bind("<Button-1>", self.button_check)

        self.menu_canvas.create_rectangle(300, 125, 500, 175, fill="#82E0AA")
        self.menu_canvas.create_text(400, 150, text="START", font=("Helvetica", 28), anchor=CENTER, fill="black")
        self.menu_canvas.create_rectangle(300, 225, 500, 275, fill="#82E0AA")
        self.menu_canvas.create_text(400, 250, text="SETTINGS", font=("Helvetica", 28), anchor=CENTER, fill="black")
        self.menu_canvas.create_rectangle(300, 325, 500, 375, fill="#82E0AA")
        self.menu_canvas.create_text(400, 350, text="TOP SCORES", font=("Helvetica", 28), anchor=CENTER, fill="black")
        self.menu_canvas.create_rectangle(300, 425, 500, 475, fill="#82E0AA")
        self.menu_canvas.create_text(400, 450, text="EXIT", font=("Helvetica", 28), anchor=CENTER, fill="black")

    """This method loads the settings menu. A new canvas is created to display it.
    From here, the player can modify the gameboard size and the number of mines."""
    def load_settings(self):

        self.settings_canvas = Canvas(self.master, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg="#FDEBD0")
        self.settings_canvas.pack()
        self.settings_canvas.bind("<Button-1>", self.button_check)

        #Game size entry
        self.settings_canvas.create_text(400, 150, text="Gameboard Side Length", font=("Helvetica", 28), anchor=CENTER, fill="black")
        self.game_size_scale = Scale(self.master, from_=5, to=30, orient=HORIZONTAL)
        self.game_size_scale.set(game.SIDE_LENGTH)
        self.game_size_scale.place(x=400, y=170, anchor=N)
        self.size_enter_button = Button(self.master, text="SAVE", command=lambda:[self.set_game_size(self.game_size_scale.get()), self.terminate_settings(), self.load_settings()])
        self.size_enter_button.place(anchor=N, x=510, y=185)
        #Current value
        self.settings_canvas.create_text(400, 230, text="Current: " + str(game.SIDE_LENGTH) + "x" + str(game.SIDE_LENGTH), font=("Helvetica", 16), fill="#616A6B")

        #Mine amount entry
        self.settings_canvas.create_text(400, 290, text="Number of Mines", font=("Helvetica", 28), anchor=CENTER, fill="black")
        self.mine_scale = Scale(self.master, from_=1, to=game.SIDE_LENGTH**2-1, orient=HORIZONTAL)
        self.mine_scale.set(game.NUMBER_OF_MINES)
        self.mine_scale.place(anchor=N, x=400, y=300)
        self.mine_enter_button = Button(self.master, text="SAVE", command=lambda:[self.set_mine_amount(self.mine_scale.get()), self.terminate_settings(), self.load_settings()])
        self.mine_enter_button.place(anchor=N, x=510, y=315)
        #Current value
        self.settings_canvas.create_text(400, 360, text="Current: " + str(game.NUMBER_OF_MINES), font=("Helvetica", 16), fill="#616A6B")

        #Back button
        self.settings_canvas.create_rectangle(300, 425, 500, 475, fill="#82E0AA")
        self.settings_canvas.create_text(400, 450, text="BACK", font=("Helvetica", 28), anchor=CENTER, fill="black")

    """This method loads the top scores. Again, a new canvas is created for that sake.
    The top scores depend on the gameboard size. The names and scores of the players
    are displayed here."""
    def load_scores(self):

        scores_file = open(self.file_name, "r")
        self.score_list = scores_file.read().splitlines()
        scores_file.close()

        self.scores_canvas = Canvas(self.master, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg="#FDEBD0")
        self.scores_canvas.pack()
        self.scores_canvas.bind("<Button-1>", self.button_check)

        self.scores_canvas.create_text(400, 50, text="Top Scores For " + str(game.SIDE_LENGTH) + "x" + str(game.SIDE_LENGTH), font=("Helvetica", 24), fill="black")

        self.scores_canvas.create_rectangle(100, 70, 700, 100, fill="#A3E4D7")
        #Rank
        self.scores_canvas.create_text(150, 85, anchor=CENTER, text="Rank", font=("Helvetica", 18), fill="black")
        #Name
        self.scores_canvas.create_text(260, 85, anchor=CENTER, text="Name", font=("Helvetica", 18), fill="black")
        #Mines
        self.scores_canvas.create_text(380, 85, anchor=CENTER, text="Mine Setting", font=("Helvetica", 18), fill="black")
        #Time
        self.scores_canvas.create_text(490, 85, anchor=CENTER, text="Time", font=("Helvetica", 18), fill="black")
        #Score
        self.scores_canvas.create_text(620, 85, anchor=CENTER, text="Score", font=("Helvetica", 18), fill="black")

        row_height = 30
        for row in range(10):
            rank = row + 1

            if row % 2 == 0:
                self.scores_canvas.create_rectangle(100, (100 + row * row_height), 700, (130 + row * row_height), fill="#82E0AA")
            else:
                self.scores_canvas.create_rectangle(100, (100 + row * row_height), 700, (135 + row * row_height), fill="#A3E4D7")

            if row < len(self.score_list)//4:

                score_name = self.score_list[4*row]
                score_mine_amount = self.score_list[4*row+1]
                score_time = self.score_list[4*row+2]
                score_value = self.score_list[4*row+3]

                #Rank
                self.scores_canvas.create_text(150, (115 + row * row_height), anchor=CENTER, text=str(rank) + ".", font=("Helvetica", 18), fill="black")
                #Name
                self.scores_canvas.create_text(260, (115 + row * row_height), anchor=CENTER, text=score_name, font=("Helvetica", 18), fill="black")
                #Mines
                self.scores_canvas.create_text(380, (115 + row * row_height), anchor=CENTER, text=score_mine_amount, font=("Helvetica", 18), fill="black")
                #Time
                self.scores_canvas.create_text(490, (115 + row * row_height), anchor=CENTER, text=score_time, font=("Helvetica", 18), fill="black")
                #Score
                self.scores_canvas.create_text(620, (115 + row * row_height), anchor=CENTER, text=score_value, font=("Helvetica", 18), fill="black")

        self.scores_canvas.create_rectangle(300, 425, 500, 475, fill="#82E0AA")
        self.scores_canvas.create_text(400, 450, text="BACK", font=("Helvetica", 28), fill="black")

    """Deletes the canvas of the main menu, so that another canvas, and thereby
    another menu, or the gameboard, can take its place"""
    def terminate_menu(self):
        self.menu_canvas.destroy()

    """Deletes the canvas of the settings menu, so that another canvas, and thereby
    another menu, or the gameboard, can take its place"""
    def terminate_settings(self):
        self.settings_canvas.destroy()

    """Deletes the canvas of the top scores page, so that another canvas, and thereby
    another menu, or the gameboard, can take its place"""
    def terminate_scores(self):
        self.scores_canvas.destroy()

    """This method sets the number of mines to the amount that was specified in the settings."""
    def set_mine_amount(event, amount):
        game.NUMBER_OF_MINES = amount

    """This method sets the gameboard size to the size that was specified in the settings."""
    def set_game_size(event, side_length):
        game.SIDE_LENGTH = side_length

    """Checks what buttons are being pressed depending on what menu is currently loaded. This is
    because some buttons have the same position on different pages. This is where the menu_selection
    property comes in handy."""
    def button_check(self, event):
        if (event.x >= 300) and (event.x <= 500):
            #start
            if (event.y >= 125) and (event.y <= 175):
                if self.menu_selection == "main":
                    self.terminate_menu()
                    game.draw_game_board()
            #settings
            elif (event.y >= 225) and (event.y <= 275):
                if self.menu_selection == "main":
                    self.menu_selection = "settings"
                    self.terminate_menu()
                    self.load_settings()
            #scores
            elif (event.y >= 325) and (event.y <= 375):
                if self.menu_selection == "main":
                    self.menu_selection= "scores"
                    self.terminate_menu()
                    self.load_scores()
            #quit or back
            elif (event.y >= 425) and (event.y <= 475):
                if self.menu_selection == "settings":
                    self.menu_selection = "main"

                    self.terminate_settings()
                    self.load_main_menu()

                elif self.menu_selection == "scores":
                    self.menu_selection = "main"
                    self.terminate_scores()
                    self.load_main_menu()

                else:
                    self.master.destroy()

"""An object of the timer class displays a timer on the given canvas.
It starts at 00:00. The stop_timer property simply stops the timer."""
class Timer:
    def __init__(self, master, canvas):
        self.master = master
        self.canvas = canvas
        self.minutes = 0
        self.seconds = 0
        self.stop_timer = False

        self.draw_timer_panel()
        self.draw_time()

    """This method displays the timer panel on the gameboard canvas."""
    def draw_timer_panel(self):
        self.timer_panel = self.canvas.create_rectangle(650, 50, 750, 100, fill="#82E0AA")
        self.colon = self.canvas.create_text(700, 75, text=":", font=("Helvetica", 28), anchor=CENTER, fill="black")
        self.minute_digit = self.canvas.create_text(675, 75, text="00", font=("Helvetica", 28), anchor=CENTER, fill="black")
        self.second_digit = self.canvas.create_text(725, 75, text="00", font=("Helvetica", 28), anchor=CENTER, fill="black")

    """This method displays the actual time. It stops at 10 minutes"""
    def draw_time(self):
        if self.stop_timer == False:
            self.canvas.itemconfig(self.minute_digit, text="0" + str(self.minutes))
            if self.seconds < 10:
                self.canvas.itemconfig(self.second_digit, text="0" + str(self.seconds))
            else:
                self.canvas.itemconfig(self.second_digit, text=str(self.seconds))

            self.seconds += 1
            if self.minutes < 10:
                if self.seconds < 60:
                    self.master.after(1000, self.draw_time)
                else:
                    self.seconds = 0
                    self.minutes += 1
                    self.master.after(1000, self.draw_time)
            else:
                self.canvas.itemconfig(self.minute_digit, text="10")
                self.canvas.itemconfig(self.second_digit, text="00")

"""This class manages all the graphical aspects of the game. It takes the master window
as a parameter. It sets the default values of the amount of mines and the side length
of the gameboard, measured in game tiles."""
class Game_GUI:
    def __init__(self, master):
        self.master = master
        self.NUMBER_OF_MINES = 10
        self.SIDE_LENGTH = 10

    """This method draws the gameboard, including the timer and a back button.
    This is done by creating a canvas and drawing on it. The mouse buttons are
    bound to the canvases to check where on the canvas the player clicks. The tiles
    are created here."""
    def draw_game_board(self):
        self.SIZE = int(self.SIDE_LENGTH**2)
        self.SQUARE_SIZE = (WINDOW_HEIGHT - 20) // self.SIDE_LENGTH
        self.game_end = False
        self.flags = []
        self.TILES = create_tiles()

        self.game_canvas = Canvas(self.master, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bg="#FDEBD0")
        self.game_canvas.pack()
        self.game_canvas.bind("<Button-1>", self.check_click_position)
        self.game_canvas.bind("<Button-2>", self.flag_check)
        self.game_canvas.bind("<Button-3>", self.flag_check)

        self.squares = []
        x, y = 10, 10
        for _ in range(self.SIDE_LENGTH):
            for _ in range(self.SIDE_LENGTH):
                self.squares.append(self.game_canvas.create_rectangle(x, y, x+self.SQUARE_SIZE, y+self.SQUARE_SIZE, fill="#82E0AA"))
                x += self.SQUARE_SIZE
            y += self.SQUARE_SIZE
            x = 10

        self.back_button = self.game_canvas.create_rectangle(650, 500, 750, 550, fill="#82E0AA")
        self.back_button_text = self.game_canvas.create_text(700, 525, text="BACK", font=("Helvetica", 28), anchor=CENTER, fill="black")

        self.timer = Timer(self.master, self.game_canvas)

    """This method deletes the gameboard canvas and thereby everything in it."""
    def del_game_board(self):
        self.game_canvas.destroy()

    """This method reveals every tile on the board, graphically.
    It is called at the end of the game.
    Nota bene: it does not change the revealed value of the tiles."""
    def reveal_game_board(self):
        for flag in self.flags:
            self.game_canvas.delete(flag.flag_drawing)

        for tile in self.TILES:
            self.game_end = True
            self.game_canvas.itemconfig(self.squares[tile.index], fill="#ABEBC6")

            if tile.type == "mine":
                center_square_y, center_square_x = self.get_square_center_coordinates(tile.index)
                radius = int(0.35 * self.SQUARE_SIZE)

                self.game_canvas.create_oval((center_square_x - radius), (center_square_y - radius), (center_square_x + radius), (center_square_y + radius), outline="#000000", fill="#000000", width=1)

            elif tile.surrounding > 0:
                self.draw_digit(tile.index)

    """This method sets the game time as a string."""
    def set_game_time_string(self):
        if (self.timer.seconds-1) < 10:
            self.game_time = str(self.timer.minutes) + ":0" + str(self.timer.seconds-1)
        else:
            self.game_time = str(self.timer.minutes) + ":" + str(self.timer.seconds-1)

    """This method returns the coordinates of the center of a square of a certain index.
    It is used when drawing flags, mines and digits in the center of tiles.
    Nota bene: the terms square and tile can be used interchangably when describing
    the game in speech. The distinction between them is that tiles are objects of
    the Tile class and quares are the graphical representations thereof."""
    def get_square_center_coordinates(self, index):
        center_square_y = int(self.SQUARE_SIZE * (index // self.SIDE_LENGTH + 0.5)) + 10
        center_square_x = int(self.SQUARE_SIZE * (index % self.SIDE_LENGTH + 0.5)) + 10
        return center_square_y, center_square_x

    """This method draws the digit representing the surrounding mines value."""
    def draw_digit(self, index):
        font_size = int(self.SQUARE_SIZE * 0.75)
        center_square_y, center_square_x = self.get_square_center_coordinates(index)
        text_color = self.TILES[index].get_surrounding_digit_color()
        surrounding = self.TILES[index].surrounding
        #Displays the number of surrounding mines graphically
        self.game_canvas.create_text(center_square_x, center_square_y, text=str(surrounding), font=("Helvetica", font_size), anchor=CENTER, fill=text_color)

    """This method checks what type of tile was clicked. If it was a mine,
    another function is called. If it was a tile with no mines surrounding it, another
    function is called to check if there are adjacent tiles whose surroundings
    are also void of mines. Otherwise, the surrounding value is shown by a call
    to draw_digit. It also checks if the player has won after the click and prompts
    a message if they did. The same thing is done upon losing."""
    def evaluate_click(self, tile_index):
        self.toggle_flag_check = False
        self.surrounding_flags = 0
        self.flag_error = None
        #Makes sure the clicked tile is neither revealed nor is marked with a flag
        if self.TILES[tile_index].has_flag == False:
            #Reveals mines
            if self.TILES[tile_index].type == "mine":
                self.mine_click(tile_index)

            #Reveals field
            elif (self.TILES[tile_index].surrounding == 0) and (self.TILES[tile_index].revealed == False):
                self.reveal_tiles(tile_index)

            #Draws the digit
            elif (self.TILES[tile_index].surrounding > 0) and (self.TILES[tile_index].revealed == False):
                self.game_canvas.itemconfig(self.squares[tile_index], fill="#ABEBC6")
                self.draw_digit(tile_index)
                self.TILES[tile_index].revealed = True

            #Checks if a revealed digit tile is clicked again
            elif (self.TILES[tile_index].surrounding > 0) and (self.TILES[tile_index].revealed == True):
                self.toggle_flag_check = True
                check_surrounding(tile_index, self.TILES)
                self.toggle_flag_check = False
                if (self.surrounding_flags == self.TILES[tile_index].surrounding) and (self.flag_error == None):
                    self.reveal_tiles(tile_index)

            if check_win(self.master, self.TILES) == True:
                self.score = "perfect"
                self.timer.stop_timer = True
                self.set_game_time_string()
                #You won panel
                Label(self.game_canvas, bg="#82E0AA", text="You won! Time: " + self.game_time, font=("Helvetica", 30)).place(anchor=N, height=70, width=400, x=300, y=300 - 70)
                #Reaveals gameboard
                self.reveal_game_board()

                check_highscores(self.score, self.game_time)

    """This function is called when the player clicks a mine. The game is over. The score is determined
    by a function call, a "you lost"-panel is displayed, the gameboard is revealed graphically and if the
    function check_highscores() is called to see if the score qualifies for the top list."""
    def mine_click(self, tile_index):
        self.score = check_loss_score(self.TILES)
        self.timer.stop_timer = True
        self.set_game_time_string()
        #You lost panel
        Label(self.game_canvas, bg="red", text="You lost. Score: " + str(self.score), font=("Helvetica", 30)).place(anchor=N, height=70, width=400, x=300, y=300 - 70)
        #Reveals gameboard
        self.reveal_game_board()
        #Paint the clicked square red
        self.game_canvas.itemconfig(self.squares[tile_index], fill="#e81414")

        check_highscores(self.score, self.game_time)

    """This function is called when the player clicked a tile with no surrounding mines.
    It calls check_surrounding(), then reveals all of the tiles that were set to the revealed
    state by check_surrounding()."""
    def reveal_tiles(self, tile_index):
        self.TILES[tile_index].revealed = True
        check_surrounding(tile_index, self.TILES)
        #Reveals the field.
        for tile in self.TILES:
            if (tile.revealed == True) and (self.game_canvas.itemcget(self.squares[tile.index], "fill") == "#82E0AA"):
                self.game_canvas.itemconfig(self.squares[tile.index], fill="#ABEBC6")
                if tile.surrounding == 0:
                    pass
                else:
                    self.draw_digit(tile.index)

    """This method checks where on the canvas the player has clicked. If the click
    occurred on the gameboard, the evaluate_click() function is called. If the
    back button is pressed, the main menu is loaded. This will be explained further down the code."""
    def check_click_position(self, event):
        #Checks back button
        if (event.x >= 650) and (event.x <= 750) and (event.y >= 500) and (event.y <= 550):
                self.timer.stop_timer = True
                del self.timer
                self.del_game_board()
                menu.load_main_menu()

        #Checks on game board
        elif (event.x >= 10) and (event.x <= self.SQUARE_SIZE * self.SIDE_LENGTH + 10) and \
        (event.y >= 10) and (event.y <= self.SQUARE_SIZE * self.SIDE_LENGTH + 10) and (self.game_end == False):
            tile_index = int((event.x-10) // self.SQUARE_SIZE + ((event.y-10) // self.SQUARE_SIZE) * self.SIDE_LENGTH)
            """Lägga till create_tiles() här ist så första draget garanterat inte mina"""
            self.evaluate_click(tile_index)

    """This method returns the list index of the flag object on a certain game tile.
    To clarify: A flag has an index in a list of flag objects. This index does not
    necessarily coincide its tile index on the gameboard. This method simply translates
    between the two."""
    def get_flag_list_index(self, tile_index):
        for index_of_flag_in_flag_list, flag in enumerate(self.flags):
            if flag.index == tile_index:
                return index_of_flag_in_flag_list

    """This method checks which tile a player right clicks on, then creates flag objects and appends
    them to a list of flags. If the same tile i right clicked again, the flag i removed. It also checks
    if the player has won by marking of mines after every placed flag."""
    def flag_check(self, event):
        if self.game_end == False:
            tile_index = (event.x-10) // self.SQUARE_SIZE + ((event.y-10) // self.SQUARE_SIZE) * self.SIDE_LENGTH
            #Checks if event occurred on the gameboard
            if (event.x >= 10) and (event.x <=590) and (event.y >= 10) and (event.y <= 590):
                self.toggle_flag(tile_index)

                #Checks if the player won
                if check_win(self.master, self.TILES) == True:
                    self.score = "perfect"
                    self.timer.stop_timer = True
                    self.set_game_time_string()
                    #You won panel
                    Label(self.game_canvas, bg="green", text="You won! Time: " + self.game_time, font=("Helvetica", 30)).place(anchor=N, height=70, width=400, x=300, y=300 - 70)
                    #Reveasl gameboard
                    self.reveal_game_board()

                    check_highscores(self.score, self.game_time)

    """This method toggles the graphical flag on the gameboard."""
    def toggle_flag(self, index):
        center_square_y, center_square_x = self.get_square_center_coordinates(index)
        radius = int(0.2 * self.SQUARE_SIZE)

        #Places flag by creating flag object
        if (self.TILES[index].has_flag == False) and (self.TILES[index].revealed == False):
            self.TILES[index].has_flag = True
            #Draws flag
            self.flags.append(Flag(index, self.game_canvas.create_oval(center_square_x - radius, center_square_y - radius, center_square_x + radius, center_square_y + radius, outline="#000000", fill="#A569BD", width=1)))
        #Removes flag by deleting the canvas drawing, then the object itself
        elif self.TILES[index].has_flag == True:
            self.TILES[index].has_flag = False
            #Deletes flag from canvas
            self.game_canvas.delete(self.flags[self.get_flag_list_index(index)].flag_drawing)
            #Removes the flag object
            del self.flags[self.get_flag_list_index(index)]

"""This function creates the tile objects of the game. It is done
by first generating random indices of mines, then iterating over
the specified number of tiles the gameboard and creating mines if
the current index is a mine index, and a tile otherwise."""
def create_tiles():
    MINE_INDICES = []
    TILES = []
    #Generating indices of mines
    for _ in range(game.NUMBER_OF_MINES):
        while True:
            mine_index = randint(0, (game.SIZE-1))
            if mine_index not in MINE_INDICES:
                MINE_INDICES.append(mine_index)
                break
    #Generating objects of the Tile class.
    for tile_index in range(game.SIZE):
        if tile_index in MINE_INDICES:
            TILES.append(Tile(tile_index, "*", False, "mine", False))

        else:
            i = 0
            surrounding = 0
            while i < len(MINE_INDICES):

                #Checks if either of the surrounding tiles is a mine. If it is, the surrounding variable is increased by one
                if (abs(tile_index - MINE_INDICES[i]) == game.SIDE_LENGTH) or \
                ((tile_index + 1 == MINE_INDICES[i]) and (tile_index % game.SIDE_LENGTH != game.SIDE_LENGTH - 1)) or \
                ((tile_index - 1 == MINE_INDICES[i]) and (tile_index % game.SIDE_LENGTH != 0)) or \
                ((abs(tile_index + 1 - MINE_INDICES[i]) == game.SIDE_LENGTH) and (tile_index % game.SIDE_LENGTH != game.SIDE_LENGTH - 1)) or \
                ((abs(tile_index - 1 - MINE_INDICES[i]) == game.SIDE_LENGTH) and (tile_index % game.SIDE_LENGTH != 0)):
                    surrounding += 1

                i += 1
            TILES.append(Tile(tile_index, surrounding, False, "tile", False))

    return TILES

"""This function checks the surroundings of a tile with no surrounding mines for tiles that
are in turn void of mines in their immediate surroundings."""
def check_surrounding(index, TILES):
    index_on_board_row = index % game.SIDE_LENGTH
    #Checks west and east
    check_W(index, TILES, index_on_board_row)
    check_E(index, TILES, index_on_board_row)
    #Checks north and south
    check_N(index, TILES, index_on_board_row)
    check_S(index, TILES, index_on_board_row)
    #Checks north east and south east
    check_NE(index, TILES, index_on_board_row)
    check_SE(index, TILES, index_on_board_row)
    #Checks north west and south west
    check_NW(index, TILES, index_on_board_row)
    check_SW(index, TILES, index_on_board_row)

"""This function reveals the tile west of itself if it has no flag and if that happens to be a tile
with no surrounding mine, check_surrounding() is called again with the index of that mine,
making check_surrounding a recursive, or semi-recursive, function. This function also checks for surrounding
flags if toggle_flag_check is True."""
def check_W(index, TILES, index_on_board_row):
    if index_on_board_row != 0:
        if (TILES[index - 1].surrounding == 0) and (TILES[index - 1].revealed == False) and \
        (TILES[index - 1].has_flag == False) and (game.toggle_flag_check == False):

            TILES[index - 1].revealed = True #reveals to the left
            check_surrounding(index - 1, TILES)

        elif (TILES[index - 1].revealed == False) and (TILES[index - 1].has_flag == False) and (game.toggle_flag_check == False):
            TILES[index - 1].revealed = True #reveals to the left

        elif (TILES[index - 1].has_flag == True) and (game.toggle_flag_check == True):
            game.surrounding_flags += 1
        #Checks if the flag is incorrectly placed
        elif (TILES[index - 1].type == "mine") and (TILES[index - 1].has_flag == False) and (game.toggle_flag_check == True):
            game.flag_error = index - 1

"""This function reveals the tile east of itself if it has no flag and if that happens to be a tile
with no surrounding mine, check_surrounding() is called again with the index of that mine,
making check_surrounding a recursive, or semi-recursive, function. This function also checks for surrounding
flags if toggle_flag_check is True."""
def check_E(index, TILES, index_on_board_row):
    if index_on_board_row != game.SIDE_LENGTH - 1:

        if (TILES[index + 1].surrounding == 0) and (TILES[index + 1].revealed == False) and \
        (TILES[index + 1].has_flag == False) and (game.toggle_flag_check == False):

            TILES[index + 1].revealed = True #reveals to the right
            check_surrounding(index + 1, TILES)

        elif (TILES[index + 1].revealed == False) and (TILES[index + 1].has_flag == False) and (game.toggle_flag_check == False):
            TILES[index + 1].revealed = True #reveals to the right

        elif (TILES[index + 1].has_flag == True) and (game.toggle_flag_check == True):
            game.surrounding_flags += 1
        #Checks if the flag is incorrectly placed
        elif (TILES[index + 1].type == "mine") and (TILES[index + 1].has_flag == False) and (game.toggle_flag_check == True):
            game.flag_error = index + 1

"""This function reveals the tile north of itself if it has no flag and if that happens to be a tile
with no surrounding mine, check_surrounding() is called again with the index of that mine,
making check_surrounding a recursive, or semi-recursive, function. This function also checks for surrounding
flags if toggle_flag_check is True."""
def check_N(index, TILES, index_on_board_row):
    if index >= game.SIDE_LENGTH:
        if (TILES[index - game.SIDE_LENGTH].surrounding == 0) and (TILES[index - game.SIDE_LENGTH].revealed == False) and \
        (TILES[index - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):

            TILES[index - game.SIDE_LENGTH].revealed = True #reveals above
            check_surrounding(index - game.SIDE_LENGTH, TILES)

        elif (TILES[index - game.SIDE_LENGTH].revealed == False) and (TILES[index - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):
            TILES[index - game.SIDE_LENGTH].revealed = True #reveals above

        elif (TILES[index - game.SIDE_LENGTH].has_flag == True) and (game.toggle_flag_check == True):
            game.surrounding_flags += 1
        #Checks if the flag is incorrectly placed
        elif (TILES[index - game.SIDE_LENGTH].type == "mine") and (TILES[index - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == True):
            game.flag_error = index - game.SIDE_LENGTH

"""This function reveals the tile south of itself if it has no flag and if that happens to be a tile
with no surrounding mine, check_surrounding() is called again with the index of that mine,
making check_surrounding a recursive, or semi-recursive, function. This function also checks for surrounding
flags if toggle_flag_check is True."""
def check_S(index, TILES, index_on_board_row):
    if index <= game.SIZE - game.SIDE_LENGTH - 1:
        if (TILES[index + game.SIDE_LENGTH].surrounding == 0) and (TILES[index + game.SIDE_LENGTH].revealed == False) and \
        (TILES[index + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):

            TILES[index + game.SIDE_LENGTH].revealed = True #reveals below
            check_surrounding(index + game.SIDE_LENGTH, TILES)

        elif (TILES[index + game.SIDE_LENGTH].revealed == False) and (TILES[index + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):
            TILES[index + game.SIDE_LENGTH].revealed = True

        elif (TILES[index + game.SIDE_LENGTH].has_flag == True) and (game.toggle_flag_check == True):
            game.surrounding_flags += 1
        #Checks if the flag is incorrectly placed
        elif (TILES[index + game.SIDE_LENGTH].type == "mine") and (TILES[index + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == True):
            game.flag_error = index + game.SIDE_LENGTH

"""This function reveals the tile north east of itself if it has no flag and if that happens to be a tile
with no surrounding mine, check_surrounding() is called again with the index of that mine,
making check_surrounding a recursive, or semi-recursive, function. This function also checks for surrounding
flags if toggle_flag_check is True."""
def check_NE(index, TILES, index_on_board_row):
    if (index >= game.SIDE_LENGTH) and (index_on_board_row != game.SIDE_LENGTH - 1):
        if (TILES[index + 1 - game.SIDE_LENGTH].surrounding == 0) and (TILES[index + 1 - game.SIDE_LENGTH].revealed == False) and \
        (TILES[index + 1 - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):

            TILES[index + 1 - game.SIDE_LENGTH].revealed = True #reveals up and to the right
            check_surrounding(index + 1 - game.SIDE_LENGTH, TILES)

        elif (TILES[index + 1 - game.SIDE_LENGTH].revealed == False) and (TILES[index + 1 - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):
            TILES[index + 1 - game.SIDE_LENGTH].revealed = True

        elif (TILES[index + 1 - game.SIDE_LENGTH].has_flag == True) and (game.toggle_flag_check == True):
            game.surrounding_flags += 1
        #Checks if the flag is incorrectly placed
        elif (TILES[index + 1 - game.SIDE_LENGTH].type == "mine") and (TILES[index + 1 - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == True):
            game.flag_error = index + 1 - game.SIDE_LENGTH

"""This function reveals the tile south east of itself if it has no flag and if that happens to be a tile
with no surrounding mine, check_surrounding() is called again with the index of that mine,
making check_surrounding a recursive, or semi-recursive, function. This function also checks for surrounding
flags if toggle_flag_check is True."""
def check_SE(index, TILES, index_on_board_row):
    if (index <= game.SIZE - game.SIDE_LENGTH - 1) and (index_on_board_row != game.SIDE_LENGTH - 1):
        if (TILES[index + 1 + game.SIDE_LENGTH].surrounding == 0) and (TILES[index + 1 + game.SIDE_LENGTH].revealed == False) and \
        (TILES[index + 1 + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):

            TILES[index + 1 + game.SIDE_LENGTH].revealed = True #reveals down and to the right
            check_surrounding(index + 1 + game.SIDE_LENGTH, TILES)

        elif (TILES[index + 1 + game.SIDE_LENGTH].revealed == False) and (TILES[index + 1 + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):
            TILES[index + 1 + game.SIDE_LENGTH].revealed = True

        elif (TILES[index + 1 + game.SIDE_LENGTH].has_flag == True) and (game.toggle_flag_check == True):
            game.surrounding_flags += 1
        #Checks if the flag is incorrectly placed
        elif (TILES[index + 1 + game.SIDE_LENGTH].type == "mine") and (TILES[index + 1 + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == True):
            game.flag_error = index + 1 + game.SIDE_LENGTH

"""This function reveals the tile north west of itself if it has no flag and if that happens to be a tile
with no surrounding mine, check_surrounding() is called again with the index of that mine,
making check_surrounding a recursive, or semi-recursive, function. This function also checks for surrounding
flags if toggle_flag_check is True."""
def check_NW(index, TILES, index_on_board_row):
    if (index >= game.SIDE_LENGTH) and (index_on_board_row != 0):
        if (TILES[index - 1 - game.SIDE_LENGTH].surrounding == 0) and (TILES[index - 1 - game.SIDE_LENGTH].revealed == False) and \
        (TILES[index - 1 - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):

            TILES[index - 1 - game.SIDE_LENGTH].revealed = True #reveals up and to the left
            check_surrounding(index - 1 - game.SIDE_LENGTH, TILES)

        elif (TILES[index - 1 - game.SIDE_LENGTH].revealed == False) and (TILES[index - 1 - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):
            TILES[index - 1 - game.SIDE_LENGTH].revealed = True

        elif (TILES[index - 1 - game.SIDE_LENGTH].has_flag == True) and (game.toggle_flag_check == True):
            game.surrounding_flags += 1
        #Checks if the flag is incorrectly placed
        elif (TILES[index - 1 - game.SIDE_LENGTH].type == "mine") and (TILES[index - 1 - game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == True):
            game.flag_error = index - 1 - game.SIDE_LENGTH

"""This function reveals the tile south west of itself if it has no flag and if that happens to be a tile
with no surrounding mines, check_surrounding() is called again with the index of that mine,
making check_surrounding a recursive, or semi-recursive, function. This function also checks for surrounding
flags if toggle_flag_check is True."""
def check_SW(index, TILES, index_on_board_row):
    if (index <= game.SIZE - game.SIDE_LENGTH - 1) and (index_on_board_row != 0):
        if (TILES[index - 1 + game.SIDE_LENGTH].surrounding == 0) and (TILES[index - 1 + game.SIDE_LENGTH].revealed == False) and \
        (TILES[index - 1 + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):

            TILES[index - 1 + game.SIDE_LENGTH].revealed = True #reveals down and to the right
            check_surrounding(index - 1 + game.SIDE_LENGTH, TILES)

        elif (TILES[index - 1 + game.SIDE_LENGTH].revealed == False) and (TILES[index - 1 + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == False):
            TILES[index - 1 + game.SIDE_LENGTH].revealed = True
        #Checks for flags
        elif (TILES[index - 1 + game.SIDE_LENGTH].has_flag == True) and (game.toggle_flag_check == True):
            game.surrounding_flags += 1
        #Checks if the flag is incorrectly placed
        elif (TILES[index - 1 + game.SIDE_LENGTH].type == "mine") and (TILES[index - 1 + game.SIDE_LENGTH].has_flag == False) and (game.toggle_flag_check == True):
            game.flag_error = index - 1 + game.SIDE_LENGTH

        if (game.surrounding_flags == TILES[index].surrounding) and (game.flag_error != None):
            game.mine_click(game.flag_error)

"""This function checks if the player has won or not. That can be done either by marking
every min or by revealing every non-mine tile."""
def check_win(master, TILES):
    #Checks if all non-min tiles are revealed. If yes: the game is won
    mine_win = False
    for tile in TILES:
        if (tile.revealed == False) and (tile.type == "tile"):
            reveal_win = False
            break
    else:
        reveal_win = True
    #Checks if all mines have flags. If yes: the game is won
    mines_with_flags = 0
    for tile in TILES:
        if (tile.has_flag == True) and (tile.type == "mine"):
            mines_with_flags += 1
    if mines_with_flags == game.NUMBER_OF_MINES:
        mine_win = True

    return True if (reveal_win == True) or (mine_win == True) else False

"""This function checks the score after the game has been lost. The score is simply the difference
between the number of marked mines and the number of marked non-mine tiles."""
def check_loss_score(TILES):
    score = 0
    for tile in TILES:
        if (tile.has_flag == True) and (tile.type == "mine"):
            score += 1
        elif (tile.has_flag == True) and (tile.type == "tile"):
            score -= 1
    return score

"""This function checks if the score is qualified for the top scores list. If it is, the player
is asked to provide their name. When entered, the function below takes over."""
def check_highscores(score, time):

    highscores = menu.score_list[3::4]
    highscore_times = menu.score_list[2::4]
    highscore_mine_setting = menu.score_list[1::4]
    rank_index = None

    for index, highscore in enumerate(highscores):
        #Both are win times
        if (score == "perfect") and (highscore == "perfect"):
            #Current mine setting is less than that of the highscore mine setting
            if game.NUMBER_OF_MINES == int(highscore_mine_setting[index]):
                rank_index = check_time(index, time, score, highscore)
                if rank_index != None:
                    break
            elif game.NUMBER_OF_MINES > int(highscore_mine_setting[index]):
                rank_index = index
                break
            else:
                continue

        #Highscore is win time and score is not or the passed score is a win, but not the highscore or neither are win times and the passed score is greater than the highscore
        elif ((score != "perfect") and (highscore == "perfect")) or \
        ((score == "perfect") and (highscore != "perfect")) or \
        (score > int(highscore)):
            if (game.NUMBER_OF_MINES > int(highscore_mine_setting[index])) or (game.NUMBER_OF_MINES == int(highscore_mine_setting[index])):
                rank_index = index
                break
            else:
                continue

        #Neither are win times and the passed score is equal to the highscore
        elif score == int(highscore):
            if game.NUMBER_OF_MINES > int(highscore_mine_setting[index]):
                rank_index = check_time(index, time, score, highscore)
                if rank_index != None:
                    break

    else:
        if len(highscores) < 10:
            rank_index = len(highscores)

    if rank_index != None:
        Label(game.game_canvas, bg="#82E0AA", text="You made the top scores list! Enter your name", font=("Helvetica", 18)).place(anchor=N, height=35, width=400, x=300, y=315)
        highscore_name_entry = Entry(game.game_canvas)
        highscore_name_entry.place(x=300, y=365, anchor=N)
        enter_button = Button(root, text="ENTER", command=lambda:[name_entry_key_press(highscore_name_entry.get(), rank_index), enter_button.destroy(), game.game_canvas.destroy(), menu.load_main_menu()])
        enter_button.place(anchor=N, x=430, y=365)
        highscore_name_entry.focus_set()

"""This function checks the game time against the highscore time."""
def check_time(index, time, score, highscore):

    highscores = menu.score_list[3::4]
    highscore_times = menu.score_list[2::4]
    rank_index = None

    #The times are both either below or exactly 10 minutes
    if (len(time) == len(highscore_times[index])):
        #The passed time is better. Determined by the minute
        if int(time[0]) < int(highscore_times[index][0]):
            rank_index = index

        #The passed time is better. Determined by the tens of seconds
        elif int(time[0]) == int(highscore_times[index][0]):
            if int(time[2]) < int(highscore_times[index][2]):
                rank_index = index

            #The passed time is better. Determined by the singular seconds
            elif int(time[2]) == int(highscore_times[index][2]):
                if int(time[3]) < int(highscore_times[index][3]):
                    rank_index = index

    #The win time is less than 10 minutes but the highscore time is 10
    elif (score == "perfect") and (highscore == "perfect") and (len(time) < len(highscore_times[index])):
        rank_index = index

    return rank_index

"""This function overwrites the old highscores list with the new highscores list.
This is done to separate files depending on the gameboard size."""
def name_entry_key_press(high_score_name, index):
    score = game.score
    time = game.game_time

    scores_file = open(menu.file_name, "r")
    highscore_stats = scores_file.readlines()
    scores_file.close()

    highscore_stats.insert(4*index, (str(score) + "\n"))
    highscore_stats.insert(4*index, (time + "\n"))
    highscore_stats.insert(4*index, (str(game.NUMBER_OF_MINES) + "\n"))
    highscore_stats.insert(4*index, (high_score_name[:15] + "\n"))

    if len(highscore_stats) == 44:
        for _ in range(4):
            del highscore_stats[-1]

    scores_file = open(menu.file_name, mode="w")
    scores_file.writelines(highscore_stats)
    scores_file.close()

if __name__ == "__main__":

    root = Tk()
    game = Game_GUI(root)
    menu = Menu(root)
    menu.load_main_menu()
    root.mainloop()
