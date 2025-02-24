import tkinter as tk
from tkinter import font
from typing import NamedTuple
from itertools import cycle

class Player(NamedTuple):
    """Defining the player class"""
    label:str
    color:str

class Move(NamedTuple):
    """Defining the move class"""
    row:int
    col:int
    label:str=""

BOARD_SIZE=3
DEFAULT_PLAYERS=(
    Player(label="X",color="red"),
    Player(label="O", color="blue")
)

class TicTacToeGame:
    """Class for the game logic"""
    def __init__(self,players=DEFAULT_PLAYERS,board_size=BOARD_SIZE):
        """Initialising all the attributes"""
        self.players=cycle(players)
        self.board_size=board_size
        self.current_player=next(self.players)
        self.winner_combo=[]
        self.current_moves=[]
        self._has_winner=False
        self.winning_combos=[]
        self.setup_board()
    
    def setup_board(self):
        """Setting up the board for possible combos"""
        self.current_moves=[
            [Move(row,col) for col in range(self.board_size)] for row in range(self.board_size)
        ]
        self.winning_combos=self.get_winning_combos()

    def get_winning_combos(self):
        """Finding the winning combos"""
        rows=[
            [(move.row,move.col) for move in row] for row in self.current_moves
        ]
        columns=[list(col) for col in zip(*rows)]
        first_diagonal=[row[i] for i,row in enumerate(rows)]
        second_diagonal=[row[i] for i,row in enumerate(reversed(columns))]
        return rows+columns+[first_diagonal,second_diagonal]

    def is_valid_move(self,move):
        """Return True if move is valid, and False otherwise"""
        row,col=move.row,move.col
        move_was_not_played=self.current_moves[row][col].label==""
        no_winner=not self._has_winner
        return no_winner and move_was_not_played
    
    def process_move(self,move):
        """Process the current move and check if it's a win"""
        row,col=move.row,move.col
        self.current_moves[row][col]=move
        for combo in self.winning_combos:
            results = set(
                self.current_moves[n][m].label for n,m in combo
            )
            is_win=(len(results)==1) and ("" not in results)
            if is_win:
                self._has_winner=True
                self.winner_combo=combo
                break
    
    def has_winner(self):
        """Return True if the game has a winner, False otherwise"""
        return self._has_winner

    def is_tied(self):
        """Return True of the game is tied, False otherwise"""
        no_winner=not self._has_winner
        played_moves=(
            move.label for row in self.current_moves for move  in row
        )
        return no_winner and all(played_moves)

    def toggle_player(self):
        """Return a toggled player"""
        self.current_player=next(self.players)

    def reset_game(self):
        """Reset the game state to play again"""
        for row,row_content in enumerate(self.current_moves):
            for col,_ in enumerate(row_content):
                row_content[col]=Move(row,col)
        self._has_winner=False
        self.winner_combo=[]


class TicTacToeBoard(tk.Tk):
    """A class that creates the game"""
    def __init__(self,game):
        """The title of the game"""
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self.game=game
        self.create_menu()
        self._create_board_display()
        self._create_board_grid()
    
    def create_menu(self):
        """Creates a menu for when the game ends"""
        menu_bar=tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu=tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again?",
            command=self.reset_board
            )
        file_menu.add_separator()
        file_menu.add_command(label="Exit",command=quit)
        menu_bar.add_cascade(label="File",menu=file_menu)
    
    def _create_board_display(self):
        """Function that creates the board's display"""
        display_frame=tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display=tk.Label(
            master=display_frame,
            text="Ready",
            font=font.Font(size=28,weight='bold')
        )
        self.display.pack()
    
    def _create_board_grid(self):
        """Creates the grid, with each square acting as a button"""
        grid_frame=tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self.game.board_size):
            self.rowconfigure(row,weight=2,minsize=50)
            self.columnconfigure(row,weight=2,minsize=50)
            for col in range(self.game.board_size):
                button=tk.Button(
                    master=grid_frame,
                    text='',
                    font=font.Font(size=36,weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="black"
                )
                self._cells[button]=(row,col)
                button.bind("<ButtonPress-1>",self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=4,
                    pady=4,
                    sticky="nsew"
                )
    
    def play(self,event):
        """Handle a player's move"""
        clicked_btn=event.widget
        row,col=self._cells[clicked_btn]
        move=Move(row,col,self.game.current_player.label)
        if self.game.is_valid_move(move):
            self.update_button(clicked_btn)
            self.game.process_move(move)
            if self.game.is_tied():
                self.update_display(msg="Tied game!", color="blue")
            elif self.game.has_winner():
                self.highlight_cells()
                msg=f'Player "{self.game.current_player.label}" won!'
                color=self.game.current_player.color
                self.update_display(msg,color)
            else:
                self.game.toggle_player()
                msg=f"{self.game.current_player.label}'s turn"
                self.update_display(msg)
    
    def update_button(self,clicked_btn):
        clicked_btn.config(text=self.game.current_player.label)
        clicked_btn.config(fg=self.game.current_player.color)
    
    def update_display(self,msg,color="black"):
        self.display["text"]=msg
        self.display["fg"]=color
    
    def highlight_cells(self):
        for button,coordinates in self._cells.items():
            if coordinates in self.game.winner_combo:
                button.config(highlightbackground="red")
    
    def reset_board(self):
        """Reset the game's board to play again"""
        self.game.reset_game()
        self.update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="black")
            button.config(text="")
            button.config(fg="black")


def main():
    """Create the game and run its main loop"""
    game=TicTacToeGame()
    board=TicTacToeBoard(game)
    board.mainloop()

if __name__=="__main__":
    main()